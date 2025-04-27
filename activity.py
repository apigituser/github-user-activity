import requests
import json
import sys

def fetch_url(url):
    response = requests.get(url)
    if len(response.json()) == 0:
        return 1
    with open("response.json", "w") as file:
        json.dump(response.json(), file)

def parse_data():
    with open("response.json") as file:
        data = json.load(file)

        for i in range(9):
            repo = data[i]['repo']['name']
            eventType = data[i]['type']

            match eventType:
                case "IssuesEvent":
                    action = data[i]['payload']['action']
                    print(f"{action} an issue in {repo}")
                case "PushEvent":
                    print(f"pushed changes to {repo}")
                case "PullRequestEvent":
                    print(f"made a pull request to {repo}")
                case "CreateEvent":
                    ref = data[i]['payload']['ref']
                    refType = data[i]['payload']['ref_type']
                    if refType == "branch":
                        print(f"created a {refType} named {ref}")
                case "DeleteEvent":
                    ref = data[i]['payload']['ref']
                    refType = data[i]['payload']['ref_type']
                    if refType == "branch":
                        print(f"deleted the {refType} named {ref}")
                case "IssueCommentEvent":
                    title = data[i]['payload']['issue']['title']
                    print(f"commented on issue '{title}'")
                case "WatchEvent":
                    print(f"watching {repo}")
                case "ForkEvent":
                    print(f"forked {repo}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide a valid username")
        exit(1)
    username = sys.argv[1]
    url = "https://api.github.com/users/{}/events".format(username)
    
    if fetch_url(url) == 1:
        print("Invalid Username") 
    else:
        print("[RECENT GITHUB ACTIVITY OF " + username + "]\n")
        parse_data()
    