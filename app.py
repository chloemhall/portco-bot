import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
load_dotenv()
from notion_helper import (
    query_company_by_name,
    search_companies,
    search_by_keyword,
    search_by_sector,
    format_results,
    get_help_recommendations
)

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    text = event["text"].strip()
    lower_text = text.lower()

    # 1️⃣ Help request
    if "help" in lower_text:
        parts = lower_text.split("help")
        if len(parts) < 2:
            return say("Please provide a company name, e.g. '@PortCo bot how can I help Acme Biotech'.")

        company_name = parts[1].strip().title()
        help_data = get_help_recommendations(company_name)

        if not help_data.get("results"):
            return say(f"Couldn't find any help suggestions for *{company_name}*.")

        lines = [f"*How to help {company_name}*"]
        for page in help_data["results"]:
            props = page["properties"]
            help_type = props.get("How to help", {}).get("select", {}).get("name", "Unspecified")
            details_field = props.get("Details", {}).get("rich_text", [])
            details = details_field[0]["text"]["content"] if details_field else "No details provided"
            lines.append(f"\u2022 *{help_type}* — {details}")

        return say("\n".join(lines))

    # 2️⃣ Advanced search: e.g. "Raising + AI"
    if "+" in text:
        parts = text.split("+")
        fundraising_status = parts[0].replace("@portco bot", "").strip().title()
        keyword = parts[1].strip()
        data = search_companies(fundraising_status, keyword)
        return say(format_results(data))

    # 3️⃣ Sector keyword detection
    known_sectors = ["Robotics", "Life Sciences", "DeepTech", "Advanced Materials"]
    for sector in known_sectors:
        if sector.lower() in lower_text:
            data = search_by_sector(sector)
            return say(format_results(data))

    # 4️⃣ General keyword search
    known_keywords = ["cancer", "bio", "protein", "ai"]
    for keyword in known_keywords:
        if keyword in lower_text:
            data = search_by_keyword(keyword)
            return say(format_results(data))

    # 5️⃣ Fallback: try to match company name exactly
    parts = text.split()
    if len(parts) <= 1:
        return say("Please provide a company name.")

    company_input = " ".join(parts[1:]).strip().title()
    data = query_company_by_name(company_input)

    if data.get("results"):
        page = data["results"][0]
        props = page["properties"]

        def get_text(prop, key="rich_text"):
            if prop not in props:
                return "N/A"
            arr = props[prop].get(key, [])
            return arr[0]["text"]["content"] if arr else "N/A"

        def get_select_or_status(prop):
            if prop not in props:
                return "N/A"
            if "select" in props[prop] and props[prop]["select"]:
                return props[prop]["select"].get("name", "N/A")
            if "status" in props[prop] and props[prop]["status"]:
                return props[prop]["status"].get("name", "N/A")
            return "N/A"

        company = get_text("Company Name", "title")
        about = get_text("About")
        sector = get_select_or_status("Sector")
        fundraising = get_select_or_status("Fundraising Status")
        stage = get_select_or_status("Stage")
        high_level = get_text("High-level")
        technical_summary = get_text("Technical summary")
        pitch_files = props.get("Deck", {}).get("files", [])
        if pitch_files:
            file_obj = pitch_files[0]
            pitch_deck_url = file_obj["file"]["url"]
            pitch_deck_name = file_obj["name"]
            pitch_deck_line = f"• *Pitch Deck:* <{pitch_deck_url}|{pitch_deck_name}>"
        else:
            pitch_deck_line = "• *Pitch Deck:* Not available"

        return say(f"""
*{company}*
• *About:* {about}
• *Sector:* {sector}
• *Fundraising Status:* {fundraising}
• *Stage:* {stage}
• *High-level:* {high_level}
• *Technical summary:* {technical_summary}
• {pitch_deck_line}
        """)
    else:
        # 6️⃣ If no match, do keyword fallback
        keyword_fallback = search_by_keyword(company_input)
        return say(format_results(keyword_fallback))

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("\u26a1\ufe0f PortCo Bot is running in Socket Mode!")
    handler.start()
