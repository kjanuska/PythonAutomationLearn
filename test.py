from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException
import re

# options = Options()
# options.headless = True

driver = webdriver.Firefox()
driver.get("https://www.khanacademy.org/math/ap-statistics/analyzing-categorical-ap")
driver.wait = WebDriverWait(driver, 10)


# find quiz or practice button on unit main page, scroll to it, and click it
buttons = {
    "double_mc": "._16c6bd9 > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > button:nth-child(1)",
    "long_numbers_mc": "div._1c8c7sfc:nth-child(5) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > button:nth-child(1)",
    "quiz": "div._1o51yl6:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(3)",
}

is_quiz = False


# use regex to clean up text
def clean_up(answers):
    # convert all answers into text and add them to one list
    answer_list = []
    for answer in answers:
        answer_list.append(answer.text)

    # ==============================================================================
    # match the format of \n4\n4\n or 4\n4\n for example and leave just the number
    re1 = (r"(\n?)(\d+)(\n)(\d+)(\n+)", r"\2 ")

    # remove newline from the beginning of katex number but leaving it at the end for re2 to work
    # ex. \n$50,00 --> $50,000
    re2 = (r"\n((.?)(\d+)(.*)(\d*))", r" \1 ")

    # remove redundant text that is between newline characters
    re3 = (r"\n(.+)\n", "")

    # add a space between numbers and letters
    re4 = (r"([a-zA-z])(\d)", r"\1 \2")

    # remove space between letter and period at the end of sentence
    re5 = (r"(.) \.", r"\1.")
    # ==============================================================================

    # simplify replacements using regex patterns defined earlier and abstraction here
    regexes = [re1, re2, re3, re4, re5]
    for regex in regexes:
        answer_list = [re.sub(regex[0], regex[1], answer) for answer in answer_list]

    return answer_list


def scrape_multiple_choice():
    # find all mulitple choice answer elements
    answer_text = driver.find_elements_by_xpath(
        "//div[@class='checkbox-and-option _tqugjn']//span[@class='perseus-radio-option-content perseus-interactive']"
    )
    answer_list = clean_up(answer_text)

    # find actual buttons for multiple choice answers
    # mc_answer_choices[0] = A, [1] = B, and so on
    mc_answer_choices = driver.find_elements_by_xpath(
        "//li[@class='_1qgxogtu perseus-radio-option']"
    )
    # loop through and select every answer out of all possible
    for index in range(0, len(mc_answer_choices)):
        mc_answer_choices[index].click()
        # use enter to submit answer because clicking didn't work
        driver.find_element_by_xpath("//div[@class='_64iw7hi']//button").send_keys(
            Keys.ENTER
        )
        # wait until popup appears and get text
        result = driver.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "._ljoq2o"))
        ).get_attribute("data-test-id")
        if "-correct" in result:
            print('The correct answer is "' + answer_list[index] + '"')
            driver.find_element_by_xpath("//div[@class='_64iw7hi']//button").click()
            break
        # click retry button if answer is wrong
        driver.find_element_by_xpath("//div[@class='_64iw7hi']//button").click()


def scrape_free_response():
    print("free response")


def choose_button(practice_type):
    if "quiz" in practice_type:
        global is_quiz
        is_quiz = True
    return buttons.get(practice_type, "None")


def intialize_problem(practice_type):
    select_button = driver.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, choose_button(practice_type),))
    )
    driver.execute_script("arguments[0].scrollIntoView(false);", select_button)
    time.sleep(0.5)
    select_button.click()
    if is_quiz:
        select_button.click()

    # find the start button and click it once loaded
    start_quiz_button = driver.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "._17h9ppyt",))
    )
    start_quiz_button.click()

    # wait until the text elements on the problem are loaded
    driver.wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "paragraph",))
    )

    # test to see if the question is multiple choice or free response
    # if the multiple choice answers do not load within 10 seconds then it is assumed to be a free response question
    try:
        driver.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "_vq37gq",))
        )
        scrape_multiple_choice()
    except TimeoutException:
        scrape_free_response()


intialize_problem("long_numbers_mc")
# print("\nALL TEXT BELOW\n")

# driver.quit()
