from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Tests import XLUtils

# Launch the browser
driver = webdriver.Chrome()
driver.maximize_window()

# Open the URL
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

# Excel File Path
path="C://Users/Manisha/Documents/TestData.xlsx"

# Get Row Count
rows=XLUtils.get_row_count(path,'Sheet1')

# Explicit Wait
wait=WebDriverWait(driver,10)


for r in range(2,rows +1):
    username=XLUtils.read_data(path,'Sheet1',r,1)
    password=XLUtils.read_data(path,'Sheet1',r,2)

    try:
        user_field=wait.until(EC.presence_of_element_located((By.NAME,"username")))
        user_field.clear()

        # Enter UserName
        user_field.send_keys(username)

        # Enter Password
        pass_field=driver.find_element(By.NAME,"password")
        pass_field.clear()
        pass_field.send_keys(password)

        # Click on Login Button
        driver.find_element(By.XPATH,"//button[normalize-space()='Login']").click()

        # Verify Successful Login
        wait.until(EC.presence_of_element_located((By.XPATH,"//p[@class='oxd-userdropdown-name']")))

        print("Test Case Passed")
        XLUtils.write_data(path,'Sheet1',r,3,'Test Passed')

        # Logout
        driver.find_element(By.XPATH,"//p[@class='oxd-userdropdown-name']").click()
        wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Logout']"))).click()

    except (NoSuchElementException, TimeoutException):
        print("Test Case Failed")
        XLUtils.write_data(path, 'Sheet1', r, 3, 'Test Failed')

    except Exception as e:
        print(f"Login Failed : {e}")
        XLUtils.write_data(path, 'Sheet1', r, 3, 'Test Failed')
        driver.refresh()

# Close the Browser
input("Press Enter to Close the browser...")
driver.quit()










