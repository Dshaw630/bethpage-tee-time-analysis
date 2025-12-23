# Thought Process / Lab Notebook

## Day 1 – Setup and system learning
- learned more about using github desktop, git repo workflow and actions
- added Python 3.11 and created a new venv in pycharm to organize project
- added packages below:
    - numpy
    - pandas
    - matplotlib
    - seaborn
    - plotly
    - jupyter
    - ipykernel
    - python-dotenv
    - openpyxl
- added local Pycharm kernel to jupyter, made first jupyter nb

## Day 2 - README Work
- Gathered some more supporting documentation
- Worked on the background and motivation section of README
- learned about markdown formatting

## Day 3 - README Work
- Finished bones of README and polished some prose 
- started working on extracting data from Excel sheets to pandas DF

## Day 4 & 5 - Data intake and cleaning
- developed data cleaning pipeline to iterate through all .xlsx files in directory which represent years of data
- for each .xlsx iterate collect tabs which represent quarters into a list
- clean and filter each quarter df based on shape, validity of data, etc.
- stick all quarters together, and put full year df in list, repeat for all years
- stick all years into one master df
- cleaned up initial attempt to improve readability and move some repeated actions to a function

## Day 6-10 - data intake and cleaning - details column 
- finalized some intake and filtering tweaks, standardizing column name format, etc. 
- started working on data cleaning
  - need to convert start (tee time) to datetime - complete
  - need to extract booking time from details (will need year from start to complete datetime format) - complete
    - regex to strip out time info after "@", maybe some helper columns and then concat?
    - N.B.!!! need to be aware of tee times booked in dec for early jan when converting to datetime
    - QA checks
      - log how many rows fail regex extraction and are dropped
      - check that all dates in booking time are in valid ranges
      - log now many rows fail booking time conversion to datetime


## intake and cleaning todo  
  - standardize status column to a binary(?) or at least more discrete set of values
  - drop booking source? seems useless
  - clean course and round length (9 or 18 holes) out of tee sheet
    - some are specially formatted as "x course 9 hole early", early distinction may be relevant here
  - clean up majority of NaT values from cancellation time