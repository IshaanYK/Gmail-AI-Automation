import ezgmail
import datetime
import os
import zipfile
import webbrowser
import pywhatkit as kit  # New: Required for WhatsApp
from plyer import notification

# 1. Initialize
ezgmail.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- CONFIGURATION ---
BASE_DOWNLOAD_PATH = r'E:\gmail bot downloads'
ARCHIVE_PATH = r'E:\gmail bot downloads\old_archives'
REPLIED_LOG_FILE = "replied_senders.txt"
HTML_REPORT_FILE = "daily_report.html"
MY_PHONE_NUMBER = "+91XXXXXXXXXX"  # <-- CHANGE THIS to your WhatsApp number

def logger(message):
    """Logs actions with a timestamp"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("bot_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def send_whatsapp_summary(counts):
    """Sends the summary via WhatsApp Desktop App"""
    summary_text = (f"*Ishaan's Inbox Summary* 🤖\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"⭐ Starred: {counts['starred']}\n"
                    f"🗑️ Trashed: {counts['trashed']}\n"
                    f"👤 Personal: {counts['personal']}\n"
                    f"📦 Archived: {counts['archived']}\n"
                    f"━━━━━━━━━━━━━━━\n"
                    f"Report & Files Updated! ✅")
    try:
        # wait_time=15 gives the laptop enough time to switch to the WhatsApp App
        kit.sendwhatmsg_instantly(MY_PHONE_NUMBER, summary_text, wait_time=15, tab_close=True)
        logger("📱 WhatsApp Summary Sent successfully.")
    except Exception as e:
        logger(f"❌ WhatsApp Error: {str(e)}")

def generate_html_report(counts):
    """Creates a professional visual summary of the bot's work"""
    now = datetime.datetime.now().strftime('%B %d, %Y - %I:%M %p')
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ishaan's Inbox Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
            .container {{ width: 90%; max-width: 600px; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.15); }}
            h1 {{ color: #1a73e8; text-align: center; font-size: 28px; margin-bottom: 5px; }}
            .date {{ text-align: center; color: #777; margin-bottom: 30px; font-style: italic; }}
            .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
            .card {{ padding: 25px; border-radius: 12px; text-align: center; color: white; transition: transform 0.3s; }}
            .card:hover {{ transform: translateY(-5px); }}
            .starred {{ background: linear-gradient(135deg, #fbbc04, #f9a825); }}
            .trashed {{ background: linear-gradient(135deg, #ea4335, #c62828); }}
            .personal {{ background: linear-gradient(135deg, #34a853, #2e7d32); }}
            .archived {{ background: linear-gradient(135deg, #4285f4, #1565c0); }}
            .stat-val {{ font-size: 32px; display: block; margin-top: 10px; }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 0.85em; color: #888; border-top: 1px solid #eee; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Inbox Assistant Report</h1>
            <div class="date">Mission Accomplished: {now}</div>
            <div class="stat-grid">
                <div class="card starred">⭐ Starred<span class="stat-val">{counts['starred']}</span></div>
                <div class="card trashed">🗑️ Trashed<span class="stat-val">{counts['trashed']}</span></div>
                <div class="card personal">👤 Personal<span class="stat-val">{counts['personal']}</span></div>
                <div class="card archived">📦 Archived<span class="stat-val">{counts['archived']}</span></div>
            </div>
            <div class="footer">Bot Version 4.0 | <b>Secure & Intelligent</b> | Data saved to E: Drive</div>
        </div>
    </body>
    </html>
    """
    with open(HTML_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(html_template)
    webbrowser.open('file://' + os.path.realpath(HTML_REPORT_FILE))

def get_category(sender, subject):
    if any(x in sender for x in ['naukri', 'internshala', 'linkedin']): return 'career'
    elif any(x in sender for x in ['sbi', 'icici', 'hdfc', 'bank', 'finance']): return 'bank'
    elif any(x in subject for x in ['result', 'certificate', 'marksheet', 'exam']): return 'educational certificate'
    elif any(ext in subject for ext in ['.pdf', '.doc', '.docx']): return 'doc'
    else: return 'others'

def smart_cleanup():
    if not os.path.exists(ARCHIVE_PATH): os.makedirs(ARCHIVE_PATH)
    now = datetime.datetime.now()
    for folder in ['others', 'doc']:
        path = os.path.join(BASE_DOWNLOAD_PATH, folder)
        if not os.path.exists(path): continue
        for file in os.listdir(path):
            file_p = os.path.join(path, file)
            if os.path.isdir(file_p): continue
            if (now - datetime.datetime.fromtimestamp(os.path.getmtime(file_p))).days >= 30:
                zip_n = os.path.join(ARCHIVE_PATH, f"archive_{now.strftime('%Y_%m')}.zip")
                with zipfile.ZipFile(zip_n, 'a', zipfile.ZIP_DEFLATED) as zf:
                    zf.write(file_p, arcname=file)
                os.remove(file_p)
                logger(f"📦 ARCHIVED: {file}")

def download_attachments(msg, category):
    folder_path = os.path.join(BASE_DOWNLOAD_PATH, category)
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    for attachment in msg.attachments:
        if os.path.exists(os.path.join(folder_path, attachment)): continue
        msg.downloadAttachment(attachment, folder_path)
        logger(f"💾 SAVED: {attachment} in {category}")

def get_human_message():
    return (f"Hi there! This is personal assistant bot. 🤖\n\n"
            f"I've just sorted your email into Ishaan's priority list so he doesn't miss it. "
            f"Since it's currently outside his study hours, he'll get back to you personally soon!\n\n"
            f"Have a great day!")

def reset_weekly_log():
    if datetime.datetime.now().strftime('%A') == 'Monday':
        if os.path.exists(REPLIED_LOG_FILE):
            os.remove(REPLIED_LOG_FILE)

def has_replied_before(email):
    if not os.path.exists(REPLIED_LOG_FILE): return False
    with open(REPLIED_LOG_FILE, "r") as f: return email in f.read()

def mark_as_replied(email):
    with open(REPLIED_LOG_FILE, "a") as f: f.write(f"{email}\n")

def intelligent_manager():
    reset_weekly_log()
    smart_cleanup()
    logger("--- STARTING NIGHTLY SCAN ---")
    counts = {"starred": 0, "trashed": 0, "archived": 0, "personal": 0}
    safe_emails = ['sir_email@company.com']
    unread_threads = ezgmail.search('is:unread label:inbox')

    for t in unread_threads:
        msg = t.messages[0]
        sender, subject = msg.sender.lower(), msg.subject.lower()
        is_automated = any(x in sender for x in ['noreply', 'info@', 'support@', 'news', 'digest'])

        if sender in safe_emails or (not is_automated and '@gmail.com' in sender):
            t.markAsRead(); counts["personal"] += 1
            if msg.attachments: download_attachments(msg, get_category(sender, subject))
            if not has_replied_before(sender):
                msg.reply(get_human_message())
                mark_as_replied(sender)
            continue

        priority = 0
        if any(x in sender for x in ['mygov', 'sbi', 'icici', 'internshala', 'naukri']): priority += 15
        if any(x in subject for x in ['urgent', 'otp', 'loan', 'accepted']): priority += 10
        if any(x in sender for x in ['quora', 'reddit', 'youtube', 'newsletter']): priority -= 20

        if priority >= 10:
            t.addLabel('STARRED'); t.markAsRead(); counts["starred"] += 1
            if msg.attachments: download_attachments(msg, get_category(sender, subject))
        elif priority <= -10:
            t.trash(); counts["trashed"] += 1
        else:
            t.markAsRead(); t.removeLabel('INBOX'); counts["archived"] += 1

    generate_html_report(counts)
    send_whatsapp_summary(counts) # Trigger WhatsApp
    notification.notify(title="Gmail Bot Done", message="Report Sent to WhatsApp!", timeout=5)

if __name__ == "__main__":
    try:
        intelligent_manager()
    except Exception as e:
        logger(f"❌ CRITICAL ERROR: {str(e)}")
