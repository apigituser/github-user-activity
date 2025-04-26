import requests
import json
import sys

def fetch_url(url):
    response = requests.get(url)
    with open("response.json", "w") as file:
        json.dump(response.json(), file)

def parse_data():
    with open("response.json") as file:
        data = json.load(file)

        for i in range(10):
            user = data[i]['actor']['login']
            repo = data[i]['repo']['name']
            eventType = data[i]['type']
            print(f"[{eventType}]")

            match eventType:
                case "IssuesEvent":
                    action = data[i]['payload']['action']
                    print(f"{user} {action} an issue in {repo}")
                case "PushEvent":
                    print(f"{user} pushed changes to {repo}")
                case "PullRequestEvent":
                    print(f"{user} made a pull request to {repo}")
                case "CreateEvent":
                    ref = data[i]['payload']['ref']
                    refType = data[i]['payload']['ref_type']
                    if refType == "branch":
                        print(f"{user} created a {refType} named {ref}")
                case "DeleteEvent":
                    ref = data[i]['payload']['ref']
                    refType = data[i]['payload']['ref_type']
                    if refType == "branch":
                        print(f"{user} deleted the {refType} named {ref}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No link provided")
        exit(1)
    url = sys.argv[1]
    fetch_url(url)
    parse_data()
    