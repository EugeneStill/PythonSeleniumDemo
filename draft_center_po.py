# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


class DraftCenter(webdriver.Chrome):

    def __init__(self, driver):
        self.driver = driver
        self.divisions = [
                "AL West",
                "AL East",
                "NL West",
                "NL East",
                "AL Central",
                "NL Central"
            ]

    login_id_locator = "username"
    password_locator = "password"
    division_locator = "tn0"
    start_year_locator = "seasonmin"
    end_year_locator = "seasonmax"
    search_button_locator = "cmdSearch"
    no_match_locator = "nomatches"
    results_locator = "results_count"
    salary_locator = "salmin"
    sign_in_button_locator = "//button[contains(text(), 'Sign in')]"
    base_url = "https://www.whatifsports.com/mlb-l/themewiz_"
    draft_hitter_url = base_url + \
        "playersearch.asp?spot=9&spotfilled=0&themeid=-1&dtid=0&repid=0&dlcl=0&ft=0&cashleft=75200000&uwl=0&ubl=0"
    draft_pitcher_url = base_url + \
        "playersearch.asp?spot=21&spotfilled=0&themeid=-1&dtid=0&repid=0&dlcl=0&ft=0&cashleft=75200000&uwl=0&ubl=0"
    results = {}

    def get_sign_in_button(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.sign_in_button_locator)))
        return element

    def get_login_id(self):
        login = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.login_id_locator)))
        return login

    def get_password(self):
        password = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.password_locator)))
        return password

    def get_division(self):
        division = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.division_locator)))
        return division

    def get_start_year(self):
        start_year = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.start_year_locator)))
        return start_year

    def get_end_year(self):
        end_year = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.end_year_locator)))
        return end_year

    def get_search_button(self):
        search = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.search_button_locator)))
        return search

    def get_no_match(self):
        # return 0 if "no match" text is found or exception encountered
        try:
            no_match = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, self.no_match_locator)))
        except:
            print("Exception encountered while looking for no results text")
        return 0
    
    def get_results_count(self):
        # return number of results (first 2 positions of results_count text)
        results_count = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.ID, self.results_locator)))
        return int(results_count.text[:2])

    def get_results(self):
        try:
            results = self.get_results_count()
        except Exception:
            results = self.get_no_match()
        return results

    def get_salary(self):
        salary = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, self.salary_locator)))
        return salary

    def login(self, user, password):
        time.sleep(1)
        self.get_login_id().send_keys(user)
        time.sleep(1)
        self.get_password().send_keys(password)
        time.sleep(1)
        self.get_sign_in_button().click()
        time.sleep(5)
        return

    def select_year(self, year):
        # sets the start year and end year to the same value so we only get results for that year
        start_year = self.get_start_year()
        start_select = Select(start_year)
        start_select.select_by_visible_text(str(year))

        end_year = self.get_end_year()
        end_select = Select(end_year)
        end_select.select_by_visible_text(str(year))
        return

    def select_divison(self, division_name):
        division = self.get_division()
        division_select = Select(division)
        division_select.select_by_visible_text(division_name)

    def select_salary(self, salary_amount):
        salary = self.get_salary()
        salary_select = Select(salary)
        salary_select.select_by_visible_text(salary_amount)

    def get_result_dict(self, pitcher_salary, hitter_salary):
        # set pitchers salary and call method to update dict with pitcher results
        self.driver.get(self.draft_pitcher_url)
        self.select_salary(pitcher_salary)
        self.update_result_dict('pitchers')
        # set hitters salary and call method to update dict with pitcher results
        self.driver.get(self.draft_hitter_url)
        self.select_salary(hitter_salary)
        self.update_result_dict('hitters')
        return self.results

    def update_result_dict(self, position):
        for year in range(1969, 2019):
            self.select_year(year)
            # Set number_of_divisions based on year.  In 1993 MLB expanded from 4 divisions to 6 divisions.
            if year >= 1993:
                number_of_divisions = 6
            else:
                number_of_divisions = 4
            for i in range(number_of_divisions):
                self.select_divison(self.divisions[i])
                self.get_search_button().click()
                # set dict_key value, get or set up dict for that key & update results
                dict_key = str(year) + " " + self.divisions[i]
                self.results[dict_key] = self.results.get(dict_key, {})
                self.results[dict_key][position] = self.get_results()
        return