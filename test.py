from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import TimeoutException
import re

# options = Options()
# options.headless = True

driver = webdriver.Firefox()
driver.get("https://www.khanacademy.org/math/ap-statistics/analyzing-categorical-ap")
driver.wait = WebDriverWait(driver, 10)

# quiz botton: div._1o51yl6:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(3)
# double multiple choice: ._16c6bd9 > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > button:nth-child(1)
# long numbers multiple choice: div._1c8c7sfc:nth-child(5) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > button:nth-child(1)

# find quiz or practice button on unit main page, scroll to it, and click it
quiz_button = driver.wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            "div._1c8c7sfc:nth-child(5) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > button:nth-child(1)",
        )
    )
)
driver.execute_script("arguments[0].scrollIntoView(false);", quiz_button)
time.sleep(0.5)
quiz_button.click()
# quiz_button.click()

# find the start quiz or practice button and click it once loaded
start_quiz_button = driver.wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "._17h9ppyt",))
)
start_quiz_button.click()

# wait until the text elements on the problem are loaded
paragraphs = driver.wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "paragraph",))
)

# test to see if the question is multiple choice or free response
# if the multiple choice answers do not load within 10 seconds then it is assumed to be a free response question
try:
    driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_vq37gq",)))
except TimeoutException:
    print("not multiple choice")

# TODO find xpath for answers by ignoring certain elements that have duplicate text
# find all mulitple choice answer elements
answers = driver.find_elements_by_xpath(
    "//div[@class='checkbox-and-option _tqugjn']//span[@class='perseus-radio-option-content perseus-interactive']"
)

# convert all answers into text and add them to one list
answer_list = []
for answer in answers:
    answer_list.append(answer.text)

# use regex to clean up answers
answer_list = [
    # match the format of \n4\n4\n or 4\n4\n for example
    re.sub(r"(\n?)(\d+)(\n)(\d+)(\n+)", r"\2 ", answer)
    for answer in answer_list
]


# answer_list = [
#     re.sub(r"\n((*?)(\d+)(*?)(\d*))\n", r" \1 ", answer) for answer in answer_list
# ]
# add spaces after commas
answer_list = [re.sub(r",", r", ", answer) for answer in answer_list]

print(answer_list)
print("\nALL TEXT BELOW\n")

# for paragraph in paragraphs:
#     print(paragraph.text)
# driver.quit()
