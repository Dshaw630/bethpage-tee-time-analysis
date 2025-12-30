import pandas as pd
import glob
import os
import re
import numpy as np


#set display preferences in Jupyter Notebook
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

#gather all absolute file paths in raw data folder and place them in a list
def get_files():
    raw_data_path = os.path.abspath(os.path.join(os.getcwd(),".."))
    pattern = os.path.join(raw_data_path,"data","raw","*.xlsx")
    file_list = glob.glob(pattern)
    return file_list

#clean and filter data raw to acceptable parameters
def get_valid_quarters(quarter_df_lst):
    #strip and force lowercase on all, force single "_" between words 
    for q in quarter_df_lst:
        q.columns = q.columns.str.lower()
        q.columns = q.columns.str.strip()
        q.columns = q.columns.str.replace('\\s+', '_', regex=True)
    #filter out any sheets with less than 5 rows
    length_check = [val for val in quarter_df_lst if len(val) > 5]
    #filter out sheets without expected cols
    required_cols = {"start","details","status_text","booking_source","player_count","tee_sheet","date_cancelled"}
    col_check = [val for val in length_check if required_cols.issubset(set(val.columns))]
    #filter out sheets with more than 10% NA values on the start time
    valid_start_time = [val for val in col_check if val["start"].isna().mean() < 0.10]
    valid_quarters = valid_start_time
    return valid_quarters

#for each file, collect each tab into a dict w/ tab name as key, df of data as value. concat all tabs into a full year df
def get_raw_data():
    year_dfs = []
    file_lst = get_files()
    for file in file_lst:
        quarter_dict = pd.read_excel(file,sheet_name=None)
        quarters = list(quarter_dict.values())
        quarters = get_valid_quarters(quarters)
        if quarters:
            year = pd.concat(quarters)
            year_dfs.append(year)
        else:
            print(f"'{os.path.basename(file)}': no valid data")

    #concat all year dfs into one master df
    master_raw = pd.concat(year_dfs,ignore_index=True)
    return master_raw

def clean_data(master_raw):
    #basic cleaning, convert start to datetime, drop booking_source (provides no meaningful input here), rename start to tee_time for clarity
    #convert cancellation time to datetime
    master_df = master_raw.copy()
    master_df["start"] = pd.to_datetime(master_df["start"])
    master_df.drop(columns=["booking_source"],inplace=True)
    master_df.rename(columns={"start":"tee_time"},inplace=True)
    master_df["date_cancelled"] = pd.to_datetime(master_df["date_cancelled"],errors="coerce")

    #clean time, date, and cost out of details column using regex,drop any rows that extract time data to nan
    master_df[["book_hr","book_min","am_pm","book_month","book_day","cost_per_group"]] = master_df["details"].str.extract(r"@\s(\d{1,2}):(\d{2})(am|pm|AM|PM|Am|Pm)\s(\d{1,2})\/(\d{1,2})(?:.*?\$(\d+\.\d{2}))?")
    master_df.dropna(subset=["book_hr","book_min","am_pm","book_month","book_day"],inplace=True)
    master_df[["book_hr","book_min","book_month","book_day"]] = master_df[["book_hr","book_min","book_month","book_day"]].astype(int)
    master_df["cost_per_group"] = pd.to_numeric(master_df["cost_per_group"], errors="coerce")

    #reformat book time to 24hr to enable cleaning
    master_df.loc[(master_df["am_pm"] == "pm")&(master_df["book_hr"] != 12), "book_hr"] = master_df.loc[(master_df["am_pm"] == "pm")&(master_df["book_hr"] != 12), "book_hr"]+12
    master_df.loc[(master_df["book_hr"] == 12) & (master_df["am_pm"] == "am"), "book_hr"] = 0

    # pull year from tee_time column, adjust booking time column value to previous year if booking in dec and tee time in jan
    master_df["book_yr"] = master_df["tee_time"].dt.year
    master_df.loc[(master_df["tee_time"].dt.month == 1)&(master_df["book_month"] == 12),"book_yr"] = master_df.loc[(master_df["tee_time"].dt.month == 1)&(master_df["book_month"] == 12),"book_yr"]-1

    #convert cleaned booking_time column data to datetime
    master_df["booking_time"] = pd.to_datetime(
        {
            "year": master_df["book_yr"],
            "month": master_df["book_month"],
            "day": master_df["book_day"],
            "hour": master_df["book_hr"],
            "minute": master_df["book_min"],
        },
        errors="coerce",
    )
    bad_book_time = master_df.index[master_df["booking_time"].isna()]
    master_df.drop(bad_book_time,inplace=True)

    #drop helper date columns to clean up df, reorganize cols
    master_df.drop(columns=["book_hr","book_min","am_pm","book_month","book_day", "book_yr"],inplace=True)
    master_df = master_df[['tee_time', 'details', 'booking_time', 'status_text', 'player_count', 'tee_sheet',
           'date_cancelled', 'cost_per_group']]

    #drop any rows where booking time occurs after tee time. No clear explanation for this upon analysis so it will be treated as noise
    bad_time_order = master_df.index[master_df["booking_time"] > master_df["tee_time"]]
    qa_bad_time_order_count = len(bad_time_order)
    master_df.drop(bad_time_order,inplace=True)

    #Adjust and collapse status_text values based to a discrete set. collapse "checked in" and "teed off" to "played",
    # reword deleted to cancelled for clarity,coerce NAN to unknown
    master_df.loc[(master_df["status_text"] == "checked in")|(master_df["status_text"] == "teed off"),"status_text"] = "played"
    master_df.loc[master_df["status_text"] == "deleted","status_text"] = "cancelled"
    master_df.loc[master_df["status_text"].isna(),"status_text"] = "unknown"

    #flag cancelled rows w/o a cancellation time listed
    master_df["invalid_cancellation"] = (master_df["status_text"]=="cancelled")&(master_df["date_cancelled"].isna())
    qa_bad_cancellation_count = len(master_df.loc[master_df["invalid_cancellation"] == True])

    #extract player counts from details column and reconcile extracted player count and player_count to yield 1-4 or NA, drop any NA
    master_df["player_count_regex"] = master_df["details"].str.extract(r"([1-4])\s+Players?").astype(float)
    master_df["player_count_final"] = master_df["player_count"]
    master_df.loc[(master_df["player_count_final"]!=master_df["player_count_regex"])&(master_df["player_count_regex"].notna()),"player_count_final"] = master_df["player_count_regex"]
    bad_player_count_index = master_df.loc[(master_df["player_count_final"]<1)|(master_df["player_count_final"]>4)|(master_df["player_count_final"].isna())].index
    master_df.drop(bad_player_count_index,inplace=True)

    #drop native player_count column (exists in raw df still) and regex helper column to clean up df
    master_df.drop(columns=["player_count","player_count_regex"],inplace=True)

    #clean course name out of tee_sheet and assign "unknown" to rows without course names
    master_df["course"] = master_df["tee_sheet"].str.extract(r"\b(black|red|blue|green|yellow)\b",flags = re.IGNORECASE, expand = True)
    master_df.loc[master_df["course"].isna(),"course"] = "unknown"

    #clean round length (9 or 18 holes) out of tee_sheet. Assume any non-9 hole round is 18 because 18 is never explicitly stated in the data
    master_df["round_length"] = master_df["tee_sheet"].str.extract(r"(?:\b(9)\s*holes?\b)",flags = re.IGNORECASE, expand = True)
    master_df.loc[master_df["round_length"].isna(),"round_length"] = 18
    master_df["round_length"] = master_df["round_length"].astype(int)

    #categorize weekend/weekday and time of day to ensure these data are not lost when dropping tee_sheet
    master_df["week_day"] = master_df["tee_time"].dt.weekday
    master_df["time_of_week"] = np.where(master_df["week_day"]>=5,"weekend","weekday")
    hours = master_df["tee_time"].dt.hour
    master_df["time_of_day"] = pd.cut(
        hours,
        bins=[-1, 10, 15, 23],
        labels=["morning", "midday", "evening"])

    #add flag for invalid tee times after 8PM and before 5AM
    master_df["invalid_tee_time"] = (master_df["tee_time"].dt.hour<5)|(master_df["tee_time"].dt.hour>19)
    qa_bad_time_of_day_count = len(master_df.loc[master_df["invalid_tee_time"]==True])

    #drop tee_sheet column after data extraction
    master_df.drop(columns=["tee_sheet","week_day"],inplace=True)

    #final cleanup
    master_df = master_df[['tee_time', 'booking_time', 'status_text', 'date_cancelled','time_of_week', 'time_of_day','player_count_final','course',
                           'round_length','cost_per_group', 'invalid_cancellation', 'invalid_tee_time']]
    master_df["time_of_week"] = master_df["time_of_week"].astype("category")
    master_df["status_text"] = master_df["status_text"].astype("category")
    master_df["time_of_day"] = pd.Categorical(master_df["time_of_day"],categories=["morning", "midday", "evening"],ordered=True)

    qa_dict = {
        "qa_bad_time_order_count" : qa_bad_time_order_count,
        "qa_bad_time_of_day_count" : qa_bad_time_of_day_count,
        "qa_bad_cancellation_count" : qa_bad_cancellation_count,
    }

    return master_df,qa_dict

def qa_summary(master_df, qa_dict):
    print("QA Summary:")
    print(f"\tRows x Cols:{master_df.shape}")
    min_tee_time = master_df["tee_time"].min()
    max_tee_time = master_df["tee_time"].max()
    print(f"\ttee_time range:{min_tee_time} to {max_tee_time}")
    print("\nSchema check:")
    print(master_df[["tee_time","booking_time","date_cancelled","time_of_day","time_of_week","status_text"]].dtypes)
    print("\nInvalid data checks:")
    print(f"\tbooking_time > tee_time: {qa_dict['QA_bad_time_order_count']} rows ({(qa_dict['QA_bad_time_order_count'] / len(master_df)):.4%})")
    print(f"\ttee time before 5am or after 8pm: {qa_dict['QA_bad_time_of_day_count']} rows ({(qa_dict['QA_bad_time_of_day_count'] / len(master_df)):.4%})")
    print(f"\trow listed as cancelled, but no cancellation time is listed: "
          f"{qa_dict['QA_bad_cancellation_count']} rows ({(qa_dict['QA_bad_cancellation_count'] / len(master_df)):.4%})")
    print("\nCategorical Variables Sanity Check:")
    print("Status text distribution:")
    print(master_df["status_text"].value_counts())
    print("\nTime of day distribution:")
    print(master_df["status_text"].value_counts())
    print("\nNumerical bounds check:")
    min_player_count = master_df["player_count_final"].min()
    max_player_count = master_df["player_count_final"].max()
    print(f"\tplayer_count range:{min_player_count} to {max_player_count}")
    print("\n---QA checks complete---")

#export cleaned data
def export(master_df):
    #define path and export parquet file
    processed_dir = os.path.join(os.getcwd(), "..", "data", "cleaned")
    os.makedirs(processed_dir, exist_ok=True)
    parquet_path = os.path.join(processed_dir,"bethpage_bookings_clean.parquet")
    master_df.to_parquet(parquet_path,index=False)

    #take a random sample of 50k rows to make a sample CSV for lighter review, no analysis will be done on this documentation purposes only
    sample_df = master_df.sample(n=50_000, random_state=42)
    processed_dir = os.path.join(os.getcwd(), "..", "data", "cleaned")
    os.makedirs(processed_dir, exist_ok=True)
    csv_path = os.path.join(processed_dir,"bethpage_bookings_clean_sample.csv")
    sample_df.to_csv(csv_path,index=False)

    #export quality QA
    reloaded = pd.read_parquet(parquet_path)
    assert len(reloaded) == len(master_df)
    assert reloaded.dtypes.equals(master_df.dtypes)

def main():
    master_raw = get_raw_data()
    master_df,qa_dict = clean_data(master_raw)
    qa_summary(master_df, qa_dict)
    export(master_df)

main()