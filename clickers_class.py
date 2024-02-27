from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


clicker_dict = {}

class clicker:

    def __init__(self, driver, number) -> None:
        self.number = number
        self.element = driver.find_element(By.ID,"product" + str(self.number))
        self.price = int(driver.find_element(By.ID,"productPrice" + str(self.number)).text.replace(",",""))
        self.owned = driver.find_element(By.ID,"productOwned" + str(self.number)).text.replace(",","")
        self.name = driver.find_element(By.ID,"productName" + str(self.number)).text
        clicker_dict[self.number] = self

    def reinitialize (self, driver):
        self.element = driver.find_element(By.ID,"product" + str(self.number))
        self.price = int(driver.find_element(By.ID,"productPrice" + str(self.number)).text.replace(",",""))
        self.owned = driver.find_element(By.ID,"productOwned" + str(self.number)).text.replace(",","")

    def get_element(self, driver):
        
        if EC.staleness_of(self.element)(driver):        
            self.reinitialize(self, driver) #updating info
        return self.element
    
    def get_price(self):
        return self.price