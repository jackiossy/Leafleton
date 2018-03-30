from selenium import webdriver
import time,string,re
from pymongo import MongoClient

def input_work_keywords(driver,keywords):
    input_keyword = driver.find_element_by_xpath('//*[@id="KeyWord_kw2"]')
    input_keyword.clear()
    input_keyword.send_keys(keywords)
    search_btn = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/div/div/form/div[8]/button')
    search_btn.click()
    pass

def get_work_details(driver,work_href):
    driver.get(work_href)
    pass

def get_work_info(driver,index):
    work_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[1]/div/a').text
    response_rate = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[2]/span').text
    company_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[3]/a[1]').text
    monthly_pay = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[4]').text
    work_address = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[5]').text
    date = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[2]/div/table['+index+']/tbody/tr[1]/td[6]/span').text
    work_dic = {'work_name': work_name, 'response_rate': response_rate, 'company_name': company_name, 'monthly_pay': monthly_pay, 'work_address': work_address, 'date': date}
    collection = MongoClient('mongodb://localhost:27017/')['zhilian']['python']
    collection.insert(work_dic)
    pass

def get_result_count(driver):
    count_str = driver.find_element_by_class_name('search_yx_tj').text
    count = re.sub("\D", "", count_str)
    return int(count)
    pass


driver = webdriver.PhantomJS()
driver.get('https://sou.zhaopin.com/jobs/searchresult.ashx?isadv=1')
input_work_keywords(driver,"python")
driver.save_screenshot('test.png')


page_cnt = get_result_count(driver)/60
print(int(page_cnt))

for page_num in range(1,int(page_cnt)):
    for i in range(2,62):
        print('__________________ '+str(page_num)+'页 第'+str(i)+'条_______________')
        get_work_info(driver,str(i))
        pass
    next_page = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[2]/form/div[1]/div[1]/div/div[3]/ul/li[10]/a')
    next_page.click()
