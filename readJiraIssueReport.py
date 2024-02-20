import requests
from bs4 import BeautifulSoup

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

        # labels = soup.find("span", {"id": "labels-13028113-value"}).text.strip()
        # labels = '[' + labels.replace(' ','') + ']'
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
    
        # COMMENTS AREN'T READING PROPERLY!!!!!
        comment_header_divs = soup.find_all("div", class_="action-head")
        comment_body_divs = soup.find_all("div", class_="action-body flooded")
        comment_string = '['
        if comment_header_divs and comment_body_divs:
            if len(comment_header_divs) != len(comment_body_divs):
                for i in range(len(comment_header_divs)):
                    '''
                    Code for reading comments will be inserted here
                    '''
                    if i != len(comment_header_divs) - 1:
                        comment_string += ','
            else:
                print('Something went wrong in reading comments')
        else:
            print("No comments found")

        comment_string += ']'
            

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