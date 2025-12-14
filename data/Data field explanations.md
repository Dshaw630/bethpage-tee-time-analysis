# Explanation of Dataset Columns
## Start
This is the tee time date and time in MM/DD/YYYY HH:MM (military time)
## Details
this has the booking method, booking time, number of players, and cost. Although, Most of these columns exist in other 
cleaner columns. The main useful info here is the booking time and date in H:MM AM/PM MM/DD. There is some slight 
variability in formatting but the useful date always follows "@"

## Status Text
This is the end result of the booking with the values deleted (canceled), blank (presumably a no-show), checked - in, 
teed off (these last two seem confusing, there are about 3.4k checked in vs 2.2k teed off, seems like they should 
represent the same end result of a customer playing their round)

## Booking Source
always has the value online, seems like this is not useful as the data requested was online bookings. Likely exists 
because Bethpage reserves some time slots for walk up players

## Player Count
The number of players on the booking. Seems to always match the redundant data in details

## Tee Sheet
Which course the booking is for, some additional data as far as special promotional times of day like "Bethpage 9 Holes
Midday Back 9". Could be useful for identifying 9 holes vs 18 holes

## Date Cancelled
If the status text is canceled, the time and date it was canceled in MM/DD/YYYY HH:MM (military time). May be useful to 
ID cancellations close to scheduled tee time which may indicate automation
