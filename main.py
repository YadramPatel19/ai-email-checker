from agents import run_all_agents
import os
from datetime import datetime


# ==============================================================
# HELPER — Extract score from agent response
# ==============================================================

def extract_score(raw_text: str) -> int:
    for line in raw_text.splitlines():
        if line.strip().upper().startswith("SCORE:"):
            score_part = line.split(":", 1)[1].strip()
            digits = "".join(ch for ch in score_part if ch.isdigit())
            if digits:
                return min(int(digits), 100)
    return 0


# ==============================================================
# HELPER — Validate email input
# ==============================================================

def validate_email(subject: str, email_body: str) -> str:
    """
    Returns an error message string if invalid, or empty string if valid.
    """
    if not subject or len(subject.strip()) < 3:
        return "Subject line is too short. Please enter a proper subject."

    word_count = len(email_body.strip().split())
    if word_count < 15:
        return f"Email body is too short ({word_count} words). Please enter at least 15 words."

    if len(email_body.strip()) > 5000:
        return "Email body is too long (max 5000 characters). Please shorten it."

    return ""  # no error


# ==============================================================
# STEP 1 — Collect email input from user
# ==============================================================

def get_email_input():
    print("\n" + "="*60)
    print("   AI EMAIL CHECKER")
    print("   Tata Steel — Corporate Communications")
    print("="*60)

    # Subject
    print("\n📌 Enter the email SUBJECT LINE:")
    subject = input("   > ").strip()

    # Body
    print("\n📝 Enter the EMAIL BODY.")
    print("   Press ENTER twice when you are done:\n")
    lines = []
    while True:
        line = input()
        if line == "":
            if lines:
                break
        else:
            lines.append(line)
    email_body = "\n".join(lines)

    # Validate
    error = validate_email(subject, email_body)
    if error:
        print(f"\n⚠️  {error}\n")
        return None, None, None   # signal to retry

    # Recipient
    print("\n👤 Who is this email being sent to?")
    print("   1 — Internal employee / colleague")
    print("   2 — External client / customer")
    print("   3 — Vendor or supplier")
    print("   4 — Regulatory / government body")
    print("   5 — Senior management / Board / C-suite")

    while True:
        choice = input("\n   Enter a number (1 to 5): ").strip()
        if choice in ["1", "2", "3", "4", "5"]:
            break
        print("   ⚠️  Please enter a number between 1 and 5.")

    recipient_map = {
        "1": "Internal employee or colleague",
        "2": "External client or customer",
        "3": "Vendor or supplier",
        "4": "Regulatory or government body",
        "5": "Senior management, Board, or C-suite executive"
    }
    recipient = recipient_map[choice]
    return subject, email_body, recipient


# ==============================================================
# STEP 2 — Save results to a .txt report file
# ==============================================================

def save_report(subject: str, recipient: str, results: list, overall: int):
    """
    Saves the full analysis to a timestamped .txt file
    inside a 'reports' folder.
    """
    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    # Make a filename using current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"reports/report_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("  AI EMAIL CHECKER — TATA STEEL\n")
        f.write(f"  Date    : {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n")
        f.write(f"  Subject : {subject}\n")
        f.write(f"  Recipient: {recipient}\n")
        f.write("="*60 + "\n\n")

        for result in results:
            f.write(f"\n{'─'*60}\n")
            f.write(f"  {result['agent']}\n")
            f.write(f"{'─'*60}\n")
            f.write(result['raw'] + "\n")

        f.write(f"\n{'='*60}\n")
        f.write(f"  OVERALL SCORE : {overall} / 100\n")
        f.write("="*60 + "\n")

    return filename


# ==============================================================
# STEP 3 — Display results in terminal
# ==============================================================

def display_results(results: list):
    print("\n\n" + "="*60)
    print("   ANALYSIS RESULTS")
    print("="*60)

    scores = []

    for result in results:
        raw = result["raw"]
        score = extract_score(raw)
        scores.append(score)

        print(f"\n{'─'*60}")
        print(f"  {result['agent']}")
        print(f"{'─'*60}")
        for line in raw.splitlines():
            print(f"  {line}")

    overall = sum(scores) // len(scores) if scores else 0

    if overall >= 80:
        verdict = "✅ Great — Ready to send!"
    elif overall >= 60:
        verdict = "⚠️  Okay — Fix a few things first."
    elif overall >= 40:
        verdict = "❌ Needs significant improvement."
    else:
        verdict = "🚫 Do NOT send — Major issues found."

    print(f"\n{'='*60}")
    print(f"  📊 OVERALL SCORE : {overall} / 100")
    print(f"  {verdict}")
    print(f"{'='*60}\n")

    return overall


# ==============================================================
# MAIN — Ties everything together
# ==============================================================

def main():
    while True:
        subject, email_body, recipient = get_email_input()

        # If validation failed, ask again
        if subject is None:
            retry = input("Try again? (y / n): ").strip().lower()
            if retry != "y":
                break
            continue

        # Run all agents
        results = run_all_agents(subject, email_body, recipient)

        # Show results and get overall score
        overall = display_results(results)

        # Save to file
        filename = save_report(subject, recipient, results, overall)
        print(f"💾 Report saved to: {filename}\n")

        # Check another?
        again = input("🔄 Check another email? (y / n): ").strip().lower()
        if again != "y":
            print("\n👋 Goodbye! Good luck with your Tata Steel internship!\n")
            break


if __name__ == "__main__":
    main()