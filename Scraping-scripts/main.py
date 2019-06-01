'''from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

'opt = webdriver.ChromeOptions()
opt.add_argument("headless")''
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1120, 550)
driver.get("http://results.eci.gov.in/pc/en/partywise/allparty.htm")'''

# table = driver.find_element_by_class_name("table-party")
# print(table.text)

import csv

with open('raw.txt', 'r') as f:
    with open('test.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for line in f:
            final = list()
            s = line
            s = s.strip('\n')
            splitStr = s.split(' ')
            nameOfEachParty = ' '.join(splitStr[:-3])
            numbersForEachParty = list(map(int,splitStr[-3:]))
            final.append(nameOfEachParty)
            for i in numbersForEachParty:
                final.append(i)
            print("\n==>",final)
            writer.writerow(final)