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
                     (df["Year"] <= 2022)]
    
    # group by state and calculate mean
    result = filtered_df.groupby("State")["Value"].mean().reset_index()
    result.columns = ["State", "Mean"]

    # sort ascending by mean
    result = result.sort_values(by="Mean", ascending=True)

    return result.to_dict(orient="records")

 