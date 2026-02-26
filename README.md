# 🏏 Cricket AI Dashboard — Local Setup


## 📁 Files
```
cricket-app/
├── server.py       ← Python proxy server (fixes CORS)
├── dashboard.html  ← Dashboard UI
└── README.md
```
## Important — Regenerate Your Keys!
Since your keys were shared in this chat, please reset them:
# Key         # Where to regenerate
Cricket       Datacricketdata.org → Login → API Keys → Regenerate
Groqc         onsole.groq.com → API Keys →  Create new

## 🚀 Run in 2 steps

### Step 1 — Start the server
```bash
cd cricket-app
python server.py
```
You should see:
```
✅  Running at: http://localhost:5000
```

### Step 2 — Open the dashboard
Open your browser and go to:
```
http://localhost:5000
```

That's it! Live cricket scores will load automatically.

## 🤖 AI Questions (Groq — Free)
Type any question in the AI box, e.g.:
- "Who is batting best?"
- "What does India need to win?"
- "Summarize today's matches"

## 🔑 API Keys (already pre-filled)
- CricketData.org key is in `server.py`
- Groq key is in `dashboard.html`

> ⚠️ Regenerate both keys at cricketdata.org and console.groq.com.
