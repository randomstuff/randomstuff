#!/usr/bin/python3

"""
CLI to GitHub API.

github-api --verbose stars johndoe
github-api --verbose followers johndoe
github-api --verbose following johndoe
github-api --verbose repos johndoe
github-api --verbose stargazers johndoe/helloworld
github-api --verbose forks johndoe/helloworld
github-api --verbose issues johndoe/helloworld
"""



import sys
import getpass
import github

# Config
verbose = False
login = None
password = None

def print_repo(repo):
    if verbose:
        sys.stdout.write(repo.full_name + "\t" + (repo.description or "") + "\n")
    else:
        sys.stdout.write(repo.full_name + "\n")

def print_issue(issue):
    if (verbose):
        sys.stdout.write(str(issue.id) + "\t" + (issue.title or "") + "\n")
    else:
        sys.stdout.write(str(issue.id) + "\n")

def print_user(user):
    if (verbose):
        sys.stdout.write(user.login + "\t" + (user.name or "") + "\n")
    else:
        sys.stdout.write(user.login + "\n")

# User commands:

def stars(args):
    for login in args:
        user = gh.get_user(login)
        for starred in user.get_starred():
            print_repo(starred)

def followers(args):
    for login in args:
        user = gh.get_user(login)
        for follower in user.get_followers():
            print_user(follower)

def following(args):
    for login in args:
        user = gh.get_user(login)
        for following in user.get_following():
            print_user(following)

def repos(args):
    for login in args:
        user = gh.get_user(login)
        for repo in user.get_repos():
            print_repo(repo)

def keys(args):
    for login in args:
        user = gh.get_user(login)
        for key in user.get_keys():
            sys.stdout.write(key.key + "\n")

# Repo commands:

def stargazers(args):
    for repo in args:
        repo = gh.get_repo(repo)
        for stargazer in repo.get_stargazers():
            print_user(stargazer)

def forks(args):
    for repo in args:
        repo = gh.get_repo(repo)
        for fork in repo.get_forks():
            print_repo(fork)

def issues(args):
    for repo in args:
        repo = gh.get_repo(repo)
        for issue in repo.get_issues():
            print_issue(issue)

commands = {
    "stars": stars,
    "followers": followers,
    "following": following,
    "repos": repos,
    "keys": keys,

    "stargazers": stargazers,
    "forks": forks,
    "issues": issues,
}

args = sys.argv[1:]
while len(args) != 0 and args[0][0] == "-":
    arg = args[0]
    if arg == "--verbose":
        verbose = True
        args = args[1:]
    elif arg == "--login":
        login = args[1]
        args = args[2:]
    else:
        sys.stderr.write("Unrecognized flag: " + arg + "\n");
        sys.exit(1);
if len(args) == 0:
    sys.stderr.write("Missing commnad");
    sys.exit(1);
command = commands[args[0]]
args = args[1:]

if login != None:
    password = getpass.getpass("Login for login " + login + ": ")
gh = github.Github(login_or_token=login, password=password, per_page=200)
command(args)
