from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from time import sleep, time
from clickers_class import clicker, clicker_dict

try:
    service = Service(executable_path="chromedriver.exe") #Need to download  chromedriver.exe separately 
except:
    prrint("There is a problem with initiating chromedriver")

chrome_options = Options()
#chrome_options.add_argument("--user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data/Profile 10")


driver = webdriver.Chrome(service = service, options=chrome_options)
#sleep(5)
driver.get("https://orteil.dashnet.org/cookieclicker/")

clickers_unlocked = 0                   #game progress
close_button = []                       #closed notes
cokie_acepted = False
cookies = 0.0
cps = 0.0                               #cookies per second
cpc = 1.0                               #closed per click
goal = 1                                #upgrade  counter
game_set_up = False                     #initial setup
action = ActionChains(driver)           

#setting up language
try:
    cookie_loaded = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"langSelect-EN")))
    select_lang = driver.find_element(By.ID,"langSelect-EN")                    
    select_lang.click()
except:
    pass
big_cookie = driver.find_element(By.ID,"bigCookie")

try :
    cookie_loaded = WebDriverWait(driver,2, 1).until(EC.staleness_of(big_cookie))
except TimeoutException:
    pass
big_cookie = driver.find_element(By.ID,"bigCookie")



def setup():
    
    options = driver.find_element(By.ID,"prefsButton")
    options.click()
    #sleep(3)
    #ActionChains.scroll_by_amount(driver,delta_x=0,delta_y=10)
    
    action.move_to_element(driver.find_element(By.ID,"menu"))
    action.key_down(Keys.ARROW_DOWN)
    action.perform()   
    if driver.find_element(By.ID,"formatButton").text.split(" ")[-1] == "ON":
        driver.find_element(By.ID,"formatButton").click()
    if driver.find_element(By.ID,"particlesButton").text.split(" ")[-1] == "ON":
        driver.find_element(By.ID,"particlesButton").click()
    if driver.find_element(By.ID,"fancyButton").text.split(" ")[-1] == "ON":
        driver.find_element(By.ID,"fancyButton").click()
    options.click()

def cookies_agrement():
    try:
        cookie_loaded = WebDriverWait(driver,2,1).until(EC.presence_of_element_located((By.LINK_TEXT,"Got it!")))
        if cookie_loaded:
            accept_all = driver.find_element(By.LINK_TEXT,"Got it!")         # close notification
            accept_all.click()
    except:
        pass

def check_cpc():
    global cpc
    stats = driver.find_element(By.ID,"statsButton")
    stats.click()
    menu = driver.find_element(By.ID,"statsGeneral")
    if menu.find_elements(By.CLASS_NAME,"listing")[7].text.__contains__("Cookies per click"):
        cpc = float(menu.find_elements(By.CLASS_NAME,"listing")[7].text.split(" ")[3].replace(",","")) #pull the needed piece of text and format it
    else:
        print("Check failed in  cpc")
    stats.click()
def check_upgrades()-> None:
    global cookies
    global goal
    try:
        first_upgrade = driver.find_element(By.ID,"upgrade0")
        action.move_to_element(first_upgrade)
        action.perform()
        tooltip = driver.find_element(By.ID,"tooltip")
        #price = int(tooltip.find_element(By.CLASS_NAME,"price disabled").text.replace(",",""))
        price = int(tooltip.find_element(By.CLASS_NAME,"price").text.replace(",",""))
        
    except StaleElementReferenceException:
        first_upgrade = driver.find_element(By.ID,"upgrade0")
        action.move_to_element(first_upgrade)
        action.perform()
        tooltip = driver.find_element(By.ID,"tooltip")
        price = int(tooltip.find_element(By.CLASS_NAME,"price").text.replace(",",""))
    except:
        return
    
    if price < cookies:
        driver.find_element(By.ID,"upgrade0").click()
        cookies = float(driver.find_element(By.ID,"cookies").text.split(" ")[0].replace(",",""))
        check_cpc()
    else:
        goal = price
       
#Alt - Golden cookie class= shimmer shimmers
cookies_agrement()

while True:
    if game_set_up:
        cookies = float(driver.find_element(By.ID,"cookies").text.split(" ")[0].replace(",",""))
        cps = float(driver.find_element(By.ID,"cookies").text.split(" ")[-1].replace(",",""))
    else:
        if len(close_button)==1:
                game_set_up = True
                setup()
                pass

    if EC.staleness_of(big_cookie):
        big_cookie = driver.find_element(By.ID,"bigCookie")                 #Clicking on the main loop if usefull
    if cpc > (0.1 * cps): big_cookie.click()

    close_found = EC.presence_of_element_located((By.ID, "notes"))(driver)  #closing all notes 
    if close_found:
        close_button = driver.find_elements(By.CLASS_NAME, "close")
        if len(close_button)>1:
            for item in close_button:
                if item.text == "x" : item.click()
                break
    
    for e in range(clickers_unlocked,20):       # updating clikers list
        if e in clicker_dict:                   # adjust starting positiong of the check
            clickers_unlocked += 1
            break
        tmp = driver.find_element(By.ID,"product" + str(e)).get_attribute("class") 
        if tmp == "product unlocked enabled":   # check if a new product unlocked and add it to dictioary 
            if not e in clicker_dict:
                clicker(driver,e)
                break
        else:                                   # stop at first locked product
            break
    if cookies > goal:
        check_upgrades()

    for item in clicker_dict:
        cookies = float(driver.find_element(By.ID,"cookies").text.split(" ")[0].replace(",",""))
        if clicker_dict[item].get_price() < cookies:
            clicker_dict[item].get_element(driver).click()
            clicker_dict[item].reinitialize(driver)
            
            check_upgrades()                                    #buy the cheapest clicker and check upgrades afterwards
        pass
    
    
