#This script permits to synchronize Sonarqube projects/groups/permissions. To make it work, you need to add your sonars and github personnal token
from github import Github
#add your github personnal token
g = Github("")

from sonarqube import SonarQubeClient
#add your sonar personnal token 
s = SonarQubeClient(sonarqube_url="", token='') #add your sonar token + url of your sonar instance

org_name = "" #add your org name
if(s.alm_settings.get('github')) == None:
    clientid="" #add the clientId
    clientsecret = "" #add the clientSecret
    s.settings.update_setting_value(key='sonar.auth.github.enabled', value="true") #permits to enable the authentification with github
    s.settings.update_setting_value(key='sonar.auth.github.clientId.secured', value=clientid) 
    s.settings.update_setting_value(key='sonar.auth.github.clientSecret.secured', value=clientsecret) 
    s.settings.update_setting_value(key='sonar.auth.github.allowUsersToSignUp', value="true")
    s.settings.update_setting_value(key='sonar.auth.github.groupsSync', value="true") #synchronize the groups between sonar and github
    s.settings.update_setting_value(key='sonar.auth.github.organizations', values=org_name)
    with open('') as file: #replace with yours
        privatekey = file.read()
    s.alm_settings.create_github(appId = "202099", clientId=clientid, clientSecret=clientsecret, key="github", privateKey=privatekey, url="https://api.github.com/")
org = g.get_organization(org_name)
for team in org.get_teams():
    group_name = org_name +"/" +team.name
    group_exist = False
    groups = list(s.user_groups.search_user_groups())
    for group in groups:
        if group_name == group['name']:
            group_exist = True
    if group_exist == False:
        s.user_groups.create_group(name=group_name, description=team.name)
    
    for repo in team.get_repos():
        project_exist = False
        projectstr = repo.full_name.split('/')
        projectName = projectstr[1]
        projects = s.projects.search_projects()
        for project in projects:
            if projectName == project['name']:
                project_exist = True
        if project_exist == False:
            s.projects.create_project(project=projectName, name=projectName, visibility="private")
        s.permissions.add_permission_to_group(groupName= org_name + "/"+ team.name, permission="scan", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + team.name, permission="codeviewer", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + team.name, permission="user", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + team.name, permission="issueadmin", projectKey=projectName)
        s.permissions.add_permission_to_group(groupName= org_name + "/" + team.name, permission="securityhotspotadmin", projectKey=projectName)

admin_group_name = "" #add the name of the github team who would be admin of your sonar instance
s.permissions.add_permission_to_group(groupName= org_name + "/" + admin_group_name, permission="admin")

