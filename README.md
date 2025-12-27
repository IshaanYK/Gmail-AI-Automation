# 🤖 Gmail AI Inbox Assistant (v4.0)

An intelligent Python-based automation suite that triages Gmail inboxes, manages digital storage, and provides real-time reporting via HTML and WhatsApp.

## 🚀 Key Features

- **Intelligent Triage:** Uses weighted scoring logic to Star important emails (Bank, Jobs, Gov) and Trash junk (Social, Newsletters).
- **Humanized Auto-Response:** Detects personal emails and sends a polite, friendly reply during off-hours.
- **Smart Attachment Sorting:** Automatically downloads attachments to specific folders on `E:/` drive based on content category (Career, Finance, Education).
- **Automated Storage Lifecycle:** Files older than 30 days are automatically zipped to save space, and archives older than 60 days are permanently cleared.
- **Dual Reporting:** - **Visual Dashboard:** Generates a modern HTML report of the daily activity.
  - **WhatsApp Integration:** Sends a summary message directly to the user's WhatsApp Desktop app.

## 🛠️ Tech Stack

- **Python 3.x**
- **EZGmail:** For Gmail API interaction.
- **PyWhatKit:** For WhatsApp automation.
- **Plyer:** For desktop system notifications.
- **HTML/CSS:** For visual reporting dashboards.

## 📁 Project Structure

- `my_bot.pyw`: The main automation engine.
- `bot_log.txt`: Historical activity log.
- `daily_report.html`: Visual status dashboard.
- `replied_senders.txt`: Tracking file for auto-reply logic.

## ⚙️ Setup & Installation

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/IshaanYK/Gmail-AI-Automation.git](https://github.com/IshaanYK/Gmail-AI-Automation.git)
