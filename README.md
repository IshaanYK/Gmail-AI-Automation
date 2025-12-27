# 📧 AI-Powered Gmail Manager

An intelligent automation script that uses weighted scoring logic to triage your inbox. It automatically Stars priority mail (like MyGov or Loans), Archives neutral mail, and Trashes social junk (like Quora).

## 🧠 Intelligence Logic
* **Priority Filter**: Senders like `MyGov`, `SBI`, or `Internshala` get a +15 score.
* **Trash Filter**: Social digests (Quora, Reddit) get a -20 score and go to the Bin.
* **Personal Protection**: Recognizes `@gmail.com` addresses to ensure human-to-human mail is never trashed.

## 🛠️ Setup
1. **Google API**: Place your `credentials.json` in the folder.
2. **Dependencies**: `pip install ezgmail plyer`
3. **Deployment**: Uses Windows Task Scheduler to run `my_bot.pyw` nightly.

## 📊 Automation Stats
The bot generates a `bot_log.txt` locally to track daily actions and sends Windows desktop notifications upon completion.
