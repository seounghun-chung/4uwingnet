from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re

options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('window-size=1920x1080')
#options.add_argument("disable-gpu")

driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe', chrome_options=options)

def parseHtml(f):
    s = BeautifulSoup(f, 'html.parser')
    s = s.select(".left")
    l = list()
    for ii in s:        
        l += (ii.select('a[href^="http://www.ppomppu.co.kr/zboard/view"]'))

    out = dict()
    for o in l:
        if(o.get_text() != ""):
            out.update({o.get("href") : o.get_text()})
            
    return out
    
def change_subject(link):
    driver.get(link)
    try:
        driver.find_element_by_xpath('//*[@id="revolution_main_table"]/tbody/tr[1]/td/a[1]/font').click()                                              
    except:
        driver.find_element_by_xpath('//*[@id="ex3"]/div[3]/div[1]/a').click()
        driver.find_element_by_xpath('//*[@id="revolution_main_table"]/tbody/tr[1]/td/a[1]/font').click()        
        
    # modify subject
    driver.find_element_by_xpath('//*[@id="divSubject"]/td[2]/input').clear()    
    driver.find_element_by_xpath('//*[@id="divSubject"]/td[2]/input').send_keys('ppung')    

    
    # modify body
    remain = '/div[6]/div[2]'
    remain2 = '/div[2]/textarea'
    xpath = ''
    for ii in range(10,13):
        xpath = '/html/body/div[6]/div[2]/div[4]/div/form/table/tbody/tr/td/table[2]/tbody/tr[%d]/td[2]/div[3]' % (ii)
        try:
            driver.find_element_by_xpath(xpath+remain)
            break
        except:
            continue        
    
    driver.find_element_by_xpath(xpath+remain).click()    
    driver.find_element_by_xpath(xpath+remain2).clear()    
    driver.find_element_by_xpath(xpath+remain2).send_keys('ppung')    

    driver.find_element_by_xpath('//*[@id="ok_button"]').click()

    
def find_path():
    out = dict()
    for pageNum in range(1,2):
        driver.get('http://www.ppomppu.co.kr/myinfo/member_my_write_list.php?page=%d&search_type=subject&keyword=' % pageNum)
        html = driver.page_source
        out.update(parseHtml(html))
    return out

def find_comment_path():
    out = dict()
    for pageNum in range(2,8):                    
        driver.get('http://www.ppomppu.co.kr/myinfo/member_my_comment_list.php?page=%d&search_type=memo&keyword=' % pageNum)
        html = driver.page_source
        out.update(parseHtml(html))
    return out    

def modify_comment(link):
    driver.get(link)
    a = re.compile(r"cno=\d+")
    comment_num = a.search(link).group().replace("cno=","")
    
    try:
        driver.find_element_by_xpath('//*[@id="comment_%s"]/div[1]/table/tbody/tr/td[6]/a' % comment_num).click()
    except:
        # QnA query
        driver.find_element_by_xpath('//*[@id="ex3"]/div[3]/div[1]/a').click()
        driver.find_element_by_xpath('//*[@id="comment_%s"]/div[1]/table/tbody/tr/td[6]/a' % comment_num).click()
        
    driver.find_element_by_xpath('//*[@id="memo"]').clear()
    driver.find_element_by_xpath('//*[@id="memo"]').send_keys("ppung")    
    driver.find_element_by_xpath('//*[@id="comment_write_form"]/tbody/tr[1]/td[2]/table/tbody/tr[4]/td[2]/input[1]').click()
    
def connect():
    driver.implicitly_wait(2)
    driver.get('https://www.ppomppu.co.kr/zboard/login.php')
    driver.find_element_by_name('user_id').send_keys('mmysun88')
    driver.find_element_by_name('password').send_keys('tlsqud88')
    driver.find_element_by_xpath('//*[@id="zb_login"]/ul/a/li').click()

connect()
o = find_comment_path()
print(o)
for ii in o:
    if (o[ii] == "ppung"):
        continue
        
    start_time = time.time()
    modify_comment(ii)
    print("%s %s : %f s" % (ii,o[ii],time.time()-start_time))
    time.sleep(0.1)

#print(o)
#connect()
#o = find_path()
#print(o)
#for ii in o:
#    if (o[ii] == "ppung"):
#        continue
#        
#    start_time = time.time()
#    change_subject(ii)
#    print("%f s" % (time.time()-start_time))
#    time.sleep(0.1)

