import streamlit as st
from agents import (
    tone_agent, compliance_agent, clarity_agent,
    subject_agent, summary_agent, rewriter_agent
)
from main import extract_score, save_report
from datetime import datetime

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AI Email Checker — Tata Steel",
    page_icon="🏭",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────
st.markdown("# 🏭 AI Email Content Checker")
st.markdown("**Tata Steel — Corporate Communications** | 6-Agent AI Analysis")
st.divider()

# ── Input form ────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    subject = st.text_input(
        "📌 Email Subject Line",
        placeholder="e.g. Update on Q3 Plant Shutdown Schedule"
    )
    email_body = st.text_area(
        "📝 Email Body",
        placeholder="Paste or type your email here...",
        height=250
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

    st.markdown("### 🤖 Agents")
    st.markdown("""
    - 🎭 Tone Analyzer
    - 🛡️ Compliance Checker
    - ✏️ Clarity Optimizer
    - 📧 Subject Line Reviewer
    - 🏆 Summary Agent
    - ✍️ Email Rewriter
    """)

st.divider()

# ── Analyze button ────────────────────────────────────────────
analyze = st.button("🚀 Analyze & Improve Email", type="primary", use_container_width=True)

if analyze:
    # Validation
    if not subject or len(subject.strip()) < 3:
        st.error("⚠️ Please enter a proper subject line.")
    elif len(email_body.strip().split()) < 15:
        st.error("⚠️ Email body is too short. Please enter at least 15 words.")
    else:
        st.markdown("### ⚙️ Running 6-Agent Analysis...")
        progress = st.progress(0, text="Starting agents...")

        results = []

        progress.progress(5, text="🎭 Running Tone Analyzer...")
        results.append(tone_agent(email_body, recipient))

        progress.progress(25, text="🛡️ Running Compliance Checker...")
        results.append(compliance_agent(email_body, recipient))

        progress.progress(42, text="✏️ Running Clarity Optimizer...")
        results.append(clarity_agent(email_body))

        progress.progress(58, text="📧 Running Subject Line Reviewer...")
        results.append(subject_agent(subject, email_body, recipient))

        progress.progress(72, text="🏆 Running Summary Agent...")
        results.append(summary_agent(results, subject, recipient))

        progress.progress(88, text="✍️ Rewriting your email...")
        rewrite_result = rewriter_agent(email_body, subject, recipient, results)
        results.append(rewrite_result)

        progress.progress(100, text="✅ All 6 agents done!")

        # ── Overall score ──────────────────────────────────────
        scores = [extract_score(r["raw"]) for r in results[:4]]
        overall = sum(scores) // len(scores) if scores else 0

        st.divider()

        # ── TAB LAYOUT ─────────────────────────────────────────
        tab1, tab2, tab3 = st.tabs([
            "📊 Analysis Results",
            "✍️ Improved Email",
            "🏆 Final Summary"
        ])

        # ══════════════════════════════════════════════════════
        # TAB 1 — Analysis Results
        # ══════════════════════════════════════════════════════
        with tab1:
            # Score cards
            s1, s2, s3, s4 = st.columns(4)
            labels = ["🎭 Tone", "🛡️ Compliance", "✏️ Clarity", "📧 Subject"]
            cols = [s1, s2, s3, s4]

            for i, col in enumerate(cols):
                sc = extract_score(results[i]["raw"])
                with col:
                    st.metric(labels[i], f"{sc}/100")

            # Overall score bar
            st.markdown(f"### Overall Score: **{overall}/100**")
            st.progress(overall / 100)

            if overall >= 80:
                st.success("✅ Great — Ready to send!")
            elif overall >= 60:
                st.warning("⚠️ Okay — Fix a few things first.")
            elif overall >= 40:
                st.error("❌ Needs significant improvement.")
            else:
                st.error("🚫 Do NOT send — Major issues found.")

            st.divider()

            # Individual agent cards
            agent_icons = ["🎭", "🛡️", "✏️", "📧"]
            for i in range(4):
                sc = extract_score(results[i]["raw"])
                if sc >= 80:
                    icon = "🟢"
                elif sc >= 60:
                    icon = "🟡"
                else:
                    icon = "🔴"

                with st.expander(
                    f"{icon} {results[i]['agent']} — {sc}/100",
                    expanded=False
                ):
                    st.text(results[i]["raw"])

        # ══════════════════════════════════════════════════════
        # TAB 2 — Improved Email (THE NEW FEATURE!)
        # ══════════════════════════════════════════════════════
        with tab2:
            st.markdown("## ✍️ Your Improved Email")
            st.markdown("*Rewritten by AI based on all agent feedback*")
            st.divider()

            raw_rewrite = rewrite_result["raw"]

            # Extract improved subject
            improved_subject = ""
            improved_email = ""
            changes = []

            lines = raw_rewrite.splitlines()
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

            # Show improved subject
            if improved_subject:
                st.markdown("#### 📌 Improved Subject Line")
                st.info(f"**{improved_subject}**")

            # Show improved email in a nice box
            if improved_email.strip():
                st.markdown("#### 📝 Improved Email Body")
                st.text_area(
                    "Copy this improved email:",
                    value=improved_email.strip(),
                    height=350,
                    key="improved_email_box"
                )
            else:
                # Fallback — show full raw response
                st.text_area(
                    "Improved Email:",
                    value=raw_rewrite,
                    height=350,
                    key="improved_email_fallback"
                )

            # Show key changes
            if changes:
                st.markdown("#### 🔧 Key Changes Made")
                for change in changes:
                    st.markdown(f"- ✅ {change}")
            else:
                st.divider()
                st.text(raw_rewrite)

            # Side by side comparison
            st.divider()
            st.markdown("#### 🔄 Before vs After")
            bcol1, bcol2 = st.columns(2)
            with bcol1:
                st.markdown("**❌ Original**")
                st.text_area(
                    "Original email",
                    value=f"Subject: {subject}\n\n{email_body}",
                    height=300,
                    key="original_compare",
                    disabled=True
                )
            with bcol2:
                st.markdown("**✅ Improved**")
                st.text_area(
                    "Improved email",
                    value=f"Subject: {improved_subject}\n\n{improved_email.strip()}",
                    height=300,
                    key="improved_compare",
                    disabled=True
                )

        # ══════════════════════════════════════════════════════
        # TAB 3 — Final Summary
        # ══════════════════════════════════════════════════════
        with tab3:
            st.markdown("## 🏆 Final Summary")
            st.markdown("*From the Chief Communication Officer Agent*")
            st.divider()
            st.text(results[4]["raw"])

        # ── Save report & download ─────────────────────────────
        st.divider()
        filename = save_report(subject, recipient, results, overall)
        st.success(f"💾 Report saved to: `{filename}`")

        with open(filename, "r", encoding="utf-8") as f:
            report_text = f.read()

        st.download_button(
            label="⬇️ Download Full Report as .txt",
            data=report_text,
            file_name=f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )