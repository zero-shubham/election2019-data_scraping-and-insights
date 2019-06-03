from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1120, 550)

# retrieve data for all party's winning seats
driver.get("http://results.eci.gov.in/pc/en/partywise/allparty.htm")

# table that contains the data is found
table = driver.find_element_by_class_name("table-party")
# print(table.text)

path = "../data/allparty/"

# selecting row wise as it will help writing the data line wise
tr = table.find_elements_by_tag_name("tr")[2:]

with open(path+'raw.txt', 'w') as wFile:
    for row in tr:
        wFile.write(row.text+"\n")


with open(path+'raw.txt', 'r') as f:
    with open(path+'allParty.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for line in f:
            final = list()
            s = line
            s = s.strip('\n')
            splitStr = s.split(' ')

            # join everything except last 3 character as it is known that those 3 are numbers
            nameOfEachParty = ' '.join(splitStr[:-3])
            # convert those last 3 element to int
            numbersForEachParty = list(map(int,splitStr[-3:]))

            final.append(nameOfEachParty)
            for i in numbersForEachParty:
                final.append(i)
            print("\n==>",final)

            writer.writerow(final)

driver.close()