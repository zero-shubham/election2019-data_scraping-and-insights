from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
driver.set_window_size(1120, 550)


filename = "./data/pageDetails/state.txt"
count = 0
with open(filename, "r") as fstate:
    # extracts code for each state
    for line in fstate:
        stateCode = line.split('-')[1].strip('\n')
        stateName = '_'.join((line.split('-')[0]).split(' '))
        file2name = "./data/pageDetails/constituencies/"+stateName+"txt"
        # for each state extracts code for each constituency in that state
        with open(file2name, "r") as fcons:
            for lineCon in fcons:
                # builds the link with those extrcted codes
                link = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise"+(stateCode+line.strip('\n'))+".htm?ac="+line.strip('\n')
                driver.get(link)
                table = driver.find_element_by_class_name("table-party")
                tr = table.find_elements_by_tag_name("tr")
                tableData = []
                csvn = '_'.join(((tr[0].text).split('-')[1]).split(' '))

                tr = tr[3:]

                for i in range(0,len(tr)):
                    td = tr[i].find_elements_by_tag_name("td")
                    tableData.append([ x.text for x in td])

                csvname = './data/constituencyWise/'+stateName+'/'+csvn+'.csv'
                os.makedirs(os.path.dirname(csvname), exist_ok=True)

                with open(csvname, "w") as csvfile:
                    count+=1
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(['SN', 'Candidate', 'Party', 'EVM Votes', 'Postal Votes', 'Total Votes', '% of Votes'])
                    for row in tableData:
                        writer.writerow(row)

                print(count)
driver.close()