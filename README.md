# reddit-topic-tracker

A lightweight, open-source tool for tracking and analyzing topic trends across Reddit communities. Designed to help researchers, developers, and community enthusiasts discover relevant discussions and understand how conversations evolve over time.

---

## Features

- **Keyword Search** — Search posts and comments across multiple subreddits by keyword or phrase
- **Trend Analysis** — Track how topic popularity changes over days, weeks, and months
- **Engagement Metrics** — Rank posts by upvotes, comment count, and activity score
- **Cross-Subreddit Discovery** — Find communities actively discussing a given topic
- **User Activity Insights** — Identify users contributing most to a topic discussion
- **Export Support** — Save results as CSV or JSON for further analysis

---

## Use Cases

- Academic or market research on public discourse
- Community managers monitoring relevant conversations
- Developers building topic-aware Reddit bots or dashboards
- Anyone looking to find where their interests are being discussed on Reddit

---

## How It Works

The tool uses Reddit's official API (OAuth2) to perform **read-only** requests against public subreddit data. It never posts, votes, sends messages, or modifies any content. All data collected is publicly accessible on Reddit.

**Authentication flow:**
1. Register a Reddit app at https://www.reddit.com/prefs/apps
2. Provide your `client_id` and `client_secret` in the config file
3. The tool authenticates via OAuth2 and begins collecting data within API rate limits

---

## Getting Started

### Requirements

- Python 3.8+
- A Reddit account with a registered app (script type)

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/reddit-topic-tracker.git
cd reddit-topic-tracker
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=reddit-topic-tracker/1.0 by u/your_username
```

### Usage

```bash
# Search posts by keyword
python tracker.py --keyword "machine learning" --subreddit "MachineLearning" --limit 100

# Track topic trends over the past week
python tracker.py --keyword "climate change" --timeframe week --sort top

# Export results
python tracker.py --keyword "gaming setup" --export csv
```

---

## API Compliance

This tool is built in full compliance with Reddit's API Terms of Service and the [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

- All requests are authenticated via OAuth2
- Rate limits are respected (max 60 requests/minute)
- No private, NSFW, or login-protected content is accessed
- No automated posting, voting, or messaging

---

## Project Status

Currently in active development. Contributions and feedback welcome.

---

## License

MIT License — free to use, modify, and distribute.
