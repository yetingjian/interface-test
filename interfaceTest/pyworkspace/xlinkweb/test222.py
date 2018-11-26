from selenium import webdriver

driver = webdriver.Chrome()
driver.maximize_window()
url = "http://test.xlink.cn/v5/#/auth/login"
driver.get(url)

str = driver.find_element_by_xpath('//input[starts-with(@id,"contac["part","icles"]")]')