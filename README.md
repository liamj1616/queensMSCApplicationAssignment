To run either project, first install a python virtual environment,
the download the libraries in requirements.txt using the command:

```
pip install -r requirements.txt
```

## getKaggleGitHubRepoStats.py

Prior to running this project, ensure you set up an environment variable
named githubToken and assign it a Github token. To run this project, enter 
the command in your working directory:

```
python getKaggleGitHubRepoStats.py
```

The stats for each individual repo will be outputted to the file
'individualRepoStats.txt' and also to the terminal as it is executed.
Note that you can remove the terminal outputs if you like a clean 
terminal as I only have them there so I know what the code is currently
executing.

The overall stats for all the GitHub repositories of Kaggle will be
outputted to the file 'overallStats.txt'.

## readJiraIssueReport.py

To run this project, enter the command in your working directory:

```
python readJiraIssueReport.py
```

The information scraped from the Jira Issue report will be outputted
to the file 'jira_issue_report.csv'.
