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

