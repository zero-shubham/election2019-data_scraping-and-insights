from threading import Thread
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
import time


class Links(Thread):
    def __init__(self, links):
        Thread.__init__(self)
        self.links = links

    def run(self):
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        driver.set_window_size(800, 550)
        for link in self.links:
            print(link)
            statename, link = link.split("$")
            while True:
                driver.get(link)

                try:
                    table = driver.find_element_by_class_name("table-party")
                    tr = table.find_elements_by_tag_name("tr")
                    tableData = []
                    constname = '_'.join(((tr[0].text).split('-')[1]).split(' '))

                    tr = tr[3:]

                    for i in range(0, len(tr)):
                        td = tr[i].find_elements_by_tag_name("td")
                        tableData.append([x.text for x in td])
                    break
                except Exception:
                    pass
            csvname = '../../data/threaded/constituencyWise/new/' + statename + '/' + constname + '.csv'
            os.makedirs(os.path.dirname(csvname), exist_ok=True)
            with open(csvname, "w") as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['SN', 'Candidate', 'Party', 'EVM Votes', 'Postal Votes', 'Total Votes', '% of Votes'])
                for row in tableData:
                    writer.writerow(row)
        driver.close()


def main():
    allLinks = []
    filename = "../../data/pageDetails/state.txt"
    with open(filename, "r") as fstate:
        # extracts code for each state
        for line in fstate:
            stateCode = line.split('-')[1].strip('\n')
            stateName = '_'.join((line.split('-')[0]).split(' '))
            file2name = "../../data/pageDetails/constituencies/" + stateName + "txt"
            # for each state extracts code for each constituency in that state
            # builds the link with those extracted codes
            with open(file2name, "r") as fcons:
                for lineCon in fcons:
                    # builds the link with those extrcted codes
                    link = "http://results.eci.gov.in/pc/en/constituencywise/Constituencywise" + (stateCode + lineCon.strip('\n')) + ".htm?ac=" + lineCon.strip('\n')
                    if stateName=="Telangana" and int(lineCon.strip("\n")) == 4:
                        print("ok")
                    allLinks.append(stateName+"$"+link)

    print(len(allLinks))
    start_time = time.time()
    t1 = Links(allLinks[0:137])
    t2 = Links(allLinks[137:274])
    t3 = Links(allLinks[274:410])
    t4 = Links(allLinks[410:])

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    duration = time.time() - start_time

    print("\n\n=============>", duration, "\n", count)


if __name__ == '__main__':
    main()