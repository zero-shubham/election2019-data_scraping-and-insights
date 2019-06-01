from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import os
#opt = webdriver.ChromeOptions()
#opt.add_argument("headless")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1120, 550)
driver.get("http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm")

selectState = driver.find_element_by_id("ddlState")

stateOptions = selectState.find_elements_by_tag_name("option")
print(stateOptions)

stateName = []
for i in range(1,len(stateOptions)):
    filename = "./data/pageDetails/state.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "a") as f:
        f.write(stateOptions[i].text + '-' + stateOptions[i].get_attribute("value") + "\n")
        stateName.append('_'.join((stateOptions[i].text).split(' ')))

print(len(stateName),"\n\n\n========================================\n")
count = 0

for i in range(1,len(stateOptions)):
    driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL,"t")
    driver.get("http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm")

    while True:
        try:
            selectState = driver.find_element_by_id("ddlState")
            stateOptions = selectState.find_elements_by_tag_name("option")

            stateOptions[i].click()

            selectCon = driver.find_element_by_id("ddlAC").find_elements_by_tag_name("option")
            selectCon = selectCon[1:]

            ids = []
            for j in range(0,len(selectCon)):
                ids.append(selectCon[j].get_attribute("value"))
            print(len(ids) == len(selectCon))
            print(len(ids))
            filename = "./data/pageDetails/constituencies/" + stateName[i-1] + 'txt'
            print(filename)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "a") as f:
                f.write("\n".join(ids))
            count+=1
            break
        except:
            pass


print(count)
driver.close()