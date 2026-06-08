import streamlit as st
from agents import (
    tone_agent, compliance_agent, clarity_agent,
    subject_agent, summary_agent, rewriter_agent
)
from grammar_agent import grammar_agent, alt_text_agent
from extractor import (
    extract_from_pdf, extract_from_docx, extract_from_excel,
    extract_from_image, detect_emojis, extract_links,
    count_words, verify_links
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
st.markdown("**Tata Steel — Corporate Communications** | 6-Agent AI Analysis")
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

    # File uploads
    st.markdown("#### 📎 Attachments (optional)")
    uploaded_files = st.file_uploader(
        "Upload PDF, Word, Excel, or Image files",
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
    - 🖼️ Alt Text Suggester
    """)

st.divider()
analyze = st.button("🚀 Analyze & Improve Email", type="primary", use_container_width=True)

# ══════════════════════════════════════════════════════════════
# ANALYSIS
# ══════════════════════════════════════════════════════════════
if analyze:
    if not subject or len(subject.strip()) < 3:
        st.error("⚠️ Please enter a proper subject line.")
    elif len(email_body.strip().split()) < 5:
        st.error("⚠️ Email body is too short.")
    else:
        # ── Extract text from uploaded files ──────────────────
        extracted_texts = {}
        image_count = 0
        full_text = email_body

        if uploaded_files:
            st.markdown("#### 📂 Processing uploaded files...")
            for f in uploaded_files:
                fname = f.name.lower()
                if fname.endswith(".pdf"):
                    t = extract_from_pdf(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                elif fname.endswith(".docx"):
                    t = extract_from_docx(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                elif fname.endswith(".xlsx"):
                    t = extract_from_excel(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                elif fname.endswith((".png", ".jpg", ".jpeg", ".gif")):
                    t = extract_from_image(f)
                    extracted_texts[f.name] = t
                    full_text += "\n\n" + t
                    image_count += 1

        # ── Element detection ──────────────────────────────────
        emojis_found = detect_emojis(full_text)
        links_found = extract_links(full_text)
        word_count = count_words(full_text)

        # ── Verify links ───────────────────────────────────────
        links_data = []
        if links_found:
            with st.spinner("🔗 Verifying hyperlinks..."):
                links_data = verify_links(links_found)

        # ── Run all agents with progress bar ──────────────────
        st.markdown("### ⚙️ Running Analysis...")
        progress = st.progress(0, text="Starting agents...")

        results = []

        progress.progress(8, text="🎭 Tone Analyzer...")
        results.append(tone_agent(email_body, recipient))

        progress.progress(22, text="🛡️ Compliance Checker...")
        results.append(compliance_agent(email_body, recipient))

        progress.progress(36, text="✏️ Clarity Optimizer...")
        results.append(clarity_agent(email_body))

        progress.progress(50, text="📧 Subject Line Reviewer...")
        results.append(subject_agent(subject, email_body, recipient))

        progress.progress(63, text="🏆 Summary Agent...")
        results.append(summary_agent(results, subject, recipient))

        progress.progress(75, text="✍️ Rewriting your email...")
        rewrite_result = rewriter_agent(email_body, subject, recipient, results)
        results.append(rewrite_result)

        progress.progress(87, text="📝 Checking grammar...")
        grammar_result = grammar_agent(full_text)
        corrections = grammar_result.get("corrections", [])

        progress.progress(95, text="🖼️ Alt text suggestions...")
        alt_result = alt_text_agent(image_count > 0, image_count)

        progress.progress(100, text="✅ All done!")

        # ── Scores ────────────────────────────────────────────
        scores = [extract_score(r["raw"]) for r in results[:4]]
        overall = sum(scores) // len(scores) if scores else 0

        st.divider()

        # ══════════════════════════════════════════════════════
        # TABS
        # ══════════════════════════════════════════════════════
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Analysis",
            "✍️ Improved Email",
            "📝 Grammar Corrections",
            "🔗 Links & Elements",
            "🏆 Summary",
            "⬇️ Export"
        ])

        # ── TAB 1: Analysis ────────────────────────────────────
        with tab1:
            s1, s2, s3, s4, s5 = st.columns(5)
            labels = ["🎭 Tone", "🛡️ Compliance", "✏️ Clarity", "📧 Subject", "📊 Overall"]
            cols = [s1, s2, s3, s4, s5]
            for i, col in enumerate(cols[:4]):
                sc = extract_score(results[i]["raw"])
                with col:
                    st.metric(labels[i], f"{sc}/100")
            with s5:
                st.metric("📊 Overall", f"{overall}/100")

            st.progress(overall / 100)
            if overall >= 80:
                st.success("✅ Ready to send!")
            elif overall >= 60:
                st.warning("⚠️ Fix a few things first.")
            elif overall >= 40:
                st.error("❌ Needs significant improvement.")
            else:
                st.error("🚫 Do NOT send.")

            # Word count and element info
            st.divider()
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                st.metric("📝 Total Word Count", word_count)
            with ec2:
                st.metric("😊 Emojis Found", len(emojis_found))
            with ec3:
                st.metric("🔗 Links Found", len(links_found))

            if emojis_found:
                st.info(f"Emojis detected: {' '.join(emojis_found)}")

            st.divider()
            for i in range(4):
                sc = extract_score(results[i]["raw"])
                icon = "🟢" if sc >= 80 else "🟡" if sc >= 60 else "🔴"
                with st.expander(f"{icon} {results[i]['agent']} — {sc}/100"):
                    st.text(results[i]["raw"])

            # Show extracted file content
            if extracted_texts:
                st.divider()
                st.markdown("#### 📎 Text extracted from attachments")
                for fname, text in extracted_texts.items():
                    with st.expander(f"📄 {fname}"):
                        st.text(text[:2000] + ("..." if len(text) > 2000 else ""))

        # ── TAB 2: Improved Email ──────────────────────────────
        with tab2:
            st.markdown("## ✍️ Your Improved Email")
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

            if improved_subject:
                st.markdown("#### 📌 Improved Subject Line")
                st.info(f"**{improved_subject}**")

            st.markdown("#### 📝 Improved Email Body")
            st.text_area("Copy this:", value=improved_email.strip() or raw_rewrite, height=300)

            if changes:
                st.markdown("#### 🔧 Key Changes Made")
                for c in changes:
                    st.markdown(f"- ✅ {c}")

            st.divider()
            st.markdown("#### 🔄 Before vs After")
            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown("**❌ Original**")
                st.text_area("", value=f"Subject: {subject}\n\n{email_body}",
                             height=280, disabled=True, key="orig")
            with bc2:
                st.markdown("**✅ Improved**")
                st.text_area("", value=f"Subject: {improved_subject}\n\n{improved_email.strip()}",
                             height=280, disabled=True, key="impr")

        # ── TAB 3: Grammar Corrections ─────────────────────────
        with tab3:
            st.markdown("## 📝 Grammar & Style Corrections")
            st.markdown("*Sentence-level corrections with explanations*")
            st.divider()

            if corrections:
                # Build the corrections table exactly like the screenshot
                import pandas as pd
                df = pd.DataFrame(corrections)
                df.columns = ["ORIGINAL", "CORRECTION", "EXPLANATION"]
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "ORIGINAL": st.column_config.TextColumn("ORIGINAL", width="medium"),
                        "CORRECTION": st.column_config.TextColumn("CORRECTION", width="medium"),
                        "EXPLANATION": st.column_config.TextColumn("EXPLANATION", width="large"),
                    }
                )
                st.success(f"Found {len(corrections)} correction(s)")
            else:
                st.success("✅ No grammar issues found!")

            # Alt text suggestions
            st.divider()
            st.markdown("## 🖼️ Image Alt Text Suggestions")
            st.text(alt_result["raw"])

            # User feedback
            st.divider()
            st.markdown("## 💬 Was this analysis helpful?")
            fc1, fc2 = st.columns(2)
            with fc1:
                if st.button("👍 Yes, helpful!", use_container_width=True):
                    st.success("Thank you for your feedback!")
            with fc2:
                if st.button("👎 Needs improvement", use_container_width=True):
                    feedback_text = st.text_area("Tell us what to improve:")
                    st.info("Feedback noted — thank you!")

        # ── TAB 4: Links & Elements ────────────────────────────
        with tab4:
            st.markdown("## 🔗 Hyperlink Verification")
            st.divider()

            if links_data:
                for link in links_data:
                    if link["working"]:
                        st.success(f"✅ **Working** | {link['url']} | HTTP {link['status_code']}")
                    else:
                        st.error(f"❌ **Broken** | {link['url']} | HTTP {link['status_code']}")
            else:
                st.info("No hyperlinks found in this email.")

            st.divider()
            st.markdown("## 😊 Emoji Detection")
            if emojis_found:
                st.warning(f"Found {len(emojis_found)} emoji(s): {' '.join(emojis_found)}")
                st.info("⚠️ Emojis may not render correctly in all email clients. Use sparingly in corporate communications.")
            else:
                st.success("✅ No emojis found — appropriate for corporate email.")

            st.divider()
            st.markdown("## 📊 Email Statistics")
            stat1, stat2, stat3 = st.columns(3)
            with stat1:
                st.metric("Total Words", word_count)
            with stat2:
                st.metric("Links Found", len(links_found))
            with stat3:
                st.metric("Subject Length", f"{len(subject)} chars")

            if len(subject) > 60:
                st.warning("⚠️ Subject line is over 60 characters — consider shortening it.")
            else:
                st.success(f"✅ Subject line length is good ({len(subject)}/60 characters).")

        # ── TAB 5: Summary ─────────────────────────────────────
        with tab5:
            st.markdown("## 🏆 Final Summary")
            st.markdown("*Chief Communication Officer Agent*")
            st.divider()
            st.text(results[4]["raw"])

        # ── TAB 6: Export ──────────────────────────────────────
        with tab6:
            st.markdown("## ⬇️ Export Your Report")
            st.divider()

            exp1, exp2 = st.columns(2)

            with exp1:
                st.markdown("### 📄 Export as PDF")
                if st.button("Generate PDF Report", use_container_width=True):
                    with st.spinner("Generating PDF..."):
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
                    st.success(f"Saved to: {pdf_file}")

            with exp2:
                st.markdown("### 📝 Export as Word Document")
                if st.button("Generate Word Report", use_container_width=True):
                    with st.spinner("Generating Word doc..."):
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
                    st.success(f"Saved to: {docx_file}")

            st.divider()
            st.markdown("### 📋 Export as TXT")
            txt_file = save_report(subject, recipient, results, overall)
            with open(txt_file, "r", encoding="utf-8") as f:
                st.download_button(
                    "⬇️ Download TXT Report",
                    data=f,
                    file_name=os.path.basename(txt_file),
                    mime="text/plain",
                    use_container_width=True
                )