# Overview
The raw data represent an export of tee times and booking data at the Bethpage state park from 2021-2025. In the cleaned 
dataset one row represents one booked tee time and lists relevant data associated with that tee time

# Final Dataset Summary
- 616,013 rows
- 12 Columns
- Individual users cannot be identified via this dataset as it lacks any unique identifiers

# Data Dictionary
| Column               | Description                                                                          | Data Type  |
|----------------------|--------------------------------------------------------------------------------------|------------|
| tee_time             | The scheduled tee time for each booking                                              | datetime64 |
| booking_time         | The time at which the user reserved the booking                                      | datetime64 |
| status_text          | The end state of the booking, played/cancelled/unknown                               | category   |
| date_cancelled       | The time at which a cancelled tee time was cancelled by the user                     | datetime64 |
| time_of_week         | Classifies bookings as weekday/weekend to investigate behavioral differences         | category   |
| time_of_day          | Classifies bookings as morning/midday/evening to investigate behavioral differences  | category   |
| player_count_final   | The number of players on the booking                                                 | int64      |
| course               | Which course at Bethpage the booking is for                                          | string     |
| round_length         | Identifies 9 hole or 18 hole round                                                   | int64      |
| cost_per_group       | The cost due by the group at check-in                                                | int64      |
| invalid_cancellation | Boolean flag for rows with "cancelled" in status_text but no value in date_cancelled | boolean    |
| invalid_tee_time     | Boolean flag for rows with tee time before 5am or after 8pm                          | boolean    |

# Cleaning & Validation decisions
## General cleaning
  - Forced all column names to lowercase
  - replaced all spaces in column names to underscore
  - stripped out extra spaces from column names
## Column specific cleaning
  - tee_time
    - Converted from string to datetime. Flagged about 50 tee times before 5am or after 8pm because these times are not 
    likely valid start times for a several-hour-long round of golf
    - Renamed from "Start" in raw data
  - booking_time
    - Extracted from details column via regex
      - utilized some helper columns to segregate day, month, year, hour, minute and perform some sanity checks that all values
      were in their acceptable ranges
      - converted extracted and checked helper cols to datetime
    - checked for any failed conversions to datetime to make sure it is small 
    - dropped any failed rows as booking_time is critical to analysis
  - status_text
    - converted to a categorical variable by coercing all values into either played, cancelled, or unknown
  - date_cancelled
    - converted from string to datetime
    - checked if any rows listed "cancelled" in status_text, but did not have a cancellation time listed
      - found about 800 and validated that these same 800 exist in the raw data
      - flagged to exclude these rows from some analyses, but did not drop 
  - time_of_week
    - bucketed weekend/weekday based on day of week attribute built into tee_time datetime
  - time_of_day
    - bucketed morning/midday/evening based on hour attribute built into tee_time datetime
      - morning = before 11, afternoon = between 11 and 4, evening = after 4
      - checked number of tee times outside valid hours
      - printed crostab table to make sure buckets were logical and workign correctly
  - player_count_final
    - Noticed some player_count values in the raw data as high as 54 players. Also noticed that details had more reasonable values
    - extracted player count from details, and wherever player_count was not a valid number between 1 and 4, used the extracted
    value from details
    - renamed corrected column player_count_final
    - dropped original player_count and player_count_regex helper column
  - course
    - extracted from tee_sheet via regex
    - checked percentage of courses that did not have a valid course value and were assigned 'unkown'
  - round_length
    - extracted from tee_sheet via regex where 9 hole was mentioned
    - any rows without an explicit length mentioned (e.g. tee_sheet listed "Bethpage Blue") were assumed to be 18 holes
    - checked percentage of rows assumed to be 18 hole rounds
  - cost_per_group
    - extracted from details column via regex
    - allowed NAN values as this is not critical to analysis, just an extra value that happened to be in the raw data
  - invalid_cancellation
    - flagged true/false for any rows where status_text is "cancelled" but no cancellation time is listed
  - invalid_tee_time
    - flagged true/false for any rows where tee_time is before 5am or after 8pm
  - booking_source
    - dropped from the dataset as it did not provide any useful information. Only online bookings were requested, so each 
    row listed "online"
  - player_count
    - dropped after validating acceptable number of players and consolidating into player_count_final
  - details
    - text string containing booking time, player count, and cost per group
    - dropped after extracting and validating useful info to separate columns
  - tee_sheet
    - listed course and potentially special booking promotional programs like early am 9 hole, etc.


