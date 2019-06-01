from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
#opt = webdriver.ChromeOptions()
#opt.add_argument("headless")

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1120, 550)

filename = "./data/pageDetails/state.txt"
count = 0
with open(filename, "r") as fstate:
    for line in fstate:
        stateCode = line.split('-')[1].strip('\n')
        stateName = '_'.join((line.split('-')[0]).split(' '))
        file2name = "./data/pageDetails/constituencies/"+stateName+"txt"
        with open(file2name, "r") as fcons:
            for line in fcons:
                link = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise"+(stateCode+line.strip('\n'))+".htm?ac="+line.strip('\n')
                driver.get(link)
                table = driver.find_element_by_class_name("table-party")
                file3name = "./data/constituencyWise/"+stateName+"/"+line.strip('\n')+".txt"
                os.makedirs(os.path.dirname(file3name),exist_ok=True)
                with open(file3name, "w") as f3:
                    f3.write(table.text)
                count+=1
                print(count)
driver.close()