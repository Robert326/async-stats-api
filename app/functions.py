import pandas as pd
import numpy as np
import json
import os

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

def best5_request(data, df, questions_best_is_min, questions_best_is_max):
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

def worst5_request(data, df, questions_best_is_min, questions_best_is_max):
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
    filtered_df = df[(df["Question"] == question) &
                     (df["Year"] >= 2011) & (df["YearEnd"] <= 2022)]
    
    # Calculez media pentru fiecare stat
    state_means = filtered_df.groupby("State")["Value"].mean().reset_index()
    state_means.columns = ["State", "Mean"]

    # Calculez global_state_mean ca fiind media mediei per stat
    global_state_mean = state_means["Mean"].mean()
    state_means["DiffFromGlobal"] = global_state_mean - state_means["Mean"]

    state_means = state_means.sort_values(by="DiffFromGlobal", ascending=False)
    
    result_dict = dict(zip(state_means["State"], state_means["DiffFromGlobal"]))
    
    return result_dict

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
    
    grouped = filtered_df.groupby(["State", "StratificationCategory1", "Stratification1"])["Value"].mean().reset_index()
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

    grouped = filtered_df.groupby(["StratificationCategory1", "Stratification1"])["Value"].mean().reset_index()
    grouped.columns = ["Category", "Segment", "Mean"]

    result_dict = {}
    for _, row in grouped.iterrows():

        key = str((row["Category"], row["Segment"]))
        result_dict[key] = row["Mean"]

    return {state: result_dict}