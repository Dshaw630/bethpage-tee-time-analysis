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

## Day 6-13 - data intake and cleaning - details column 
- finalized some intake and filtering tweaks, standardizing column name format, etc. 
- started working on data cleaning
- - dropped booking source as it only listed "online" which is not valuable here as the FOIL request only covered online data
  - need to convert start (tee time) to datetime - complete
  - need to extract booking time from details (will need year from start to complete datetime format) - complete
    - regex to strip out time info after "@", maybe some helper columns and then concat?
    - N.B.!!! need to be aware of tee times booked in dec for early jan when converting to datetime
    - QA checks
      - log how many rows fail regex extraction and are dropped
      - check that all dates in booking time are in valid ranges
      - log now many rows fail booking time conversion to datetime
  - standardize status column to a binary(?) or at least more discrete set of values - complete
    - "checked in" and "teed off" both seemingly represent a player showing up to the course and almost certainly playing.
    "teed off" is much less frequent relative to "checked in" so it is possible this is an inconsistency in how staff use the 
    booking software.
      - The two statuses will be merged into "played"
    - Seems likely that "NAN" values are no-shows given that they do not seem to occur on tee times that were cancelled. 
    this can't be proven with the data at hand so "NAN" will be coerced to "unknown"
    - reword "deleted" as "cancelled" for clarity
    - QA checks
      - confirm that the size of the df was not altered 
      - confirm that no rows are both "played" and have a cancellation time,
      nor "cancelled" without a time listed
  - Clean number of players column, some values >4 exist - complete
    - invalid values exist in raw data, but upon inspection the details column for each row has a valid player count 
    within the string. 
    - extracted correct values from details, compare to player_count, and reconcile valid data out of these two
    - - dropped player_count and helper columns to clean up df
    - QA checks
      - count % of rows with mismatches and report how many were cleaned from raw data
      - count % of rows with mismatches after cleaning which have no valid data to extract, decided to drop as only two 
      were found
  - clean course and round length (9 or 18 holes) out of tee sheet
    - will clean 9/18 holes and course name out of tee_sheet via regex
    - will ignore "early am", etc. and define a more global schema to categorize all records based on time of day and 
    weekday/weekend
    - QA checks
      - count % of rows with no course in raw data, correspond to Bethpage 9 Holes Midday Front 9 / Bethpage 9 Holes Midday Back 9
      - count % of rows were 18 holes was assumed in the absence of an explicit value in raw data
      - count % of rows with invalid tee times 5AM or after 8PM
      - print crosstab table to verify time of day bins are working right
  - Exported to parquet for analysis, and a 50k row random sample to CSV for documentation and github readability
  - converted time_of_day, time_of_week, and status to categorical columns to save memory

  

  