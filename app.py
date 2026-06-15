import streamlit as st
from agents import (
    tone_agent, compliance_agent, clarity_agent,
    subject_agent, summary_agent, rewriter_agent
)
from grammar_agent import grammar_agent, alt_text_agent, duplicate_content_agent
from extractor import (
    extract_from_pdf, extract_from_docx, extract_from_excel,
    extract_from_image, detect_emojis, extract_links,
    count_words, verify_links, extract_qr_links
)
from export_report import export_as_pdf, export_as_docx
from main import extract_score, save_report
from datetime import datetime
import os

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Email Checker — Tata Steel",
    page_icon="🏭",
    layout="wide"
)

st.markdown("# 🏭 AI Email Content Checker")
st.markdown("**Tata Steel — Corporate Communications** | 8-Agent AI Analysis")

# ══════════════════════════════════════════════════════════════
# FIX 2 — AI DISCLAIMER AT TOP (visible before any analysis)
# ══════════════════════════════════════════════════════════════
st.warning("""
⚠️ **AI-Generated Content Disclaimer**

This tool uses Artificial Intelligence (Llama 3.3 70B via Groq API) to analyze email content.
All suggestions, scores, corrections, and rewritten content are **AI-generated and AI-assisted**.

**Please note:**
- AI analysis may not be 100% accurate and should always be reviewed by a human
- Compliance and legal assessments are indicative only — consult your legal/compliance team for critical communications
- The rewritten email is a suggestion only — always review carefully before sending
- AI models may occasionally misinterpret context or industry-specific terminology
""")

st.divider()

# ══════════════════════════════════════════════════════════════
# INPUT SECTION
# ══════════════════════════════════════════════════════════════
col1, col2 = st.columns([2, 1])

with col1:
    subject = st.text_input(
        "📌 Email Subject Line",
        placeholder="e.g. Update on Q3 Plant Shutdown Schedule"
    )
    email_body = st.text_area(
        "📝 Email Body",
        placeholder="Paste or type your email content here...",
        height=200
    )

    st.markdown("#### 📎 Attachments (optional)")
    uploaded_files = st.file_uploader(
        "Upload PDF, Word, Excel, or Image/GIF files",
        type=["pdf", "docx", "xlsx", "png", "jpg", "jpeg", "gif"],
        accept_multiple_files=True
    )

with col2:
    recipient = st.selectbox(
        "👤 Recipient Type",
        [
            "Internal employee or colleague",
            "External client or customer",
            "Vendor or supplier",
            "Regulatory or government body",
            "Senior management, Board, or C-suite executive"
        ]
    )
    comm_type = st.selectbox(
        "📂 Communication Type",
        [
            "Operational update",
            "HR / People matter",
            "Safety notice",
            "Financial / Business update",
            "Legal / Compliance matter"
        ]
    )
    st.markdown("#### 🤖 Agents")
    st.markdown("""
    - 🎭 Tone Analyzer
    - 🛡️ Compliance Checker
    - ✏️ Clarity Optimizer
    - 📧 Subject Line Reviewer
    - 🏆 Summary Agent
    - ✍️ Email Rewriter
    - 📝 Grammar Checker
    - 🔁 Duplicate Detector
    - 🖼️ Alt Text Suggester
    """)

st.divider()
analyze = st.button(
    "🚀 Analyze & Improve Email",
    type="primary",
    use_container_width=True
)

# ══════════════════════════════════════════════════════════════
# ANALYSIS
# ══════════════════════════════════════════════════════════════
if analyze:
    # ── Validation ─────────────────────────────────────────────
    if not subject or len(subject.strip()) < 3:
        st.error("⚠️ Please enter a proper subject line.")
    elif len(email_body.strip().split()) < 5:
        st.error("⚠️ Email body is too short.")
    else:
        # ── Process uploaded files ─────────────────────────────
        extracted_texts = {}
        image_count = 0
        full_text = email_body
        links_found = extract_links(email_body)

        if uploaded_files:
            st.markdown("#### 📂 Processing uploaded files...")
            for f in uploaded_files:
                fname = f.name.lower()

                if fname.endswith(".pdf"):
                    t = extract_from_pdf(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                    links_found.extend(extract_links(t))

                elif fname.endswith(".docx"):
                    t = extract_from_docx(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                    links_found.extend(extract_links(t))

                elif fname.endswith(".xlsx"):
                    t = extract_from_excel(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t

                elif fname.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    t = extract_from_image(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                    image_count += 1

                    # QR code detection
                    f.seek(0)
                    qr_found = extract_qr_links(f)
                    if qr_found:
                        links_found.extend(qr_found)
                        st.info(
                            f"🔲 QR code detected in "
                            f"{f.name}: {', '.join(qr_found)}"
                        )

        # Remove duplicate links
        links_found = list(set(links_found))

        # ── Element detection ──────────────────────────────────
        emojis_found = detect_emojis(full_text)
        word_count = count_words(full_text)

        # ── Verify links ───────────────────────────────────────
        links_data = []
        if links_found:
            with st.spinner("🔗 Verifying hyperlinks..."):
                links_data = verify_links(links_found)

        # ── Run all agents ─────────────────────────────────────
        # FIX 1 — Using full_text (includes attachment content)
        # instead of email_body so agents analyze attachments too
        st.markdown("### ⚙️ Running Analysis...")
        progress = st.progress(0, text="Starting agents...")

        results = []

        progress.progress(8, text="🎭 Running Tone Analyzer...")
        results.append(tone_agent(full_text, recipient))

        progress.progress(20, text="🛡️ Running Compliance Checker...")
        results.append(compliance_agent(full_text, recipient))

        progress.progress(32, text="✏️ Running Clarity Optimizer...")
        results.append(clarity_agent(full_text))

        progress.progress(44, text="📧 Running Subject Line Reviewer...")
        results.append(subject_agent(subject, full_text, recipient))

        progress.progress(55, text="🏆 Running Summary Agent...")
        results.append(summary_agent(results, subject, recipient))

        progress.progress(65, text="✍️ Rewriting your email...")
        rewrite_result = rewriter_agent(full_text, subject, recipient, results)
        results.append(rewrite_result)

        progress.progress(75, text="📝 Checking grammar...")
        grammar_result = grammar_agent(full_text)
        corrections = grammar_result.get("corrections", [])

        progress.progress(85, text="🔁 Detecting duplicate content...")
        duplicate_result = duplicate_content_agent(full_text)

        progress.progress(93, text="🖼️ Generating alt text suggestions...")
        alt_result = alt_text_agent(image_count > 0, image_count)

        progress.progress(100, text="✅ All agents done!")

        # ── Calculate overall score ────────────────────────────
        scores = [extract_score(r["raw"]) for r in results[:4]]
        overall = sum(scores) // len(scores) if scores else 0

        st.divider()

        # ══════════════════════════════════════════════════════
        # TABS
        # ══════════════════════════════════════════════════════
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Analysis",
            "✍️ Improved Email",
            "📝 Grammar & Duplicates",
            "🔗 Links & Elements",
            "🏆 Summary",
            "⬇️ Export"
        ])

        # ══════════════════════════════════════════════════════
        # TAB 1 — Analysis Results
        # ══════════════════════════════════════════════════════
        with tab1:
            # Score metrics row
            s1, s2, s3, s4, s5 = st.columns(5)
            metric_data = [
                ("🎭 Tone", results[0]),
                ("🛡️ Compliance", results[1]),
                ("✏️ Clarity", results[2]),
                ("📧 Subject", results[3]),
            ]
            for col, (label, result) in zip([s1, s2, s3, s4], metric_data):
                sc = extract_score(result["raw"])
                with col:
                    st.metric(label, f"{sc}/100")
            with s5:
                st.metric("📊 Overall", f"{overall}/100")

            # Overall score bar and verdict
            st.progress(overall / 100)
            if overall >= 80:
                st.success("✅ Great — Ready to send!")
            elif overall >= 60:
                st.warning("⚠️ Okay — Fix a few things first.")
            elif overall >= 40:
                st.error("❌ Needs significant improvement.")
            else:
                st.error("🚫 Do NOT send — Major issues found.")

            # Email statistics
            st.divider()
            st.markdown("#### 📊 Email Statistics")
            ec1, ec2, ec3, ec4 = st.columns(4)
            with ec1:
                st.metric("📝 Word Count", word_count)
            with ec2:
                st.metric("😊 Emojis", len(emojis_found))
            with ec3:
                st.metric("🔗 Links", len(links_found))
            with ec4:
                subj_len = len(subject)
                st.metric(
                    "📌 Subject Length",
                    f"{subj_len} chars",
                    delta="✅ Good" if subj_len <= 60 else "⚠️ Too long",
                    delta_color="normal" if subj_len <= 60 else "inverse"
                )

            if emojis_found:
                st.warning(
                    f"Emojis detected: {' '.join(emojis_found)} — "
                    f"use sparingly in corporate emails."
                )

            # Individual agent result cards
            st.divider()
            st.markdown("#### 🤖 Agent Reports")

            # FIX 1 — Show attachment analysis notice
            if extracted_texts:
                st.info(
                    f"✅ **Attachment Analysis Included** — "
                    f"Content from {len(extracted_texts)} uploaded file(s) "
                    f"has been included in all agent analysis above. "
                    f"Scores and feedback reflect both email body and attachment content."
                )

            for i in range(4):
                sc = extract_score(results[i]["raw"])
                icon = "🟢" if sc >= 80 else "🟡" if sc >= 60 else "🔴"
                with st.expander(
                    f"{icon} {results[i]['agent']} — {sc}/100",
                    expanded=False
                ):
                    st.text(results[i]["raw"])

            # Extracted file content viewer
            if extracted_texts:
                st.divider()
                st.markdown("#### 📎 Text Extracted from Attachments")
                st.caption(
                    "The following text was extracted from your uploaded files "
                    "and included in the AI analysis above."
                )
                for fname, text in extracted_texts.items():
                    with st.expander(f"📄 {fname} — extracted text"):
                        st.text(
                            text[:2000] + ("..." if len(text) > 2000 else "")
                        )

            # FIX 2 — Disclaimer at bottom of analysis tab
            st.divider()
            st.info("""
🤖 **AI Analysis Disclaimer**

All scores, feedback, and recommendations above are generated by Artificial Intelligence
(Llama 3.3 70B via Groq API). This analysis is designed to assist human reviewers,
not replace them. Final decisions on email content should always be made by a
qualified human professional familiar with your organisation's policies.
            """)

        # ══════════════════════════════════════════════════════
        # TAB 2 — Improved Email
        # ══════════════════════════════════════════════════════
        with tab2:
            st.markdown("## ✍️ Your Improved Email")
            st.markdown("*Rewritten by AI based on all agent feedback*")

            # FIX 2 — Disclaimer at top of improved email tab
            st.warning("""
✍️ **AI Rewrite Disclaimer**

The improved email below has been rewritten by Artificial Intelligence.
Please review all changes carefully before use. Ensure the rewritten content
accurately reflects your intended message and complies with your organisation's
communication policies. Do not send AI-generated content without human review.
            """)

            st.divider()

            raw_rewrite = rewrite_result["raw"]
            lines = raw_rewrite.splitlines()
            improved_subject = ""
            improved_email = ""
            changes = []
            section = ""

            for line in lines:
                if line.strip().upper().startswith("IMPROVED SUBJECT:"):
                    improved_subject = line.split(":", 1)[1].strip()
                elif line.strip().upper() == "IMPROVED EMAIL:":
                    section = "email"
                elif line.strip().upper() == "KEY CHANGES MADE:":
                    section = "changes"
                elif section == "email":
                    improved_email += line + "\n"
                elif section == "changes" and line.strip().startswith("-"):
                    changes.append(line.strip()[1:].strip())

            # Improved subject
            if improved_subject:
                st.markdown("#### 📌 Improved Subject Line")
                st.info(f"**{improved_subject}**")

            # Improved email body
            st.markdown("#### 📝 Improved Email Body")
            st.text_area(
                "Copy this improved email:",
                value=improved_email.strip() if improved_email.strip() else raw_rewrite,
                height=320,
                key="improved_email_box"
            )

            # Key changes list
            if changes:
                st.markdown("#### 🔧 Key Changes Made")
                for change in changes:
                    st.markdown(f"- ✅ {change}")

            # Before vs After comparison
            st.divider()
            st.markdown("#### 🔄 Before vs After Comparison")
            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown("**❌ Original**")
                st.text_area(
                    "Original",
                    value=f"Subject: {subject}\n\n{email_body}",
                    height=300,
                    key="original_compare",
                    disabled=True
                )
            with bc2:
                st.markdown("**✅ Improved**")
                st.text_area(
                    "Improved",
                    value=f"Subject: {improved_subject}\n\n{improved_email.strip()}",
                    height=300,
                    key="improved_compare",
                    disabled=True
                )

        # ══════════════════════════════════════════════════════
        # TAB 3 — Grammar & Duplicates
        # ══════════════════════════════════════════════════════
        with tab3:
            st.markdown("## 📝 Grammar & Style Corrections")
            st.markdown(
                "*Sentence-level corrections with explanations "
                "— as per output sample format*"
            )
            st.divider()

            if corrections:
                import pandas as pd
                df = pd.DataFrame(corrections)
                df.columns = ["ORIGINAL", "CORRECTION", "EXPLANATION"]
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ORIGINAL": st.column_config.TextColumn(
                            "ORIGINAL", width="medium"
                        ),
                        "CORRECTION": st.column_config.TextColumn(
                            "CORRECTION", width="medium"
                        ),
                        "EXPLANATION": st.column_config.TextColumn(
                            "EXPLANATION", width="large"
                        ),
                    }
                )
                st.success(f"✅ Found {len(corrections)} correction(s)")
            else:
                st.success("✅ No grammar issues found — great writing!")

            # FIX 2 — Grammar disclaimer
            st.caption("""
📝 AI Disclaimer: Grammar corrections are AI-generated suggestions based on standard
English writing conventions. They may not account for all industry-specific terminology
or regional language preferences. Please review each correction before applying.
            """)

            # Duplicate content detection
            st.divider()
            st.markdown("## 🔁 Duplicate & Repetitive Content Detection")
            with st.expander("View Duplicate Content Report", expanded=True):
                st.text(duplicate_result["raw"])

            # Alt text suggestions
            st.divider()
            st.markdown("## 🖼️ Image Alt Text Suggestions")
            with st.expander("View Alt Text Recommendations", expanded=False):
                st.text(alt_result["raw"])

            # User feedback
            st.divider()
            st.markdown("## 💬 Was this analysis helpful?")
            st.markdown("*Your feedback helps improve the AI agents*")
            fc1, fc2 = st.columns(2)
            with fc1:
                if st.button("👍 Yes, very helpful!", use_container_width=True):
                    st.success("Thank you for your positive feedback! 🎉")
            with fc2:
                if st.button("👎 Needs improvement", use_container_width=True):
                    st.text_area(
                        "Please tell us what to improve:",
                        key="feedback_text"
                    )
                    st.info("Thank you — your feedback has been noted!")

        # ══════════════════════════════════════════════════════
        # TAB 4 — Links & Elements
        # ══════════════════════════════════════════════════════
        with tab4:
            st.markdown("## 🔗 Hyperlink Verification")
            st.divider()

            if links_data:
                working = [l for l in links_data if l["working"]]
                broken = [l for l in links_data if not l["working"]]

                lc1, lc2 = st.columns(2)
                with lc1:
                    st.metric("✅ Working Links", len(working))
                with lc2:
                    st.metric("❌ Broken Links", len(broken))

                st.markdown("#### Link Details")
                for link in links_data:
                    if link["working"]:
                        st.success(
                            f"✅ **Working** | {link['url']} "
                            f"| HTTP {link['status_code']}"
                        )
                    else:
                        st.error(
                            f"❌ **Broken** | {link['url']} "
                            f"| HTTP {link['status_code']}"
                        )
            else:
                st.info("No hyperlinks found in this email or attachments.")

            # Emoji section
            st.divider()
            st.markdown("## 😊 Emoji Detection")
            if emojis_found:
                st.warning(
                    f"Found {len(emojis_found)} emoji(s): "
                    f"{' '.join(emojis_found)}"
                )
                st.info(
                    "⚠️ Emojis may not render correctly in all email "
                    "clients. Use sparingly in corporate communications."
                )
            else:
                st.success(
                    "✅ No emojis found — appropriate for corporate email."
                )

            # Element summary
            st.divider()
            st.markdown("## 📊 Element Summary")
            el1, el2, el3, el4 = st.columns(4)
            with el1:
                st.metric("📝 Total Words", word_count)
            with el2:
                st.metric("🔗 Links Found", len(links_found))
            with el3:
                st.metric("😊 Emojis", len(emojis_found))
            with el4:
                st.metric("📎 Files Uploaded", len(uploaded_files) if uploaded_files else 0)

            # Subject length check
            st.divider()
            st.markdown("## 📌 Subject Line Analysis")
            subj_len = len(subject)
            st.markdown(f"**Current length:** {subj_len} characters")
            st.progress(min(subj_len / 60, 1.0))
            if subj_len <= 60:
                st.success(f"✅ Good length ({subj_len}/60 characters recommended)")
            else:
                st.warning(
                    f"⚠️ Too long ({subj_len} characters) — "
                    f"trim by {subj_len - 60} characters"
                )

        # ══════════════════════════════════════════════════════
        # TAB 5 — Final Summary
        # ══════════════════════════════════════════════════════
        with tab5:
            st.markdown("## 🏆 Final Summary")
            st.markdown("*Chief Communication Officer Agent verdict*")
            st.divider()
            st.text(results[4]["raw"])

            # FIX 2 — Disclaimer in summary tab
            st.divider()
            st.caption("""
🤖 AI Disclaimer: This summary was generated by Artificial Intelligence and represents
an automated assessment only. It should be used as a guide to assist human decision-making,
not as a definitive or authoritative evaluation of the email content.
            """)

        # ══════════════════════════════════════════════════════
        # TAB 6 — Export
        # ══════════════════════════════════════════════════════
        with tab6:
            st.markdown("## ⬇️ Export Your Report")
            st.markdown("Download the full analysis in your preferred format")

            # FIX 2 — Disclaimer in export tab
            st.info("""
📄 **Export Disclaimer**

All exported reports contain AI-generated analysis (Llama 3.3 70B via Groq API).
Reports are intended for internal review purposes only. Content should be verified
by a human professional before any action is taken. Do not share exported reports
externally without human review and approval.
            """)

            st.divider()

            exp1, exp2, exp3 = st.columns(3)

            # PDF Export
            with exp1:
                st.markdown("### 📄 PDF Report")
                if st.button("Generate PDF", use_container_width=True):
                    with st.spinner("Generating PDF report..."):
                        try:
                            pdf_file = export_as_pdf(
                                subject, recipient, results,
                                overall, corrections, links_data
                            )
                            with open(pdf_file, "rb") as f:
                                st.download_button(
                                    "⬇️ Download PDF",
                                    data=f,
                                    file_name=os.path.basename(pdf_file),
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            st.success(f"Saved: {pdf_file}")
                        except Exception as e:
                            st.error(f"PDF error: {str(e)}")

            # Word Export
            with exp2:
                st.markdown("### 📝 Word Document")
                if st.button("Generate Word Doc", use_container_width=True):
                    with st.spinner("Generating Word document..."):
                        try:
                            docx_file = export_as_docx(
                                subject, recipient, results,
                                overall, corrections, links_data
                            )
                            with open(docx_file, "rb") as f:
                                st.download_button(
                                    "⬇️ Download Word Doc",
                                    data=f,
                                    file_name=os.path.basename(docx_file),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    use_container_width=True
                                )
                            st.success(f"Saved: {docx_file}")
                        except Exception as e:
                            st.error(f"Word doc error: {str(e)}")

            # TXT Export
            with exp3:
                st.markdown("### 📋 Text Report")
                try:
                    txt_file = save_report(
                        subject, recipient, results, overall
                    )
                    with open(txt_file, "r", encoding="utf-8") as f:
                        st.download_button(
                            "⬇️ Download TXT Report",
                            data=f,
                            file_name=os.path.basename(txt_file),
                            mime="text/plain",
                            use_container_width=True
                        )
                    st.success(f"Saved: {txt_file}")
                except Exception as e:
                    st.error(f"TXT error: {str(e)}")