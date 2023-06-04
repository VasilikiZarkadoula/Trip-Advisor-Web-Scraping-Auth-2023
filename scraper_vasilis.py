from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
import sys, time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
chrome_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
print("ChromeDriver version:", chrome_version)

def find(xpath):
    tries = 0
    while True:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.location_once_scrolled_into_view
            return element
        except (
            exceptions.StaleElementReferenceException,
            exceptions.ElementClickInterceptedException,
            exceptions.ElementNotInteractableException,
            exceptions.TimeoutException,
            AttributeError,
            UnboundLocalError,
        )as e:
            tries += 1
            if tries > 4:
                print('I did many tries but i cannot click it')
                return None
            print(f"Error: {e}. Retrying...")
            pass


driver.get("https://www.tripadvisor.com/Restaurants-g189473-Thessaloniki_Thessaloniki_Region_Central_Macedonia.html")

#Accept cookies
find("//button[@id='onetrust-accept-btn-handler']").click()

time.sleep(2)


#Show more
show_more_label = find("//span[contains(text(), 'Show more')]")
if show_more_label:
    try:
        show_more_label.click()
        print("Clicked on 'Show more' successfully.")
    except ElementClickInterceptedException as e:
        print(f"Error clicking 'Show more': {e}")
else:
    print("'Show more' label not found.")


#Check Coffee & Tea
time.sleep(2)
label_text = "Coffee & Tea"
label_element = driver.find_element(By.XPATH, "//label[contains(., '{}')]".format(label_text))
checkbox = label_element.find_element(By.XPATH, "./preceding-sibling::input")
driver.execute_script("arguments[0].click();", checkbox)

#Check Bars & Pubs
time.sleep(2)
label_text = "Bars & Pubs"
label_element = driver.find_element(By.XPATH, "//label[contains(., '{}')]".format(label_text))
checkbox = label_element.find_element(By.XPATH, "./preceding-sibling::input")
driver.execute_script("arguments[0].click();", checkbox)

#Uncheck Restaurans
time.sleep(3)
label_text = "Restaurants"
label_element = driver.find_elements(By.XPATH, "//label[contains(., '{}')]".format(label_text))
checkbox = label_element[2].find_element(By.XPATH, "./preceding-sibling::input")
driver.execute_script("arguments[0].removeAttribute('checked'); arguments[0].click();", checkbox)
time.sleep(5)


k = 0
page = 1
with open("href_file.txt", "w") as file:
    for i in range (1, 191):
        k += 1
        business_div = driver.find_element(By.CSS_SELECTOR, f"div[data-test='{i}_list_item']")
        element = business_div.find_element(By.TAG_NAME, "a")
        href = element.get_attribute("href")
        file.write(str(href) + "\n")
        if k == 30:
            k = 0
            page += 1
            try:
                next_page_link = driver.find_element("xpath", f".//a[contains(@aria-label, {page})]").click()
            except NoSuchElementException:
                next_page_link = driver.find_element("xpath", f".//a[contains(@data-page-number, {page})]").click()
            time.sleep(3)

        




