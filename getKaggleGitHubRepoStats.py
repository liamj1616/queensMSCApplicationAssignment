import requests, os
import numpy as np

def getKaggleGitHubRepoStats():
    # Need to set up an environment variable called
    # 'githubToken' and assign it a value of a
    # GitHub token
    access_token = os.environ['githubToken']
    owner = 'Kaggle'
    headers = {'Authorization':'Token '+access_token}

    def add_to_file_list(page, path, file_list):
        for element in page['tree']:
            if element['type'] == 'tree':
                new_page = requests.get(element['url'],headers=headers).json()
                new_path = path + '/' + element['path']
                add_to_file_list(new_page, new_path, file_list)
            else:
                file_list.append(path + '/' + element['path'])
                

    num_commits = []
    num_stars = []
    num_contributors = []
    num_branches = []
    num_tags = []
    num_forks = []
    num_releases = []
    num_closed_issues = []
    num_environments = []

    lines_per_lang = []

    individualRepoStats = open('individualRepoStats.txt','w')

    '''
    Github API stores 30 items per page

    If a dictionary has more than 30 items, you will need to 
    loop through the pages as done below

    It must be manually decided the maximum number of pages
    you are willing to loop through based on the total number
    of items in the dictionary
    '''
    url=f"https://api.github.com/users/{owner}/repos?page=1"
    repos=requests.get(url,headers=headers).json()
    for i in range(len(repos)):

        print(repos[i]['name'])
        individualRepoStats.write(repos[i]['name'] + ' STATS\n')

        num_commits.append(0)
        for page_num in range(1,100):
            try:
                url=f""+repos[i]['commits_url']
                url = url[0:-6]+"?page="+str(page_num)
                commit_page = requests.get(url,headers=headers).json()
                num_commits[i] += len(commit_page)
                if len(commit_page) == 0:
                    break
            except:
                break

        print(num_commits[i], 'commits')
        individualRepoStats.write(str(num_commits[i]) + ' commits\n')

        num_stars.append(0)
        for page_num in range(1,250):
            try:
                url=f""+repos[i]['stargazers_url']+"?page="+str(page_num)
                stars_page = requests.get(url,headers=headers).json()
                num_stars[i] += len(stars_page)
                if len(stars_page) == 0:
                    break
            except:
                break

        print(num_stars[i], 'stars')
        individualRepoStats.write(str(num_stars[i]) + ' stars\n')


        num_contributors.append(0)
        for page_num in range(1,10):
            try:
                url=f""+repos[i]['contributors_url']+"?page="+str(page_num)
                contributors_page = requests.get(url,headers=headers).json()
                num_contributors[i] += len(contributors_page)
                if len(contributors_page) == 0:
                    break
            except:
                break

        print(num_contributors[i], 'contributors')
        individualRepoStats.write(str(num_contributors[i]) + ' contributors\n')

        num_branches.append(0)
        for page_num in range(1,10):
            try:
                url = f""+repos[i]['branches_url'][0:-9]+"?page="+str(page_num)
                branch_page = requests.get(url,headers=headers).json()
                num_branches[i] += len(branch_page)
                if len(branch_page) == 0:
                    break
            except:
                break

        print(num_branches[i], 'branches')
        individualRepoStats.write(str(num_branches[i]) + ' branches\n')

        num_tags.append(0)
        for page_num in range(0,10):
            try:
                url=f""+repos[i]['tags_url']+"?page="+str(page_num)
                tags_page = requests.get(url,headers=headers).json()
                num_tags[i] += len(tags_page)
                if len(tags_page) == 0:
                    break
            except:
                break
        print(num_tags[i], ' tags')
        individualRepoStats.write(str(num_tags[i]) + ' tags\n')


        num_forks.append(0)
        if repos[i]['forks']:
            for page_num in range(1,60):
                try:
                    url=f""+repos[i]['forks_url']+"?page="+str(page_num)
                    fork_page = requests.get(url,headers=headers).json()
                    num_forks[i] += len(fork_page)
                    if len(fork_page) == 0:
                        break
                except:
                    break
        
        print(num_forks[i], 'forks')
        individualRepoStats.write(str(num_forks[i]) + ' forks\n')

        num_releases.append(0)
        for page_num in range(1,60):
            try:
                url=f""+repos[i]['releases_url']
                url = url[:-5] +"?page="+str(page_num)
                release_page = requests.get(url,headers=headers).json()
                num_releases[i] += len(release_page)
                if len(release_page) == 0:
                    break
            except:
                break

        print(num_releases[i], ' releases')
        individualRepoStats.write(str(num_releases[i]) + ' releases\n')

        num_closed_issues.append(0)
        for page_num in range(1,100):
            try:
                url=f""+repos[i]['issue_events_url']
                url=url[0:-9]+"?page="+str(page_num)
                closed_issue_page = requests.get(url,headers=headers).json()
                num_closed_issues[i] += len(closed_issue_page)
                if len(closed_issue_page) == 0:
                    break
            except:
                break
        individualRepoStats.write(str(num_closed_issues[i]) + ' closed issues\n')
        print(num_closed_issues[i], 'closed issues')

        num_environments.append(0)
        url=f""+repos[i]['deployments_url']
        environments_page = requests.get(url,headers=headers).json()
        num_environments[i] += len(environments_page)
        individualRepoStats.write(str(num_environments[i]) + ' environments\n')
        print(num_environments[i], 'environments')

        lines_per_lang.append({})

        '''
        .allstar,jupyterlab,kaggle-environments,learntools,pipelinehelpers HAS 'master' BRANCH
        WHEREAS
        docker-julia,docker-python,docker-rcran,docker-rstats
        kaggle-api,kagglehub HAS 'main' BRANCH
        '''
        branches_page = requests.get(repos[i]['branches_url'][:-9],headers=headers).json()
        sha = ''
        branch_name = ''
        for branch in branches_page:
            if branch['name'] == 'master':
                sha = branch['commit']['sha']
                branch_name = 'master'
                break
            elif branch['name'] == 'main':
                sha = branch['commit']['sha']
                branch_name = 'main'
                break
                
        if sha == '':
            print("NO MASTER OR MAIN BRANCH FOUND!!!!")
            print("May need to edit the code to read the second page of branches for this repository")
            # Manually found that all first branch pages for all
            # Kaggle repos contained either a master or main branch
            continue

        trees_url = repos[i]['trees_url'][:-6] + '/' + sha
        file_list = []
        page = requests.get(trees_url,headers=headers).json()
        path = 'https://raw.githubusercontent.com' + '/' + owner + '/' + repos[i]['name'] + '/' + branch_name
        add_to_file_list(page,path,file_list)

        for file in file_list:

            file_extension = ''
            for j in range(len(file) - 1,0,-1):
                if file[j] == '.':
                    # If you don't want certain types of file types
                    # or if you only want certain types of file types
                    # the logic can be added here!!!
                    not_code_files = []
                    if file_extension not in lines_per_lang[i] not in not_code_files:
                        lines_per_lang[i][file_extension] = 0
                    break
                elif file[j] == '/':
                    # If there is no file extension, only add the name after 
                    # the last slash to the dictionary if the name is
                    # 'Dockerfile'
                    if file_extension == 'Dockerfile':
                        if 'Dockerfile' not in lines_per_lang[i]:
                            lines_per_lang[i]['Dockerfile'] = 0
                    break
                else:
                    file_extension = file[j] + file_extension

            if file_extension in lines_per_lang[i]:
                line_count = 0
                for line in requests.get(file,headers=headers).iter_lines():
                    line_count += 1

                lines_per_lang[i][file_extension] += line_count

        for lang in lines_per_lang[i].keys():
            print('Number of lines of', lang, ':',str(lines_per_lang[i][lang]))
            individualRepoStats.write('Number of lines of ' + lang + ':' + str(lines_per_lang[i][lang]) + '\n')

        individualRepoStats.write('\n\n')


    individualRepoStats.close()

    lines_per_lang_overall = {}
    for i in range(len(lines_per_lang)):
        for lang in lines_per_lang[i].keys():
            if lang not in lines_per_lang_overall:
                count_list = []
                for j in range(i):
                    count_list.append(0)
                count_list.append(lines_per_lang[i][lang])
                lines_per_lang_overall[lang] = count_list
            else:
                while len(lines_per_lang_overall[lang]) < i:
                    lines_per_lang_overall[lang].append(0)
                lines_per_lang_overall[lang].append(lines_per_lang[i][lang])

    proper_list_length = len(lines_per_lang)
    for lang in lines_per_lang_overall.keys():
        while len(lines_per_lang_overall[lang]) < proper_list_length:
            lines_per_lang_overall[lang].append(0)


    num_commits = np.asarray(num_commits)
    num_stars = np.asarray(num_stars)
    num_contributors = np.asarray(num_contributors)
    num_branches = np.asarray(num_branches)
    num_tags = np.asarray(num_tags)
    num_forks = np.asarray(num_forks)
    num_releases = np.asarray(num_releases)
    num_closed_issues = np.asarray(num_closed_issues)
    num_environments = np.asarray(num_environments)



    with open('overallStats.txt','w') as overallStatsFile:
        overallStatsFile.write('Total,Median\n')
        overallStatsFile.write('Number of Commits:'+ str(np.sum(num_commits))+','+ str(np.median(num_commits))+'\n')
        overallStatsFile.write('Number of Stars:'+ str(np.sum(num_stars))+','+ str(np.median(num_stars))+'\n')
        overallStatsFile.write('Number of Contributors:'+ str(np.sum(num_contributors))+','+ str(np.median(num_contributors))+'\n')
        overallStatsFile.write('Number of Branches:'+ str(np.sum(num_branches))+','+ str(np.median(num_branches))+'\n')
        overallStatsFile.write('Number of Tags:'+ str(np.sum(num_tags))+','+ str(np.median(num_tags))+'\n')
        overallStatsFile.write('Number of Forks:'+ str(np.sum(num_forks))+','+ str(np.median(num_forks))+'\n')
        overallStatsFile.write('Number of Releases:'+ str(np.sum(num_releases))+','+ str(np.median(num_releases))+'\n')
        overallStatsFile.write('Number of Closed Issues:'+ str(np.sum(num_closed_issues))+','+ str(np.median(num_closed_issues))+'\n')
        overallStatsFile.write('Number of Environments:'+ str(np.sum(num_environments))+','+ str(np.median(num_environments))+'\n')

        for lang in lines_per_lang_overall.keys():
            sum = str(np.sum(np.asarray(lines_per_lang_overall[lang])))
            median = str(np.median(np.asarray(lines_per_lang_overall[lang])))
            overallStatsFile.write('Number of lines of ' + lang + ':' + sum +',' + median+'\n')

if __name__ == "__main__":
    getKaggleGitHubRepoStats()
