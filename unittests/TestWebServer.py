import unittest
import json
import pandas as pd

from app import webserver
from app.functions import (
    states_mean_request, state_mean_request, best5_request,
    worst5_request, global_mean_request, diff_from_mean_request,
    state_diff_from_mean_request, mean_by_category_request, state_mean_by_category_request
)

class TestWebServer(unittest.TestCase):

    def setUp(self):
        # Load the CSV file into a DataFrame
        self.df = pd.read_csv("./nutrition_activity_obesity_usa_subset.csv")
        self.df.rename(columns={
            "YearStart": "Year",
            "LocationDesc": "State",
            "Data_Value": "Value",
        }, inplace=True)

        # Create a mock webserver instance
        self.df2 = pd.read_csv("./unittests_values.csv")
        self.webserver = webserver
        self.webserver.data_ingestor.df = self.df
        self.app = self.webserver.test_client()
        self.app.testing = True
    
    def test_states_mean_calculation(self):
        data = {
            "question": "Percent of adults aged 18 years and older who have an overweight classification"
        }
        result = states_mean_request(data, self.df)
        expected = 33.25753424657535
        self.assertEqual(result["Ohio"], expected)

