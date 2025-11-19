from __future__ import annotations

import pandas
import re

# Dictionary of U.S. states
STATE_MAP = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
    "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
    "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"
}


def state_full_name(abbrev: str) -> str | None:
    """
    Return the full state name for a given abbreviation.
    Case-insensitive. Returns None if not found.
    """
    if not isinstance(abbrev, str):
        return None

    state = abbrev.strip().upper()
    if state in STATE_MAP:
        return STATE_MAP[state]
    return None


class BadDataException(ValueError, TypeError):
    """Raised when int(x) fails; behaves like both ValueError and TypeError."""

    def __init__(self, value, message=None):
        self.value = value
        super().__init__(message)


BAD_DATA = {
    "id": [],
    "category": [],
    "title": [],
    "body": [],
    "amenities": [],
    "bathrooms": [],
    "bedrooms": [],
    "currency": [],
    "fee": [],
    "has_photo": [],
    "pets_allowed": [],
    "price": [],
    "price_display": [],
    "price_type": [],
    "square_feet": [],
    "address": [],
    "cityname": [],
    "state": [],
    "latitude": [],
    "longitude": [],
    "source": [],
    "time": []
}

# Common state/territory abbreviations to exclude when they appear alone as the "city"
US_STATE_ABBR = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
    "MD", "MA", "MI",
    "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD",
    "TN", "TX", "UT",
    "VT", "VA", "WA", "WV", "WI", "WY", "DC", "PR", "VI", "GU", "AS", "MP"
}

US_STATE_NAMES = {
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware",
    "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana",
    "nebraska", "nevada", "new hampshire", "new jersey", "new mexico", "new york", "north carolina",
    "north dakota", "ohio", "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina",
    "south dakota", "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia",
    "wisconsin", "wyoming", "district of columbia", "washington dc", "dc"
}

COUNTY_TO_CITY = {
    "fulton county": "Atlanta",
    "henrico county": "Henrico",
    "montgomery county": "Rockville",
    "prince george county": "Upper Marlboro",
    "prince georges county": "Upper Marlboro",
    "los angeles county": "Los Angeles",
    "harris county": "Houston",
    "cook county": "Chicago",
    "dallas county": "Dallas",
    "orange county": "Orlando",
}

# Expand common city-name abbreviations when they start the city token
ABBREV_MAP = {
    "st": "saint", "st.": "saint",
    "ft": "fort", "ft.": "fort",
    "mt": "mount", "mt.": "mount",
    "slc": "salt lake city"  # common leftover
}

# Patterns we consider invalid for a city field
URL_PAT = re.compile(r"(https?://|www\.|\.(com|net|org|edu|gov|io|co|us)\b)", re.I)
COORD_PAIR = re.compile(r"^\s*-?\d+(?:\.\d+)?\s*[, ]\s*-?\d+(?:\.\d+)?\s*$")  # "40.7, -73.9" or "40.7 -73.9"
NUM_ONLY = re.compile(r"^\s*-?\d+(?:\.\d+)?\s*$")
ALLOWED_CHARS = re.compile(r"^[A-Za-z .'\-]+$")


def _expand_leading_abbrev(s: str) -> str:
    # Expand only if the *first* token is an abbreviation (e.g., "St Louis" -> "Saint Louis")
    tokens = s.split()
    if not tokens:
        return s
    first = tokens[0].lower().strip(".,")
    if first in ABBREV_MAP:
        tokens[0] = ABBREV_MAP[first]
    return " ".join(tokens)


def _fix_prefix_patterns(s: str) -> str:
    # "O Fallon" -> "O'Fallon" (only when O is a standalone leading token)
    s = re.sub(r"\bO\s+([A-Za-z])", r"O'\1", s)
    # "Mc Kees" -> "McKees", "Mc Donald" -> "McDonald"
    s = re.sub(r"\bMc\s+([A-Za-z])", r"Mc\1", s)
    return s


def clean_id(x):
    try:
        try:
            return int(x)
        except Exception:
            raise BadDataException(x)
    except BadDataException as e:
        BAD_DATA["id"].append(e.value)
        return None
    except Exception:
        BAD_DATA["id"].append(x)
        return None


def clean_category(x):
    try:
        x = str(x).lower().strip()
        parts = x.split('/')

        cleaned_parts = [
            re.sub(r'^(ousing|ing)', 'housing', p.strip())
            for p in parts
        ]

        if any(p == '2' for p in cleaned_parts):
            raise BadDataException(cleaned_parts)

        return cleaned_parts

    except BadDataException as e:
        BAD_DATA["category"].append(e.value)
        return None
    except Exception:
        BAD_DATA["category"].append(x)
        return None


def clean_title(x):
    try:
        return str(x)
    except BadDataException as e:
        BAD_DATA["title"].append(e.value)
        return None
    except Exception:
        BAD_DATA["title"].append(x)
        return None


def clean_body(x):
    try:
        return str(x)
    except BadDataException as e:
        BAD_DATA["body"].append(e.value)
        return None


def clean_amenities(x):
    try:
        # Convert to string and lowercase
        x = str(x).lower().strip()

        # Split first by '/', then flatten any comma-separated pieces
        raw_parts = []
        for part in x.split('/'):
            raw_parts.extend(part.split(','))

        # Clean and filter empty values
        cleaned_parts = [p.strip() for p in raw_parts if p.strip()]

        if any(p == 'nan' for p in cleaned_parts):
            raise BadDataException(cleaned_parts, 'nan')

        return cleaned_parts

    except BadDataException as e:
        BAD_DATA["amenities"].append(e.value)
        return None
    except Exception:
        BAD_DATA["amenities"].append(x)
        return None


def clean_bathrooms(x):
    try:
        # Normalize to lowercase string
        val = str(x).strip().lower()

        # If the value is invalid, raise your custom exception
        if val in {"nan", "no", "thumbnail"}:
            raise BadDataException(x)

        # Try converting to integer
        return int(float(val))  # handles '2.0' etc.

    except BadDataException as e:
        BAD_DATA["bathrooms"].append(e.value)
        return None
    except Exception:
        BAD_DATA["bathrooms"].append(x)
        return None


def clean_bedrooms(x):
    try:
        # Normalize value to lowercase string
        val = str(x).strip().lower()

        # Raise custom exception for clearly invalid values
        if val in {"nan", "no", "thumbnail", "cats,dogs"}:
            raise BadDataException(x)

        # Attempt numeric conversion (handles "2.0" etc.)
        return int(float(val))

    except BadDataException as e:
        BAD_DATA["bedrooms"].append(e.value)
        return None
    except Exception:
        BAD_DATA["bedrooms"].append(x)
        return None


def clean_currency(x):
    try:
        # Normalize value to lowercase string
        val = str(x).strip().upper()  # currency codes are uppercase by convention

        # Define acceptable currency codes
        valid_currencies = {"USD"}

        # Raise if not valid
        if val not in valid_currencies:
            raise BadDataException(x)

        return val

    except BadDataException as e:
        BAD_DATA["currency"].append(e.value)
        return None
    except Exception:
        BAD_DATA["currency"].append(x)
        return None


def clean_fee(x):
    try:
        # Normalize value
        val = str(x).strip().lower()

        # Map valid values
        if val == "yes":
            return True
        elif val == "no":
            return False

        raise BadDataException(x)

    except BadDataException as e:
        BAD_DATA["fee"].append(e.value)
        return None

    except Exception:
        BAD_DATA["fee"].append(x)
        return None


def clean_has_photo(x):
    try:
        # Normalize value
        val = str(x).strip().lower()

        # Map known valid values
        if val in {"yes", "thumbnail"}:
            return True
        elif val == "no":
            return False

        # Anything else is bad data
        raise BadDataException(x)

    except BadDataException as e:
        BAD_DATA["has_photo"].append(e.value)
        return None
    except Exception:
        BAD_DATA["has_photo"].append(x)
        return None


def clean_pets_allowed(x):
    try:
        val = str(x).strip().lower()

        # Handle truly missing or numeric data (bad)
        if val == "nan" or val.isnumeric():
            raise BadDataException(x)

        # Split on commas or slashes
        tokens = [t.strip() for t in re.split(r"[,/]", val) if t.strip()]

        has_cats = any(t == "cats" for t in tokens)
        has_dogs = any(t == "dogs" for t in tokens)
        has_none = any(t == "none" for t in tokens)

        # Determine clean category
        if has_cats and has_dogs:
            return "Cats&Dogs"
        if has_cats:
            return "Cats"
        if has_dogs:
            return "Dogs"
        if has_none:
            return "X"  # ← keep as string 'None', not Python None


    except BadDataException as e:
        BAD_DATA["pets_allowed"].append(e.value)
        return None
    except Exception:
        BAD_DATA["pets_allowed"].append(x)
        return None


def clean_price(x):
    try:
        return float(x)
    except BadDataException as e:
        BAD_DATA["price"].append(e.value)
        return None
    except Exception:
        BAD_DATA["price"].append(x)
        return None


def clean_price_display(x):
    try:
        if x is None:
            print(f"found None {x}")
            raise BadDataException(x)

        val = str(x).strip()

        # --- Detect "Weekly" / "Monthly" and print ---
        if re.search(r'\b(weekly|monthly)\b', val, flags=re.IGNORECASE):
            pass
            # print(f"found recurring term {x}")

        # --- Remove $ signs, commas, and spaces ---
        val = val.replace("$", "").replace(",", "").strip()

        # --- Extract numeric parts ---
        range_match = re.findall(r"[\d.]+", val)
        if len(range_match) == 0:
            # print(f"found non numeric term {x}")
            raise BadDataException(x)
        elif len(range_match) == 1:
            return float(range_match[0])
        else:
            # print(f"averaging terms {range_match=}")
            nums = [float(v) for v in range_match]
            return sum(nums) / len(nums)

    except BadDataException as e:
        BAD_DATA["price_display"].append(e.value)
        return None
    except Exception:
        BAD_DATA["price_display"].append(x)
        return None


def clean_price_type(x):
    try:
        val = str(x).strip().lower()

        # Valid categories
        if "monthly" in val:
            return "monthly"
        elif "weekly" in val:
            return "weekly"

        # print(f"found {x}")
        raise BadDataException(x, " i cant intepret")

    except BadDataException as e:
        BAD_DATA["price_type"].append(e.value)
        return None
    except Exception:
        BAD_DATA["price_type"].append(x)
        return None


def clean_square_feet(x):
    try:
        # Treat None and float('nan') as invalid
        if x is None:
            raise BadDataException(x)

        val = str(x).strip()

        # Detect values that contain only numbers or a decimal
        match = re.fullmatch(r"\d+(?:\.\d+)?", val)
        if match:
            return float(val)

        # print(f"found {x}")
        raise BadDataException(x)

    except BadDataException as e:
        BAD_DATA["square_feet"].append(e.value)
        return None
    except Exception:
        BAD_DATA["square_feet"].append(x)
        return None


def clean_address(x):
    try:
        # TODO
        # --- Handle missing / NaN values ---
        if x is None:
            raise BadDataException(x)

        val = str(x).strip()

        # --- Handle explicit invalid tokens ---
        if val.lower() in {"", "none", "nan"}:
            raise BadDataException(val)

        # --- Reject coordinate-like values (e.g., "40.2659 -77.4948") ---
        if re.fullmatch(r"^-?\d+(\.\d+)?\s*[,\s]\s*-?\d+(\.\d+)?$", val):
            raise BadDataException(val)

        # --- Reject numeric-only or "square feet" type values ---
        if re.fullmatch(r"[\d., ]+$", val) or "square" in val.lower() or "sq" in val.lower():
            raise BadDataException(val)

        # --- Basic address sanity check: must contain both a number and a letter ---
        if not (re.search(r"\d", val) and re.search(r"[A-Za-z]", val)):
            raise BadDataException(val)

        # --- Normalize whitespace and punctuation ---
        cleaned = re.sub(r"\s+", " ", val).strip(" ,.;-")

        return cleaned

    except BadDataException as e:
        BAD_DATA["address"].append(e.value)
        return None
    except Exception:
        BAD_DATA["address"].append(x)
        return None


def clean_city_name(x):
    try:
        if x is None:
            raise BadDataException(x)

        raw = str(x).strip()
        if raw == "" or raw.lower() in {"nan", "none", "null", "n/a"}:
            return None

        s = re.sub(r"\s+", " ", raw)

        # handle URLs, coordinates, numeric-only
        if URL_PAT.search(s) or COORD_PAIR.match(s) or NUM_ONLY.match(s):
            raise BadDataException(raw)

        # only allowed characters
        if not ALLOWED_CHARS.match(s):
            raise BadDataException(raw)

        s = _expand_leading_abbrev(s)
        s = _fix_prefix_patterns(s)
        s = re.sub(r"\s+", " ", s).strip(" ,.;-")
        s_lower = s.lower()

        # map counties to their city equivalents
        for county, city in COUNTY_TO_CITY.items():
            if county in s_lower:
                return city

        # reject pure state names
        if s_lower in US_STATE_NAMES:
            raise BadDataException(raw)

        # normalize capitalization
        s = " ".join(t.capitalize() if not (t.isupper() and len(t) <= 3) else t for t in s.split())
        if not re.search(r"[A-Za-z]", s):
            raise BadDataException(raw)

        return s

    except BadDataException as e:
        BAD_DATA["cityname"].append(e.value)
        return None
    except Exception:
        BAD_DATA["cityname"].append(x)
        return None


def clean_state(x):
    try:
        state_abbrev = str(x).strip().upper()
        if state_abbrev not in STATE_MAP:
            raise BadDataException(x, 'not a valid state')

        return STATE_MAP[state_abbrev]
    except BadDataException as e:
        BAD_DATA["state"].append(e.value)
        return None
    except Exception:
        BAD_DATA["state"].append(x)
        return None


def clean_latitude(x):
    try:
        latitude = float(x)
        out_of_range = latitude < -90.0 or latitude > 90.0

        if out_of_range:
            raise BadDataException(x, 'is out of range. Latitude values must be between -90 and 90 degrees.')

        return latitude
    except BadDataException as e:
        BAD_DATA["latitude"].append(e.value)
        return None
    except Exception:
        BAD_DATA["latitude"].append(x)
        return None


def clean_longitude(x):
    try:
        longitude = float(x)
        out_of_range = longitude < -180.0 or longitude > 180.0

        if out_of_range:
            raise BadDataException(x, 'is out of range. Longitude values must be between -180 and 180 degrees.')

        return float(x)
    except BadDataException as e:
        BAD_DATA["longitude"].append(e.value)
        return None
    except Exception:
        BAD_DATA["longitude"].append(x)
        return None


def clean_source(x):
    try:
        return str(x).strip().lower()
    except BadDataException as e:
        BAD_DATA["source"].append(e.value)
        return None
    except Exception:
        BAD_DATA["source"].append(x)
        return None


def clean_time(x):
    try:
        return str(x)
    except BadDataException as e:
        BAD_DATA["time"].append(e.value)
        return None
    except Exception:
        BAD_DATA["time"].append(x)
        return None


def clean(uci_df) -> pandas.DataFrame:
    cleaned_uci_df = pandas.DataFrame()
    cleaned_uci_df['id'] = uci_df['id'].apply(clean_id)
    cleaned_uci_df['category'] = uci_df['category'].apply(clean_category)
    cleaned_uci_df['title'] = uci_df['title']  # .apply(clean_title)
    cleaned_uci_df['body'] = uci_df['body']  # .apply(clean_body)
    cleaned_uci_df['amenities'] = uci_df['amenities'].apply(clean_amenities)
    cleaned_uci_df['bathrooms'] = uci_df['bathrooms'].apply(clean_bathrooms)
    cleaned_uci_df['bedrooms'] = uci_df['bedrooms'].apply(clean_bedrooms)
    cleaned_uci_df['currency'] = uci_df['currency'].apply(clean_currency)
    cleaned_uci_df['fee'] = uci_df['fee'].apply(clean_fee)
    cleaned_uci_df['has_photo'] = uci_df['has_photo'].apply(clean_has_photo)
    cleaned_uci_df['pets_allowed'] = uci_df['pets_allowed'].apply(clean_pets_allowed)
    cleaned_uci_df['price'] = uci_df['price'].apply(clean_price)
    cleaned_uci_df['price_display'] = uci_df['price_display'].apply(clean_price_display)
    cleaned_uci_df['price_type'] = uci_df['price_type'].apply(clean_price_type)
    cleaned_uci_df['square_feet'] = uci_df['square_feet'].apply(clean_square_feet)
    cleaned_uci_df['address'] = uci_df['address'].apply(clean_address)
    cleaned_uci_df['cityname'] = uci_df['cityname'].apply(clean_city_name)
    cleaned_uci_df['state'] = uci_df['state'].apply(clean_state)
    cleaned_uci_df['latitude'] = uci_df['latitude'].apply(clean_latitude)
    cleaned_uci_df['longitude'] = uci_df['longitude'].apply(clean_longitude)
    cleaned_uci_df['source'] = uci_df['source'].apply(clean_source)
    cleaned_uci_df['time'] = uci_df['time'].apply(clean_time)
    return cleaned_uci_df
