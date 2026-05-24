from utils import call_llm


# ==============================================================
# AGENT 1 — TONE ANALYZER
# Checks if the email sounds professional and appropriate
# ==============================================================

def tone_agent(email_body: str, recipient: str) -> dict:
    prompt = f"""
You are a corporate email tone analyzer working for Tata Steel, 
a major steel manufacturing company in India.

Your job is to analyze the tone and professionalism of emails 
before they are sent to: {recipient}

Here is the email to analyze:
-------------------------------
{email_body}
-------------------------------

Give your analysis in this EXACT format (copy the format exactly, 
fill in the values):

SCORE: <a number from 0 to 100>
VERDICT: <one of: Excellent / Good / Needs Work / Poor>
TONE DETECTED: <describe the tone in a few words, e.g. "too casual", "aggressive", "professional">
ISSUES:
- <describe issue 1>
- <describe issue 2>
POSITIVES:
- <something done well>
TIP: <one specific actionable suggestion to improve the tone>

Do not add any extra explanation outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "🎭  Tone Analyzer",
        "raw": response
    }


# ==============================================================
# AGENT 2 — COMPLIANCE CHECKER
# Checks for legal risks, data leaks, policy violations
# ==============================================================

def compliance_agent(email_body: str, recipient: str) -> dict:
    prompt = f"""
You are a strict compliance officer at Tata Steel.
Your job is to check corporate emails for:
- Confidential information being shared with wrong people
- Legal or financial risks
- Sensitive data exposure (salary figures, plant costs, strategy)
- Inappropriate promises or commitments
- Regulatory violations

The email is being sent to: {recipient}

Here is the email:
-------------------------------
{email_body}
-------------------------------

Give your analysis in this EXACT format:

SCORE: <0 to 100, where 100 means fully compliant and safe>
RISK LEVEL: <one of: Low / Medium / High / Critical>
VERDICT: <one of: Compliant / Minor Issues / Serious Issues / Do Not Send>
FLAGS:
- <describe risk or flag 1>
- <describe risk or flag 2>
TIP: <one specific action to make this email safer and compliant>

Do not add any extra explanation outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "🛡️  Compliance Checker",
        "raw": response
    }


# ==============================================================
# AGENT 3 — CLARITY OPTIMIZER
# Checks if the email is easy to read and understand
# ==============================================================

def clarity_agent(email_body: str) -> dict:
    prompt = f"""
You are a business writing coach who specializes in corporate 
communication at large companies like Tata Steel.

Your job is to check if emails are clear, concise, and easy to 
understand. Look for:
- Confusing or vague sentences
- Overuse of jargon or technical terms
- Very long sentences that are hard to follow
- Passive voice used too much
- Missing key information (who, what, when, why)
- Poor structure or paragraph organization

Here is the email:
-------------------------------
{email_body}
-------------------------------

Give your analysis in this EXACT format:

SCORE: <0 to 100, where 100 means perfectly clear>
READABILITY: <one of: Very Easy / Easy / Moderate / Complex / Very Complex>
VERDICT: <one of: Crystal Clear / Good / Unclear / Confusing>
ISSUES:
- <clarity issue 1>
- <clarity issue 2>
REWRITE: <take the single most confusing sentence from the email 
and rewrite it in a clearer way. Show: Original: "..." → Improved: "...">
TIP: <one key thing the writer can do to improve clarity>

Do not add any extra explanation outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "✏️  Clarity Optimizer",
        "raw": response
    }


# ==============================================================
# AGENT 4 — SUBJECT LINE REVIEWER
# Checks if the subject line is effective and suggests better ones
# ==============================================================

def subject_agent(subject: str, email_body: str, recipient: str) -> dict:
    prompt = f"""
You are a corporate email subject line expert at Tata Steel.

Your job is to evaluate whether an email subject line is:
- Clear and specific (not vague like "Update" or "Hi")
- Professional and appropriate for the recipient
- The right length (not too short, not too long)
- Accurately representing the email content

The email is being sent to: {recipient}
Subject line: "{subject}"
Email content preview: {email_body[:400]}

Give your analysis in this EXACT format:

SCORE: <0 to 100>
VERDICT: <one of: Strong / Good / Weak / Poor>
ISSUES:
- <issue with current subject line>
ALTERNATIVES:
1. <better subject line option 1>
2. <better subject line option 2>
3. <better subject line option 3>
TIP: <explain why your first alternative is better than the original>

Do not add any extra explanation outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "📧  Subject Line Reviewer",
        "raw": response
    }


# ==============================================================
# ORCHESTRATOR — Runs all 4 agents and collects results
# This is what main.py calls
# ==============================================================

# ==============================================================
# AGENT 5 — SUMMARY AGENT
# Reads all 4 agent results and writes a final verdict
# ==============================================================

def summary_agent(all_results: list, subject: str, recipient: str) -> dict:
    """
    Takes the output of all 4 agents and produces a human-friendly
    final summary and recommendation.
    """
    # Combine all agent outputs into one block of text
    combined = ""
    for r in all_results:
        combined += f"\n\n{r['agent']}:\n{r['raw']}"

    prompt = f"""
You are the chief communication officer at Tata Steel.
You have received analysis from 4 AI agents about this email:

Subject: {subject}
Recipient: {recipient}

Here are the 4 agent reports:
{combined}

Based on all the above, write a short final summary for the email sender.
Use this EXACT format:

FINAL VERDICT: <one of: Send it / Send after minor edits / Rewrite needed / Do not send>
BIGGEST STRENGTH: <the best thing about this email in one sentence>
BIGGEST PROBLEM: <the most important issue to fix in one sentence>
ACTION PLAN:
1. <most important fix>
2. <second fix>
3. <third fix>
ENCOURAGEMENT: <one short motivating sentence for the writer>

Keep it short, clear, and helpful. No extra text outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "🏆  Final Summary (Chief Communication Officer)",
        "raw": response
    }

def run_all_agents(subject: str, email_body: str, recipient: str) -> list:
    print("\n" + "="*60)
    print("  STARTING MULTI-AGENT ANALYSIS")
    print("="*60)

    results = []

    print("\n  [1/5] 🎭  Tone Analyzer is running...")
    results.append(tone_agent(email_body, recipient))
    print("        ✅ Done!")

    print("  [2/5] 🛡️  Compliance Checker is running...")
    results.append(compliance_agent(email_body, recipient))
    print("        ✅ Done!")

    print("  [3/5] ✏️  Clarity Optimizer is running...")
    results.append(clarity_agent(email_body))
    print("        ✅ Done!")

    print("  [4/5] 📧  Subject Line Reviewer is running...")
    results.append(subject_agent(subject, email_body, recipient))
    print("        ✅ Done!")

    print("  [5/5] 🏆  Summary Agent is running...")
    results.append(summary_agent(results, subject, recipient))
    print("        ✅ Done!")

    print("\n  All 5 agents finished!")
    print("="*60)

    return results