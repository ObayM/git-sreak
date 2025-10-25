import requests
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timezone

load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# GraphQL was much faster then the rest api so i used it
def get_latest_commit(username: str):

    query = f"""
    {{
      user(login: "{username}") {{
        repositories(first: 1, orderBy: {{field: PUSHED_AT, direction: DESC}}) {{
          nodes {{
            name
            defaultBranchRef {{
              target {{
                ... on Commit {{
                  messageHeadline
                  committedDate
                  url
                  oid
                }}
              }}
            }}
          }}
        }}
      }}
    }}
    """

    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

    data = response.json()

    try:
        repo_info = data["data"]["user"]["repositories"]["nodes"][0]
        commit_info = repo_info["defaultBranchRef"]["target"]
        repo_name = repo_info["name"]

    except (KeyError, IndexError, TypeError):
        raise Exception(f"something went wrong with '{username}'")

    return {
        "username": username,
        "repository": repo_name,
        "message": commit_info["messageHeadline"],
        "date": commit_info["committedDate"],
        "url": commit_info["url"],
        "oid": commit_info["oid"]
    }




def does_user_exist(githubHndle: str):
    url = f"https://api.github.com/users/{githubHndle}"
    response = requests.get(url)

    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
 

def is_the_commit_today(commit_date_str: str) -> bool:

    try:
        commit_dt = datetime.fromisoformat(commit_date_str.rstrip("Z")).replace(tzinfo=timezone.utc)
    except ValueError:
        commit_dt = datetime.fromisoformat(commit_date_str).astimezone(timezone.utc)

    now_utc = datetime.now(timezone.utc)

    return (commit_dt.year == now_utc.year and
            commit_dt.month == now_utc.month and
            commit_dt.day == now_utc.day)

# test

my_commit = get_latest_commit("ObayM")
print(my_commit)

print(is_the_commit_today(my_commit['date']))
print(does_user_exist("ObayM"))
# IT WOKRS yay