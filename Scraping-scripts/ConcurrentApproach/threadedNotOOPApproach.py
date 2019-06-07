import threading
import time
import concurrent.futures
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv

thread_local = threading.local()
count: int = 0


def get_driver():
    if not hasattr(thread_local, "driver"):
        thread_local.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        thread_local.driver.set_window_size(800, 550)
    return thread_local.driver


def parse_link(link):
    global count
    count += 1
    statename, link = link.split("$")
    driver = get_driver()
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
    csvname = './data/threaded/constituencyWise/new/' + statename + '/' + constname + '.csv'
    os.makedirs(os.path.dirname(csvname), exist_ok=True)
    with open(csvname, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['SN', 'Candidate', 'Party', 'EVM Votes', 'Postal Votes', 'Total Votes', '% of Votes'])
        for row in tableData:
            writer.writerow(row)


def parse_all_links(links):
    print(links)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(parse_link,links)


def main():
    allLinks = []
    filename = "./data/pageDetails/state.txt"
    with open(filename, "r") as fstate:
        # extracts code for each state
        for line in fstate:
            stateCode = line.split('-')[1].strip('\n')
            stateName = '_'.join((line.split('-')[0]).split(' '))
            file2name = "./data/pageDetails/constituencies/" + stateName + "txt"
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
    parse_all_links(allLinks)
    duration = time.time() - start_time

    print("\n\n=============>", duration, "\n", count)


if __name__ == '__main__':
    main()