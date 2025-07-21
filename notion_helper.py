import os
import requests
print("HELP DB:", os.environ.get("NOTION_HELP_DATABASE_ID")) 
NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def query_company_by_name(company_name):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Company Name",
            "title": {
                "equals": company_name
            }
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()

def search_companies(fundraising_status, keyword):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Fundraising Status",
                    "status": {
                        "equals": fundraising_status
                    }
                },
                {
                    "or": [
                        {
                            "property": "Technical summary",
                            "rich_text": {"contains": keyword}
                        },
                        {
                            "property": "About",
                            "rich_text": {"contains": keyword}
                        },
                        {
                            "property": "High-level",
                            "rich_text": {"contains": keyword}
                        }
                    ]
                }
            ]
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()
def search_by_keyword(keyword):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "or": [
                {
                    "property": "Technical summary",
                    "rich_text": {
                        "contains": keyword
                    }
                },
                {
                    "property": "High-level",
                    "rich_text": {
                        "contains": keyword
                    }
                },
                {
                    "property": "About",
                    "rich_text": {
                        "contains": keyword
                    }
                }
            ]
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()
def search_by_sector(sector_tag):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": "Sector",
            "multi_select": {
                "contains": sector_tag
            }
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()
def format_results(data):
    if not data.get("results"):
        return "No matching companies found."

    output = []
    for page in data["results"]:
        props = page["properties"]
        name = props["Company Name"]["title"][0]["text"]["content"]
        about = props.get("About", {}).get("rich_text", [])
        about_text = about[0]["text"]["content"] if about else "No summary"
        output.append(f"*{name}* — {about_text}")
    return "\n".join(output)

def get_help_recommendations(company_name):
    NOTION_HELP_DB = os.environ.get("NOTION_HELP_DATABASE_ID")
    if NOTION_HELP_DB is None:
        raise EnvironmentError("❌ NOTION_HELP_DATABASE_ID is not set.")

    url = f"https://api.notion.com/v1/databases/{NOTION_HELP_DB}/query"
    payload = {
        "filter": {
            "property": "Text Name",  # 👈 matches your new rollup column
            "rich_text": {
                "contains": company_name
            }
        }
    }
    res = requests.post(url, headers=HEADERS, json=payload)
    return res.json()

