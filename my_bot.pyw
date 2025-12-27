import ezgmail
import datetime
import os
from plyer import notification

# 1. Initialize
ezgmail.init()

# Change directory to where the script is located so it finds token.json
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def logger(message):
    """Writes bot actions to bot_log.txt"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("bot_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def intelligent_manager():
    logger("--- STARTING NIGHTLY SCAN ---")
    counts = {"starred": 0, "trashed": 0, "archived": 0, "personal": 0}

    # Define Safe/Personal list
    safe_emails = ['sir_email@company.com']

    unread_threads = ezgmail.search('is:unread label:inbox')

    for t in unread_threads:
        msg = t.messages[0]
        sender = msg.sender.lower()
        subject = msg.subject.lower()

        # Check if Personal
        is_automated = any(x in sender for x in ['noreply', 'info@', 'support@', 'news', 'digest'])

        if sender in safe_emails or (not is_automated and '@gmail.com' in sender):
            t.markAsRead()
            counts["personal"] += 1
            logger(f"👤 PERSONAL: Left alone -> {sender}")
            continue

            # Scoring Logic
        priority_score = 0
        if any(x in sender for x in ['mygov', 'sbi', 'icici', 'internshala', 'naukri']): priority_score += 15
        if any(x in subject for x in ['urgent', 'otp', 'loan', 'accepted']): priority_score += 10
        if any(x in sender for x in ['quora', 'reddit', 'youtube', 'newsletter']): priority_score -= 20

        # Actions
        if priority_score >= 10:
            t.addLabel('STARRED')
            t.markAsRead()
            counts["starred"] += 1
            logger(f"⭐ STARRED: {subject[:30]}")
        elif priority_score <= -10:
            t.trash()
            counts["trashed"] += 1
            logger(f"🗑️ TRASHED: {subject[:30]}")
        else:
            t.markAsRead()
            t.removeLabel('INBOX')
            counts["archived"] += 1
            logger(f"📦 ARCHIVED: {subject[:30]}")

    logger(f"FINISH: Starred {counts['starred']}, Trashed {counts['trashed']}, Personal {counts['personal']}")

    # Desktop Notification
    notification.notify(
        title="Gmail Bot Success",
        message=f"Starred: {counts['starred']} | Trashed: {counts['trashed']}",
        timeout=5
    )


if __name__ == "__main__":
    try:
        intelligent_manager()
    except Exception as e:
        logger(f"❌ CRITICAL ERROR: {str(e)}")