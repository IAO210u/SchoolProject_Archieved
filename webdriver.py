from selenium import webdriver

url = 'http://www.ptpress.com.cn/search/books'

driver = webdriver.Chrome()
# driver.get(url)
driver.get('http://www.ptpress.com.cn/search/books') # this will open a new window

# page source
data = driver.page_source # source code
# print(type(data))
# print(data)



# if clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

wait = WebDriverWait(driver, 10)
cfm_btn = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, '#app>div:nth-child(1)>div>div>div>button>i'))) # the 'search button' position with CSS expression
print(cfm_btn)  # to see if clickable, just print the handles if returned with value, it is clickable

'''
# open several windows
import time
browser = webdriver.Chrome()
browser.get(url)  # open a tab (opening a window at the same time when there's no tab)
browser.execute_script('window.open()')  # open another tab
print(browser.window_handles)  # there are only 2 tabs in total, that's why you can't switch to window_handles[2]
browser.switch_to_window(browser.window_handles[1])
browser.get('http://www.tipdm.com')
time.sleep(1)
browser.execute_script('window.open()')
browser.switch_to_window(browser.window_handles[2])
browser.get('http://www.baidu.com')
browser.get('http://www.tipdm.org')  # this will replace the handle you're on, which is the third window
'''



# auto-search
#driver = webdriver.Chrome()
#driver.get(url)
wait = WebDriverWait(driver, 10)
btn = wait.until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR,'#app > div:nth-child(1) > div > div > div button > i'))
)
btn.click()  # click the clickable element


# scroll down the end(using page's JS)
browser = webdriver.Chrome()
browser.get(url)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# browser.execute_script('alert("You\'ve succeed")')  # look up the inspector with this on, codes only appear after it's gone


# Find element
## through id, css selector and xpath using find_element_by method
# browser = webdriver.Chrome()
# browser.get(url)
input_1st = browser.find_element_by_id('searchVal')  # attribute name is id, whose value is searchVal
input_2nd = browser.find_element_by_css_selector('#searchVal')  # css way of calling it
input_3rd = browser.find_element_by_xpath('//*[@id="searchVal"]')
##** which indicates the handles gotten are NOT randomly named by program but their own 'real's names

## through By cluster
input_by1 = browser.find_element(By.ID, 'searchVal')
input_by2 = browser.find_element(By.CSS_SELECTOR, '#searchVal')
input_by3 = browser.find_element(By.XPATH, '//*[@id="searchVal"]')

print(input_1st)
print(input_by1, '\n')

print(input_2nd)
print(input_by2, '\n')

print(input_3rd)  # all three methods will find the same element
print(input_by3, '\n')

# Find multiple elements
one_em = browser.find_element(By.CSS_SELECTOR, '#nav')
multi_ems = browser.find_elements(By.CSS_SELECTOR, '#nav')  # return a list
print(one_em)
print(multi_ems, '\n')

########## TEST

muti3 = browser.find_elements_by_css_selector('li[class="ivu-page-item"]')
print(len(muti3))  # five elements supposed
mono3 = browser.find_element_by_css_selector('li[class="ivu-page-item"]')
print('The first one:', muti3[0], '\nmono3', mono3)
'''
# Input search
from bs4 import BeautifulSoup
import re
import time
wait = WebDriverWait(browser, 5)  # the browser thing pause
time.sleep(5)  # the whole program pause
# browser.get(url)
input = wait.until(EC.element_to_be_clickable((By.ID, "searchVal")))
btn = browser.find_element_by_id("searchVal")  # this will not jump to the element
time.sleep(3)
btn.send_keys('python编程')  # to send input thus resulting in scrolling
confirm_btn = wait.until(EC.element_to_be_clickable(
(By.CSS_SELECTOR,'#app > div:nth-child(1) > div > div > div button > i') # for div whose value is "app" then > pass to next condition
    # nth-child(1) means the first one of all its big children, it indicates order but only hire
))
time.sleep(3)
confirm_btn.click()
html = browser.page_source  # the source code has changed
soup = BeautifulSoup(html, features='lxml')  # to use lxml, install first
a = soup.select('.rows')  # a CSS selector
ls1 = '<img src="(.*?)"/></div>'  # image information
# The "?" means "less greedy", as .* will match "." as much as it could
pattern = re.compile(ls1, re.S)
res_img = re.findall(pattern, str(a))
ls2 = '<img src=".*?"/></div>.*?<p>(.*?)</p></a>'  # 只收集了<p>和</p>之间的元素
ls2_alt = '<img src=".*?"/></div>.*?<p>.*?</p></a>'  # 从<img src=>到</a>
ls2_alt2 = '<img src=".*?"/></div>(.*?)<p>.*?</p></a>'  # 只收集</div>到<p>之间的，返回的是换行符
# The ".*?" indicates it also matches information with blocks/elements between </div> and <p>
pattern2 = re.compile(ls2, re.S)
res_text = re.findall(pattern2, str(a))

pattern2_alt = re.compile(ls2_alt, re.S)
res_text_alt = re.findall(pattern2_alt, str(a))

pattern2_alt2 = re.compile(ls2_alt2, re.S)
res_text_alt2 = re.findall(pattern2_alt2, str(a))

# print(res_img)

#print(len(res_text), len(res_text_alt))
#print(res_text)
#print(res_text_alt)
print(len(res_text_alt2))
print(res_text_alt2)
browser.quit()


# driver.close()
'''
driver.quit()
browser.quit()


