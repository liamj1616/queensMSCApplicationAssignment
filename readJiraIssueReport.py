import requests, time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def readJiraIssueReport(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        '''
        You can find whatever details you need by looking at the
        HTML source code of the webpage.
        '''

        '''
        Note that these are all values that are always present in the 
        modules of a Jira Issue Report.

        Note that there are is also a custom field module, where fields
        such as "Patch Info" or "Estimated Complexity" can be added. It
        is not recommended to add these fields as then the script may 
        not work for different Jira pages.
        '''
        issue_key = soup.find("a", {"id": "key-val"}).text.strip()
        summary = soup.find("h1", {"id": "summary-val"}).text.strip()
        type = soup.find("span", {"id": "type-val"}).text.strip()
        status = soup.find("span", {"id": "status-val"}).text.strip()
        priority = soup.find("span", {"id": "priority-val"}).text.strip()
        resolution = soup.find("span", {"id": "resolution-val"}).text.strip()

        affects_versions = soup.find("span", {"id": "versions-field"}).text.strip()
        affects_versions = '[' + affects_versions.replace(' ','') + ']'

        fix_versions = soup.find("span", {"id": "fixVersions-field"}).text.strip()
        fix_versions = '[' + fix_versions.replace(' ','') + ']'

        components = soup.find("span", {"id": "components-val"}).text.strip()
        components = '[' + components.replace(' ','') + ']'

        labels_string = '['
        label_divs = soup.find_all("div", class_="labels")
        for i in range(len(label_divs)):
            labels_string += label_divs[i].find("span").string().strip()

            if i != len(label_divs) - 1:
                labels_string += ','

        labels_string += ']'

        assignee = soup.find("span", {"id": "assignee-val"}).text.strip()
        reporter = soup.find("span", {"id": "reporter-val"}).text.strip()

        date_title_string = ''
        date_string = ''
        date_divs = soup.find_all("dl", class_="dates")
        for i in range(len(date_divs)):
            date_title_string += date_divs[i].find("dt").string.strip()
            date_string += date_divs[i].find("time").get("datetime")

            if i != len(date_divs) - 1:
                date_title_string += ','
                date_string += ','

        date_title_string = date_title_string.replace(" ","")
        date_title_string = date_title_string.replace(":","")

        description = soup.find("div", {"id": "description-val"}).text.strip().replace('\n','')
    
        # Since comments are lazy-loaded based on an onClick event, need to use a driver
        driver = webdriver.Chrome()
        driver.get(url)
        lazy_load_button = driver.find_element(By.XPATH, "//li[@id='comment-tabpanel']")
        lazy_load_button.click()

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        comment_string = '['

        comment_divs = soup.find_all("div", class_="action-head")
        '''
        This returns 2 divs for each comment: one that contains the HTML
        source code to show if the the comment is collapsed, therefore
        only the commenter and the comment time is shown and one that 
        contains the HTML source code to show if the comment is expanded
        which contains the comment itself. Therefore, we will iterate 
        through every second item in comment_divs
        '''
        if comment_divs:
            for i in range(1,len(comment_divs),2):
                commenter = comment_divs[i].find("a").text.strip()
                comment_string += '[' + commenter + ','
                comment_string += comment_divs[i].find("time").get("datetime") + ','

                comment = comment_divs[i].find("div", class_="action-details flooded").text.strip()
                comment = comment.replace("\n","")
                
                cur_reading = ''
                reading_commenter = True
                waiting_for_post_date = False
                reading_post_date = False
                reading_comment = False
                for char in comment:
                    if reading_comment:
                        comment_string += char
                    elif reading_post_date:
                        cur_reading += char
                        if len(cur_reading) == 15:
                            reading_comment = True
                            reading_post_date = False
                    elif waiting_for_post_date:
                        if char.isnumeric():
                            cur_reading += char
                            waiting_for_post_date = False
                            reading_post_date = True
                    elif reading_commenter:
                        cur_reading += char
                        if cur_reading == commenter:
                            cur_reading = ''
                            reading_commenter = False
                            waiting_for_post_date = True
                        
                comment_string += ']'
                if i != len(comment_divs) - 1:
                    comment_string += ','
        else:
            print('No comments found')

        comment_string += ']'
        print(comment_string)

        driver.quit()
            
        with open('jira_issue_report.csv', 'w') as outfile:
            outfile.write('Issue Key,Summary,Type,Status,Priority,Resolution,Affects Versions,' + 
                          'Fix Versions,Components,Labels,Assignee,Reporter,' 
                          + date_title_string + ',Description,Comments\n')
            outfile.write(
                issue_key + ',' +
                summary + ',' +
                type + ',' +
                status + ',' +
                priority + ',' +
                resolution + ',' +
                affects_versions + ',' +
                fix_versions + ',' +
                components + ',' +
                labels_string + ',' +
                assignee + ',' +
                reporter + ',' +
                date_string + ',' +
                description + ',' + 
                comment_string + '\n'
            )
        

    else:
        print("Error fetching data from Jira:", response.status_code)

if __name__ == "__main__":
    '''
    If you want to use this script to read multiple Jira 
    issue reports, you can modify this code so that the 
    variable 'url' accepts a command line argument, then
    create a shell script containing all the URLs of Jira 
    issue reports that you want to read
    '''
    url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
    readJiraIssueReport(url)