def parse_message(text, notion):
    text = text.lower()
    if text.startswith("lookup"):
        name = text.replace("lookup", "", 1).strip()
        return notion.lookup_company(name)
    elif "search" in text:
        keyword = text.split("search", 1)[-1].strip()
        return notion.search_companies(keyword)
    elif "met" in text and "at" in text:
        # e.g., "I met AcmeAI at Demo Day"
        return notion.log_meeting(text)
    else:
        return "Sorry, I didn't understand that. Try 'lookup', 'search', or 'log'." 