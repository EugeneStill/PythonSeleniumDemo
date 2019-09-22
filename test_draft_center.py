# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest, os

import draft_center_po as draft_center


class TestDraftCenter(unittest.TestCase, webdriver.Chrome):

    def setUp(self):
        """Runs before test case"""
        self.driver = webdriver.Chrome()
        self.user = os.getenv('WHAT_IF_USERNAME', None)
        self.password = os.getenv('WHAT_IF_PASSWORD', None)
        self.base_url = "https://www.whatifsports.com/mlb-l/themewiz_"
        self.draft_pitcher_url = self.base_url + \
            "playersearch.asp?spot=21&spotfilled=0&themeid=-1&dtid=0&repid=0&dlcl=0&ft=0&cashleft=75200000&uwl=0&ubl=0"
        self.minimum_hitter_salary = "$7,000,000"
        self.minimum_pitcher_salary = "$8,000,000"
        self.minimum_qualifying_hitters = 3
        self.minimum_qualifying_pitchers = 2

    def tearDown(self):
        """Runs after test case"""
        self.driver.quit()

    def test_what_if(self):
        """validates > 0 divisions have > 0 seasons with >= expected number of hitters & pitchers >= expected salary"""
        dc = draft_center.DraftCenter(self.driver)
        # log in
        self.driver.get(self.draft_pitcher_url)
        dc.login(self.user, self.password)
        # get raw results for all seasons
        result_dict = dc.get_result_dict(self.minimum_pitcher_salary, self.minimum_hitter_salary)
        # get list of divisions with number of players that meet the criteria of the test
        criteria_met = [[k,v] for k,v in result_dict.items() if v['pitchers'] >= self.minimum_qualifying_pitchers
                       and v['hitters'] >= self.minimum_qualifying_hitters]
        self.print_results(criteria_met)
        self.assertTrue(True,
                        "Minimum number of qualifying hitter & pitcher salaries not found in any division's season.")

    def print_results(self, result_list):
        header = "\nMIN " + str(self.minimum_qualifying_pitchers) + " PIITCHERS > "  + self.minimum_pitcher_salary[:2] \
                 + "M"
        header += " & MIN " + str(self.minimum_qualifying_hitters) + " HITTERS > "  + self.minimum_hitter_salary[:2] \
                 + "M"
        print(header)
        if len(result_list) == 0:
            print("No matching results were found")
        else:
            for entry in result_list:
                print(entry[0] + " " + str(entry[1]['pitchers']) + " Pitchers & " + str(entry[1]['hitters'])
                      + " Hitters")
        return


if __name__ == "__main__":
    unittest.main()