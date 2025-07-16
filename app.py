from slack_bolt import App
from dotenv import load_dotenv
import os
from notion_helper import NotionHelper
from parser import parse_message

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"],
          signing_secret=os.environ["SLACK_SIGNING_SECRET"])

notion = NotionHelper()

@app.event("app_mention")
def handle_mention(event, say):
    text = event.get('text', '')
    response = parse_message(text, notion)
    say(response)

if __name__ == "__main__":
    app.start(port=3000)
