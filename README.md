# Semester Project

- [Instructions](#instructions)
- [Authors](#authors)
- [Data Source](#data-source)
- [Project Proposal](#project-proposal)
- [Directory Structure](#directory-structure)
- [Common Commands](#common-commands)
- [Bureau of Economic Analysis (BEA) API Key](#bureau-of-economic-analysis-bea-api-key)
- [Progress Report](#progress-report)

# Instructions

__________

You will complete a semester project.
The first step of the project is a Project Proposal.
See the PDF for instructions on creating your project proposal.

Project proposals are due ***Tuesday, September 23***.

You are expected to work in groups of 2-3.
You may work alone if your project is tied to an academic research project, or tied to work for an internship or job.
If your project is tied to work with an internship or job,
you must get permission from your employer to share your data for the purposes of grading,
and permission to present your results to the class.
You may also work alone for similar compelling reasons.
Groups may not be larger than 3.

All students must submit their own copy of the proposal on Canvas, including the names of your project partners.
If your group has 3 people in it, all 3 of you must submit a copy of the same proposal on Canvas.

https://sdsu.instructure.com/courses/187179/files/18135112?wrap=1

# Authors

__________
Isaia Pacheco

- Email
    - ipacheco9311@sdsu.edu
- Red ID
    - 819438016

Isaac Pacheco

- Email
    - ipacheco3354@sdsu.edu
- Red ID
    - 120448533

# Data Source

__________
"Apartment for Rent Classified." UCI Machine Learning Repository, 2019, https://doi.org/10.24432/C5X623.

"SARPP Real Personal Income, Real PCE, and Regional Price Parities by State." Bureau of Economic Analysis, 2019,
https://apps.bea.gov/iTable/?reqid=70&step=1&isuri=1&acrdn=4&_gl=1*5smdkb*_ga*ODc4NzEzMTExLjE3NjMzMzY3Nzg.*_ga_J4698JNNFT*czE3NjMzMzY3NzckbzEkZzEkdDE3NjMzMzczNzkkajU5JGwwJGgw#eyJhcHBpZCI6NzAsInN0ZXBzIjpbMSwyOSwyNSwzMSwyNiwyNywzMF0sImRhdGEiOltbIlRhYmxlSWQiLCIxMTAiXSxbIk1ham9yX0FyZWEiLCIwIl0sWyJTdGF0ZSIsWyIwIl1dLFsiQXJlYSIsWyJYWCJdXSxbIlN0YXRpc3RpYyIsWyItMSJdXSxbIlVuaXRfb2ZfbWVhc3VyZSIsIkxldmVscyJdLFsiWWVhciIsWyIyMDE5Il1dLFsiWWVhckJlZ2luIiwiLTEiXSxbIlllYXJfRW5kIiwiLTEiXV19

# Project Proposal

__________

- https://docs.google.com/document/d/12TCXoH94xUPD0hpUMPlKg9uXZ1I1V-cDOle3JsIMFkk/edit?usp=sharing

# Directory Structure

__________

- data/
    - Folder where data will live
- requirements.txt
    - File that maintains the dependencies
- source/
    - Folder where source code will live
    - project.ipynb
        - Main source of data science
            - Exploratory data analysis
            - Visualization
            - Fitting
            - Etc.
- .env
    - File that stores environment variables

# Common Commands

__________

- `pip freeze > requirements.txt`
- ` pip install -r requirements.txt`

# Bureau of Economic Analysis (BEA) API Key

__________
API calls are made to the BEA API via a wrapper class.
To use it, you must first register for an API key from [here](https://apps.bea.gov/api/signup/) by providing your name
and email address.
The key will be emailed to you.

Once you have received your BEA API key.

1. Create an unversioned text file in the repository root called `.env`

```
├── .env
├── README.md
├── requirements.txt
├── data/
└── source/
```

2. In the `.env` file, Create an environment variable `BEA_KEY` with your personal key i.e.

```
BEA_KEY=Your36DigitAPiKey
```

# Progress Report
__________
View Progress Report [here](https://docs.google.com/document/d/1Brqvj0mPTDfRLu50i3gCvDf3HdrsVv1lbN4VC6Q-RSk/edit?usp=sharing)