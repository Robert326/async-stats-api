import pandas as pd
import numpy as np

def states_mean_request(data, df):
    """
    Calculate the mean of the given questions for each state.
    
    Args:
        data (dict): A dictionary containing the list of questions.
        df (pd.DataFrame): The DataFrame containing the data.
    """

    question = data["question"]
    
    # filter by questions and years
    filtered_df = df[(df["Question"] == question) & 
                     (df["Year"] >= 2011) & 
                     (df["YearEnd"] <= 2022)]
    
    # group by state and calculate mean
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # sort ascending by mean
    result = result.sort_values(by="Mean", ascending=True)

    result_dict = dict(zip(result["State"], result["Mean"]))

    return result_dict

def state_mean_request(data, df):
    """
    Calculate the mean of the given questions for a specific state.
    
    Args:
        data (dict): A dictionary containing the list of questions and the state.
        df (pd.DataFrame): The DataFrame containing the data.
    """

    question = data["question"]
    state = data["state"]
    
    # filter by questions and years
    filtered_df = df[(df["Question"] == question) & 
                     (df["State"] == state) & 
                     (df["Year"] >= 2011) & 
                     (df["YearEnd"] <= 2022)]
    
    # group by state and calculate mean
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    result_dict = dict(zip(result["State"], result["Mean"]))

    return result_dict

def best5_request(data, df, questions_best_is_min):
    """
    Calculate the mean of the given questions for each state and return the top 
    5 states.

    Args:
        data (dict): A dictionary containing the list of questions.
        df (pd.DataFrame): The DataFrame containing the data.
    """

    question = data["question"]
    
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & 
                     (df["YearEnd"] <= 2022)]
    
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    if question in questions_best_is_min:
        result = result.sort_values(by="Mean", ascending=True)
    else:
        result = result.sort_values(by="Mean", ascending=False)

    top5 = result.head(5)

    result_dict = dict(zip(top5["State"], top5["Mean"]))

    return result_dict

def worst5_request(data, df, questions_best_is_min):
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                        (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    if question in questions_best_is_min:
        result = result.sort_values(by="Mean", ascending=False)
    else:
        result = result.sort_values(by="Mean", ascending=True)

    top5 = result.head(5)

    result_dict = dict(zip(top5["State"], top5["Mean"]))

    return result_dict

def global_mean_request(data, df):
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    mean_value = filtered_df["Value"].mean()
    return {"global_mean": mean_value}

def diff_from_mean_request(data, df):
    question = data["question"]

    # Obținem lista de state unice din datele filtrate
    filtered_df = df[df["Question"] == question]
    states = filtered_df["State"].unique()

    # Inițializăm un dicționar pentru a stoca diferențele
    diffs = {}

    # Parcurgem fiecare stat și calculăm diferența folosind state_diff_from_mean_request
    for state in states:
        state_data = {'question': question, 'state': state}
        diff = state_diff_from_mean_request(state_data, df)
        diffs.update(diff)  # Adăugăm diferența în dicționar

    sorted_diffs = dict(sorted(diffs.items(), key=lambda item: item[1], reverse=True))

    return sorted_diffs



def state_diff_from_mean_request(data, df):
    question = data["question"]
    state = data["state"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    global_mean = filtered_df["Value"].mean()
    state_mean = filtered_df[filtered_df["State"] == state]["Value"].mean()

    return {
        state: global_mean - state_mean
    }

def mean_by_category_request(data, df):
    question = data["question"]
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]

    grouped = filtered_df.groupby(["State", "StratificationCategory1",
                                   "Stratification1"])["Value"].mean().reset_index()
    grouped.columns = ["State", "Category", "Segment", "Mean"]

    result_dict = {}
    for _, row in grouped.iterrows():
        key = str((row['State'], row['Category'], row['Segment']))
        result_dict[key] = row["Mean"]

    return result_dict

def state_mean_by_category_request(data, df):
    question = data["question"]
    state = data["state"]
    filtered_df = df[
        (df["Question"] == question) &
        (df["Year"] >= 2011) & (df["YearEnd"] <= 2022) &
        (df["State"] == state)
    ]

    grouped = filtered_df.groupby(["StratificationCategory1",
                                   "Stratification1"])["Value"].mean().reset_index()
    grouped.columns = ["Category", "Segment", "Mean"]

    result_dict = {}
    for _, row in grouped.iterrows():

        key = str((row["Category"], row["Segment"]))
        result_dict[key] = row["Mean"]

    return {state: result_dict}