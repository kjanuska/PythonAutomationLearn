from selenium.webdriver import Firefox

# from selenium.webdriver.firefox.options import Options

# opts = Options()
# opts.set_headless()
# assert opts.headless  # operating in headless mode
# browser = Firefox(options=opts)
browser = Firefox()
browser.get("https://start.duckduckgo.com")

search_form = browser.find_element_by_id("search_form_input_homepage")
search_form.send_keys("youtube")
search_form.submit()

results = browser.find_element_by_css_selector(
    "#r1-1 > div:nth-child(1) > h2:nth-child(1)"
)
print(results.txt)

# browser.close()
# quit()
