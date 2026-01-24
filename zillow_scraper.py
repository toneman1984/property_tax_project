from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import undetected_chromedriver as uc
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

#the url that chrome will open
url = "https://www.zillow.com/homes/for_rent/"

#dictionary of test addresses
addresses = {'address':['12800 Tomanet Trl #B, Austin, TX 78727', '7518A Stonecliff Dr, Austin, TX 78731'], 'rental':''}

#convert python dictionary into pandas dataframe  
test_addresses_df = pd.DataFrame(addresses)

#custom function for scraping zillow
def is_rental(url, addresses_df):
    
    #instantiate selenium webdriver
    options = webdriver.ChromeOptions() 

    #got this from stack exchange. it circumvents the bot check
    options.add_argument('--disable-blink-features=AutomationControlled')

    #while the counter i, which starts at 0, is less than the number of addresses, do the following
    i = 0
    while i < len(addresses_df):
        #This is for debugging. We can take this out later 
        print(f"loop {i}")
        
        #The line driver = uc.Chrome() initializes an instance of a Chrome web driver using the undetected_chromedriver library in Python in order to avoid bot detection
        driver = uc.Chrome()

        #open the zillow url
        driver.get(url)   

        #wait 2 seconds for the url to fully load
        time.sleep(2)

        #finds the search bar
        search_bar = driver.find_element(By.CLASS_NAME, "StyledFormControl-c11n-8-109-3__sc-w61kvv-0")

        #delete the 'Austin TX' default text in the search bar
        search_bar.send_keys(Keys.BACK_SPACE * 9)

        #locate the nth address on the nth loop through
        addy = addresses_df.at[i,'address']

        print(addy)
        time.sleep(120)
        try:
            #locate the anti bot checker
            press_and_hold_element = driver.find_element(By.XPATH, '//*[@id="WoUdupanTEFedGf"')
            
            #instantiate Action Chains for the click and hold
            actions = ActionChains(driver)

            #click and hold on the press and hold element
            actions.click_and_hold(press_and_hold_element).perform()
        
        except Exception as e:
            print(f"Element not found: {e}")

        #wait 3 seconds 
        time.sleep(3)

        #release mouse
        actions.release(press_and_hold_element).perform()

        #type the address into the search bar
        search_bar.send_keys(addresses_df.at[i,'address'])

        #wait a second for the address finish being typed
        time.sleep(1)

        #press enter on the keyboard
        search_bar.send_keys(Keys.ENTER)

        #wait a second for the url to load
        time.sleep(1)

        #find where the html/css element that contains the text 'Listed for rent' is
        rental_element = driver.find_element(By.CLASS_NAME, 'jDnfxD')

        #grab the text 	'Listed for rent'
        rental_el_text = rental_element.text

        #at the nth loop trough the function, at the index of the dataframe, in column 'rental', insert the 'yes' value. This answers the question, 'is this a rental?'. 
        addresses_df.at[i,'rental'] = 'yes'
        
        #close the chrome browser

        driver.close()
        print(f"the zillow page says {rental_el_text}")

        #add 1 to i before looping back to beginning of function
        i += 1
    
    #make a copy of the dataframe just in case we messed something up
    copy_addresses_df = addresses_df 

    return copy_addresses_df   

#call the custom function 
rental_check_df = is_rental(url, test_addresses_df)

print(rental_check_df)




