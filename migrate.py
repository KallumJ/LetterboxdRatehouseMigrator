import argparse
import csv
import os

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored

TIMEOUT = 5
MIGRATIONS = ["ratings", "watchlist"]


def main():
    os.system('color')

    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("--letterboxd_data", help="The path to your exported Letterboxd data. Required.", required=True)
    parser.add_argument("--username", help="Your ratehouse username/email. Required.", required=True)
    parser.add_argument("--password", help="Your ratehouse password. Required.", required=True)
    parser.add_argument("--migration", help="The type of migration to run", required=True, choices=MIGRATIONS)

    args = parser.parse_args()

    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()

    sign_in(driver, args.username, args.password)

    if args.migration == "ratings":
        migrate_ratings(driver, args.letterboxd_data)
    elif args.migration == "watchlist":
        migrate_watchlist(driver, args.letterboxd_data)


def migrate_watchlist(driver, letterboxd_data):
    watchlist = parse_watchlist(letterboxd_data + "/watchlist.csv")

    # for wish in watchlist:


def migrate_ratings(driver, letterboxd_data):
    ratings = parse_ratings(letterboxd_data + "/ratings.csv")

    failed = []
    # For each movie
    for rating in ratings:
        try:
            search_movie(driver, rating["movie_name"])
        except NoSuchElementException:  # If no result is found, add it to the failed list
            failed.append(rating)
            continue

        # Click the appropriate rating button
        rating_form = get_or_wait_for_element(driver, By.ID, "rating-input")
        rating_buttons = rating_form.find_elements(By.XPATH, "*")

        for button in rating_buttons:
            if button.get_attribute("value") == rating["rating"]:
                button.click()

    # Report failures
    print(colored(f"Successfully migrated ratings with {len(failed)} failures!", "green"))
    if len(failed) > 0:
        print(colored("Failed to set these movies ratings:", "red"))
        for fail in failed:
            print(colored(f"{fail['movie_name']}", "yellow"))


def search_movie(driver, query):
    # Search for movie
    search_bar = driver.find_element(By.NAME, "searchTerms")
    search_bar.send_keys(query)
    result = get_or_wait_for_element(driver, By.CSS_SELECTOR, ".see-all")
    result.click()

    # Get the movie category of results
    categories = driver.find_elements(By.CSS_SELECTOR, ".relations-box")
    movies_category = categories[2]

    # Find matching result
    results = movies_category.find_elements(By.TAG_NAME, "a")
    found = None
    for result in results:
        if result.get_attribute("innerHTML") == query:
            found = result

    # If a result is found, click it
    if found:
        found.click()
    else:
        raise NoSuchElementException


def parse_ratings(path):
    ratings = []
    with open(path, "r", encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            movie_name = row[1]
            rating = row[4]

            if not movie_name == "Name":
                ratings.append({"movie_name": movie_name, "rating": rating})

    return ratings


def parse_watchlist(path):
    watchlist = []
    with open(path, "r", encoding="UTF-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            watchlist.append({"movie_name": row[1]})

    return watchlist


def sign_in(driver, username, password):
    # Navigate to rate house sign in page
    driver.get("https://rate.house/signin")

    # Enter username and password
    username_field = driver.find_element(By.ID, "signin-username")
    password_field = driver.find_element(By.ID, "signin-password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Sign in
    signin_button = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/form/button")
    signin_button.click()
    get_or_wait_for_element(driver, By.CSS_SELECTOR, ".featured")  # Wait for sign in redirect


def get_or_wait_for_element(driver, by, selector):
    return WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((by, selector)))


if __name__ == "__main__":
    main()
