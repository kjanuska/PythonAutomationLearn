from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.common.exceptions import TimeoutException

# options = Options()
# options.headless = True

driver = webdriver.Firefox()
driver.get("https://www.khanacademy.org/math/ap-statistics/analyzing-categorical-ap")
driver.wait = WebDriverWait(driver, 10)

quiz_button = driver.wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
            "div._1o51yl6:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > button:nth-child(3)",
        )
    )
)
driver.execute_script("arguments[0].scrollIntoView(false);", quiz_button)
time.sleep(0.5)
quiz_button.click()
quiz_button.click()

start_quiz_button = driver.wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "._17h9ppyt",))
)
start_quiz_button.click()

paragraphs = driver.wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "paragraph",))
)

try:
    driver.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_vq37gq",)))
except TimeoutException:
    print("not multiple choice")

answers = driver.find_elements_by_xpath(
    "//div[@class='checkbox-and-option _tqugjn']/span[@class='perseus-radio-option-content perseus-interactive']"
)

# TODO: find text that contains duplicate numbers and newline characters, i.e. "4\n4\nvariables" and replace with one number
answer_list = []
for answer in answers:
    answer_list.append(answer.text)

print(answer_list)

print("\nALL TEXT BELOW\n")

# for paragraph in paragraphs:
#     print(paragraph.text)
# driver.quit()
