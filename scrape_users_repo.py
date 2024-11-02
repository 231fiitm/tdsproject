import requests
import csv
import time

# Replace with your personal access token
ACCESS_TOKEN = "TOKEN"
BASE_URL = "https://api.github.com"
CITY = "Seattle"
MIN_FOLLOWERS = 200

HEADERS = {"Authorization": f"token {ACCESS_TOKEN}"}

def make_request(url, params=None):
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 403:
            print("[!] Rate limit hit. Waiting for 60 seconds...")
            time.sleep(60)  # Wait and retry
        elif response.status_code != 200:
            print(f"[ERROR] {response.status_code} - {response.json()}")
            return None
        else:
            return response.json()

def get_user_info(username):
    print(f"  [+] Fetching user info for: {username}")
    url = f"{BASE_URL}/users/{username}"
    return make_request(url)

def get_user_repos(username):
    url = f"{BASE_URL}/users/{username}/repos"
    repos = []
    page = 1

    while True:
        response = make_request(url, params={"page": page})

        if response is None:
            break

        print(f"Fetching page {page} for user {username}. Repos fetched: {len(response)}")

        if not response:
            break

        for repo in response:
            if isinstance(repo, dict):
                repos.append({
                    "login": username,
                    "full_name": repo.get("full_name", ""),
                    "created_at": repo.get("created_at", ""),
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "watchers_count": repo.get("watchers_count", 0),
                    "language": repo.get("language", ""),
                    "has_projects": repo.get("has_projects", False),
                    "has_wiki": repo.get("has_wiki", False),
                    "license_name": repo.get("license", {}).get("name", "") if repo.get("license") else None,        })

        page += 1

        if len(repos) >= 500:
            break

    return repos

def clean_company(company_name):
    return company_name.strip().lstrip("@").upper() if company_name else ""

def write_to_csv(data, filename, fieldnames):
    print(f"[+] Writing data to {filename}...")
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def main():
    users = []
    repositories = []
    page = 1

    while True:
        print(f"[+] Fetching users from page {page}...")
        user_url = f"{BASE_URL}/search/users"
        params = {"q": f"location:{CITY} followers:>{MIN_FOLLOWERS}", "page": page, "per_page": 100}
        data = make_request(user_url, params)

        if not data or not data.get("items"):
            print("[!] No more users found or failed to fetch data. Exiting...")
            break

        for item in data["items"]:
            user_info = get_user_info(item["login"])

            if user_info:
                user_info_filtered = {key: user_info.get(key, "") for key in [
                    "login", "name", "company", "location", "email", 
                    "hireable", "bio", "public_repos", "followers",
                    "following", "created_at"
                ]}
                user_info_filtered["company"] = clean_company(user_info_filtered.get("company"))
                users.append(user_info_filtered)
                print(f"  [+] User {item['login']} added with {user_info.get('followers', 0)} followers.")

                repos = get_user_repos(item["login"])
                repositories.extend(repos)

        page += 1
        time.sleep(1)
    print(f"[✔] Data collection complete. Users collected: {len(users)}, Repositories collected: {len(repositories)}. Files saved: users.csv, repositories.csv, README.md")

    user_fieldnames = [
        "login", "name", "company", "location", "email",
        "hireable", "bio", "public_repos", "followers",
        "following", "created_at"
    ]
    write_to_csv(users, "users.csv", user_fieldnames)

    repo_fieldnames = [
        "login", "full_name", "created_at", "stargazers_count",
        "watchers_count", "language", "has_projects",
        "has_wiki", "license_name"
    ]
    write_to_csv(repositories, "repositories.csv", repo_fieldnames)

    # Create README.md
    print("[+] Creating README.md...")
    with open("README.md", "w") as readme:
        readme.write(
            "## GitHub User Analysis in Seattle\n\n"
            "- This data was scraped using the GitHub API.\n"
            "- We found a surprising number of users in Seattle with over 200 followers working in various industries.\n"
            "- Developers in Seattle should consider contributing to open-source projects to increase visibility and networking opportunities.\n"
        )

    print(f"[✔] Data collection complete. Users collected: {len(users)}, Repositories collected: {len(repositories)}. Files saved: users.csv, repositories.csv, README.md")

if __name__ == "__main__":
    main()
