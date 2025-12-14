# Bethpage State Park Tee Time Booking Automation Analysis
Analysis of Bethpage State Park tee-time data (2021–2025) focusing on the prevalence of automated booking abuse,
and the effectiveness of recent booking rule changes in reducing such behavior.

## Background & Motivation
This analysis is inspired by [episode 945 of the No Laying Up Podcast](https://nolayingup.com/podcasts/no-laying-up-podcast/945-nlu-special-projects-the-mystery-behind-why-bethpage-is-always-booked), 
in which Kevin Van Valkenburg investigates the seemingly herculean task of securing a tee time at Bethpage State Park. Bethpage is a public facility with five
18-hole golf courses, including the lauded Black Course, host to the 2025 Ryder Cup. As highlighted in the podcast,
one major contributor to the perpetual unavailability of these tee times is the deployment of automated booking
software by individuals and organized resellers. Such programs are able to secure large blocks of tee times fractions of
seconds after release time, before most users are able to load the booking web page. This dynamic has raised concerns about
equitable access and the operational integrity of the booking system.

In April 2025, a few months after the podcast aired, Bethpage announced booking policy changes designed to discourage
automated intervention in the booking process. These changes included a new booking fee, increased
no-show penalties, and monthly cancellation limits. The focus of this analysis is to evaluate the extent to
which automated booking activity may have influenced booking behavior prior to these rule changes, and to gauge their
effectiveness in discouraging system abuse.

It is important to note that shortly after the dataset was requested via a New York State FOIL request, Bethpage announced
a more robust set of rule changes set to take effect in October 2025. The centerpiece of this second policy update is the
implementation of two-factor authentication during the booking process, which will likely be much more, if not completely,
effective in stopping automated booking. A future FOIL request in the fall of 2026 could enable a follow-up analysis comparing
booking behavior across all three policy eras.

## Project Goals
- Quantify tee time inventory patterns at Bethpage State Park from 2021 to 2025
- Identify signals and patterns consistent with automated booking systems, including timing, volume, and cancellation behavior
- Compare booking behavior before and after the April 2025 rule changes
- Evaluate the impact of these rule changes on user behavior
- Establish a repeatable analysis framework to enable future analysis of the October 2025 rule change

## Current Status
- Data cleaning in process

## Data Source & Ethics
The data for this project were sourced from a New York State Freedom of Information Law request. The data are anonymized
listings of tee time inventory transactions. This analysis will make no attempt to identify individuals, and rather
cannot be used to do so, given the level of specificity provided.

