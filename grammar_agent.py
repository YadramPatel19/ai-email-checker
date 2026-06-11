from utils import call_llm
import json
import re


def grammar_agent(text: str) -> dict:
    """
    Checks grammar and returns a corrections table
    with Original, Correction, and Explanation columns
    exactly like the output sample in the specification.
    """
    prompt = f"""
You are a professional grammar and style editor for corporate communications at Tata Steel.

Analyze this text and find ALL grammar, spelling, punctuation, style, and clarity errors.

TEXT TO ANALYZE:
{text}

Return ONLY a valid JSON array (no explanation, no markdown, no backticks).
Each item in the array must have exactly these three keys:
- "original": the original problematic phrase or sentence
- "correction": the corrected version
- "explanation": why this change was made

Example format:
[
  {{
    "original": "In case of any query, please mail to hr@company.com",
    "correction": "For any queries, please email hr@company.com.",
    "explanation": "Replaced 'In case of' with 'For' and 'mail to' with 'email' for conciseness and modern usage."
  }}
]

Find at least 3 corrections if they exist. Return empty array [] if text is perfect.
Return ONLY the JSON array, nothing else.
"""
    response = call_llm(prompt)

    # Clean and parse JSON
    try:
        clean = response.strip()
        clean = re.sub(r'```json|```', '', clean).strip()
        corrections = json.loads(clean)
        return {
            "agent": "📝  Grammar & Syntax Checker",
            "corrections": corrections,
            "raw": response
        }
    except Exception as e:
        return {
            "agent": "📝  Grammar & Syntax Checker",
            "corrections": [],
            "raw": response
        }


def alt_text_agent(has_images: bool, image_count: int) -> dict:
    """
    Suggests alt text guidelines for images in the email.
    """
    if not has_images:
        return {
            "agent": "🖼️  Image Alt Text Suggester",
            "raw": "No images detected in this email."
        }

    prompt = f"""
You are an accessibility expert for corporate email communications at Tata Steel.

This email contains {image_count} image(s).

Provide:
1. General best practices for writing alt text for corporate email images
2. Template alt text suggestions for common corporate email image types
   (logos, charts, product photos, infographics, signature images)

Keep it practical and specific to steel industry corporate communications.

Format your response clearly with sections.
"""
    response = call_llm(prompt)
    return {
        "agent": "🖼️  Image Alt Text Suggester",
        "raw": response
    }
def duplicate_content_agent(text: str) -> dict:
    """
    Detects repetitive or duplicate content in the email.
    """
    prompt = f"""
You are a corporate email editor at Tata Steel.

Analyze this email text and find:
1. Repeated words used too many times unnecessarily
2. Repeated phrases or sentences
3. Duplicate information mentioned more than once
4. Redundant expressions (e.g. "completely finished", "past history")

TEXT:
{text}

Respond in this EXACT format:

DUPLICATE PHRASES:
- <repeated phrase 1> (appears X times)
- <repeated phrase 2> (appears X times)

REDUNDANT EXPRESSIONS:
- <expression> → suggested fix: <better version>

OVERALL: <Clean / Minor repetition / Significant repetition>
SUGGESTION: <one tip to improve>

If no duplicates found, write "No repetitive content detected" under each section.
Do not add anything outside this format.
"""
    response = call_llm(prompt)
    return {
        "agent": "🔁  Duplicate Content Detector",
        "raw": response
    }