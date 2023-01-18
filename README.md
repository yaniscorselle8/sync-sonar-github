This script permits to : 
- add github SSO authentification inside sonar
- create of all your github teams inside sonar (as sonar groups)
- create a project on sonar for all your github repos (required for next step because repos needs to be created to synchronize the rights)
- synchronize the rights on sonar projects with those on github repos


To make this script work, you need to : 
- create a github personnal token and add it inside g = Github("") : line 4 of the script
- create a sonar token + add it and your sonar instance url inside s = sonarqubeClient var : line 8 of the script
- add your organization name line 10
- add the clientid line 12
- add the clientSecret line 13
- add the path to your github app private key line 20
- add the name of the github team who would have administration rights on your sonar instance line 50
