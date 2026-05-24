import streamlit as st
from agents import run_all_agents
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
st.markdown("**Tata Steel — Corporate Communications** | Multi-Agent AI Analysis")
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
    """)

st.divider()

# ── Analyze button ────────────────────────────────────────────
analyze = st.button("🚀 Analyze Email", type="primary", use_container_width=True)

if analyze:
    # Validation
    if not subject or len(subject.strip()) < 3:
        st.error("⚠️ Please enter a proper subject line.")
    elif len(email_body.strip().split()) < 15:
        st.error("⚠️ Email body is too short. Please enter at least 15 words.")
    else:
        # Run agents with a progress bar
        st.markdown("### ⚙️ Running Analysis...")
        progress = st.progress(0, text="Starting agents...")

        results = []
        agent_names = [
            "🎭 Tone Analyzer",
            "🛡️ Compliance Checker",
            "✏️ Clarity Optimizer",
            "📧 Subject Line Reviewer",
            "🏆 Summary Agent"
        ]

        # Import individual agents
        from agents import (
            tone_agent, compliance_agent,
            clarity_agent, subject_agent, summary_agent
        )

        # Run each agent and update progress bar
        progress.progress(10, text="Running Tone Analyzer...")
        results.append(tone_agent(email_body, recipient))

        progress.progress(30, text="Running Compliance Checker...")
        results.append(compliance_agent(email_body, recipient))

        progress.progress(50, text="Running Clarity Optimizer...")
        results.append(clarity_agent(email_body))

        progress.progress(70, text="Running Subject Line Reviewer...")
        results.append(subject_agent(subject, email_body, recipient))

        progress.progress(90, text="Running Summary Agent...")
        results.append(summary_agent(results, subject, recipient))

        progress.progress(100, text="✅ All agents done!")

        # ── Overall score ──────────────────────────────────────
        scores = [extract_score(r["raw"]) for r in results[:-1]]  # exclude summary
        overall = sum(scores) // len(scores) if scores else 0

        st.divider()
        st.markdown("## 📊 Results")

        # Score display
        score_col1, score_col2, score_col3 = st.columns(3)
        with score_col1:
            st.metric("Overall Score", f"{overall} / 100")
        with score_col2:
            if overall >= 80:
                st.success("✅ Ready to send!")
            elif overall >= 60:
                st.warning("⚠️ Minor edits needed")
            elif overall >= 40:
                st.error("❌ Significant issues")
            else:
                st.error("🚫 Do NOT send")
        with score_col3:
            st.metric("Agents Run", "5")

        st.progress(overall / 100)
        st.divider()

        # ── Individual agent results ───────────────────────────
        for i, result in enumerate(results):
            agent_name = result["agent"]
            raw = result["raw"]
            score = extract_score(raw)

            # Pick color based on score
            if i < 4:  # not the summary agent
                if score >= 80:
                    icon = "🟢"
                elif score >= 60:
                    icon = "🟡"
                else:
                    icon = "🔴"
                header = f"{icon} {agent_name} — {score}/100"
            else:
                header = f"🏆 {agent_name}"

            with st.expander(header, expanded=(i == 4)):
                st.text(raw)

        # ── Save report ────────────────────────────────────────
        filename = save_report(subject, recipient, results, overall)
        st.divider()
        st.success(f"💾 Report saved to: `{filename}`")

        # Download button
        with open(filename, "r", encoding="utf-8") as f:
            report_text = f.read()

        st.download_button(
            label="⬇️ Download Report as .txt",
            data=report_text,
            file_name=f"email_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )