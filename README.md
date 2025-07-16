# portco-bot

A Slackbot for portfolio company lookup, search, and meeting note logging, integrated with Notion.

## Features
- Lookup a portfolio company by name
- Keyword-based fuzzy search (e.g. "AI companies")
- Log meeting notes ("I met AcmeAI at Demo Day")
- Clean Slack integration via Bolt
- Uses your existing Notion schema

## Setup

1. Clone the repo:
   ```sh
   git clone https://github.com/chloemhall/portco-bot.git
   cd portco-bot
   ```
2. Copy and fill in your environment variables:
   ```sh
   cp .env.example .env
   # Edit .env with your Slack and Notion tokens/IDs
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```sh
   python3 app.py
   ```
5. Expose your local server (e.g., with localhost.run or ngrok) and set the public URL in your Slack app config.

## Notion Mock Data
- See `notion-mock.json` for example companies and schema setup instructions.

## Development
- See `notion_helper.py` and `parser.py` for extension points.

## Security
- **Never commit your real `.env` file or tokens.** 