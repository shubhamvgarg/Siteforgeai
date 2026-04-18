import streamlit as st
import sys
import os
import threading
import queue
import time
from io import StringIO

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Project Builder",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0a0a0f 60%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent; }

/* Hide default streamlit elements */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7c5cbf;
    border: 1px solid #7c5cbf44;
    padding: 0.3rem 0.8rem;
    border-radius: 2px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 6vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 30%, #9b6dff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.75rem;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: #6a6a88;
    letter-spacing: 0.05em;
}

/* ── Input card ── */
.input-card {
    background: #12121e;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    padding: 1.8rem;
    max-width: 760px;
    margin: 0 auto 2rem;
    position: relative;
    overflow: hidden;
}
.input-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #7c5cbf, #a78bfa, transparent);
}
.input-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c5cbf;
    margin-bottom: 0.6rem;
    display: block;
}

/* Style Streamlit textarea */
[data-testid="stTextArea"] textarea {
    background: #0d0d18 !important;
    border: 1px solid #2a2a40 !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
    line-height: 1.6 !important;
    resize: vertical !important;
    min-height: 110px !important;
    padding: 0.85rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #7c5cbf !important;
    box-shadow: 0 0 0 3px #7c5cbf22 !important;
    outline: none !important;
}
[data-testid="stTextArea"] label { display: none !important; }

/* Style Streamlit button */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #7c5cbf, #a78bfa) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    width: 100% !important;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }
[data-testid="stButton"] > button:disabled {
    opacity: 0.4 !important;
    cursor: not-allowed !important;
}

/* ── Log / output panel ── */
.log-header {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c5cbf;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    max-width: 760px;
    margin: 0 auto 0.4rem;
}
.log-dot {
    width: 7px; height: 7px;
    background: #a78bfa;
    border-radius: 50%;
    animation: blink 1.1s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

.log-box {
    background: #0d0d18;
    border: 1px solid #2a2a40;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    max-width: 760px;
    margin: 0 auto 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    color: #9090b0;
    max-height: 380px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.log-box::-webkit-scrollbar { width: 5px; }
.log-box::-webkit-scrollbar-track { background: transparent; }
.log-box::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 3px; }

/* ── Status badges ── */
.status-row {
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}
.badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    letter-spacing: 0.08em;
}
.badge-idle   { background:#1e1e30; color:#5a5a78; border:1px solid #2a2a40; }
.badge-run    { background:#1a0d30; color:#a78bfa; border:1px solid #7c5cbf66; }
.badge-done   { background:#0d201a; color:#4ade80; border:1px solid #22c55e55; }
.badge-error  { background:#200d0d; color:#f87171; border:1px solid #ef444455; }

/* ── Result card ── */
.result-card {
    background: #0d201a;
    border: 1px solid #22c55e33;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    max-width: 760px;
    margin: 0 auto 2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #4ade80, transparent);
}
.result-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4ade80;
    margin-bottom: 0.8rem;
}
.result-body {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #a0c0a8;
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.7;
    max-height: 320px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────

def add_agent_to_path():
    """Add the agent directory to sys.path so we can import from it."""
    agent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "agent")
    if agent_dir not in sys.path:
        sys.path.insert(0, agent_dir)


class StreamCapture:
    """Captures stdout/stderr into a queue for live display."""
    def __init__(self, q: queue.Queue, original):
        self.q = q
        self.original = original

    def write(self, text):
        self.q.put(text)
        self.original.write(text)

    def flush(self):
        self.original.flush()


def run_agent(prompt: str, log_queue: queue.Queue, result_queue: queue.Queue):
    """Runs the agent in a background thread, captures output."""
    add_agent_to_path()

    orig_stdout, orig_stderr = sys.stdout, sys.stderr
    sys.stdout = StreamCapture(log_queue, orig_stdout)
    sys.stderr = StreamCapture(log_queue, orig_stderr)

    try:
        from agent.graph import agent  # imported here inside thread after path fix
        result = agent.invoke(
            {"user_prompt": prompt},
            {
                "recursion_limit": 100,
                "configurable": {"thread_id": f"session-{int(time.time())}"},
            },
        )
        result_queue.put(("ok", result))
    except Exception as exc:
        result_queue.put(("err", str(exc)))
    finally:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr
        log_queue.put(None)  # sentinel


# ── Session state ─────────────────────────────────────────────────────────────
for key, default in [
    ("running", False),
    ("log_lines", []),
    ("final_result", None),
    ("error", None),
    ("log_queue", None),
    ("result_queue", None),
    ("thread", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── UI ────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-tag">LangGraph · LangChain · Groq</div>
    <div class="hero-title">AI Project Builder</div>
    <div class="hero-sub">describe an idea → plan → architect → code → ship</div>
</div>
""", unsafe_allow_html=True)

# Status badge
if st.session_state.error:
    badge = '<div class="badge badge-error">● ERROR</div>'
elif st.session_state.final_result:
    badge = '<div class="badge badge-done">● COMPLETE</div>'
elif st.session_state.running:
    badge = '<div class="badge badge-run">● RUNNING</div>'
else:
    badge = '<div class="badge badge-idle">○ IDLE</div>'

st.markdown(f'<div class="status-row">{badge}</div>', unsafe_allow_html=True)

# Input card
# st.markdown('<div class="input-card"><span class="input-label">Your idea</span>', unsafe_allow_html=True)
user_prompt = st.text_area(
    label="idea",
    placeholder="e.g. Simple to-do app",
    height=120,
    disabled=st.session_state.running,
)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    build_clicked = st.button(
        "⚡  Build Project",
        disabled=st.session_state.running or not user_prompt.strip(),
        use_container_width=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ── Start agent ───────────────────────────────────────────────────────────────
if build_clicked and user_prompt.strip():
    st.session_state.running = True
    st.session_state.log_lines = []
    st.session_state.final_result = None
    st.session_state.error = None

    lq: queue.Queue = queue.Queue()
    rq: queue.Queue = queue.Queue()
    st.session_state.log_queue = lq
    st.session_state.result_queue = rq

    t = threading.Thread(target=run_agent, args=(user_prompt.strip(), lq, rq), daemon=True)
    t.start()
    st.session_state.thread = t

# ── Poll queues while running ─────────────────────────────────────────────────
if st.session_state.running:
    lq = st.session_state.log_queue
    rq = st.session_state.result_queue

    # Drain log queue
    while True:
        try:
            msg = lq.get_nowait()
        except queue.Empty:
            break
        if msg is None:
            # Check result
            try:
                status, payload = rq.get_nowait()
                if status == "ok":
                    st.session_state.final_result = payload
                else:
                    st.session_state.error = payload
            except queue.Empty:
                pass
            st.session_state.running = False
            break
        if msg.strip():
            st.session_state.log_lines.append(msg)

    # Auto-refresh while still running
    if st.session_state.running:
        time.sleep(0.5)
        st.rerun()

# ── Log display ───────────────────────────────────────────────────────────────
if st.session_state.log_lines or st.session_state.running:
    dot_html = '<span class="log-dot"></span>' if st.session_state.running else ""
    st.markdown(
        f'<div class="log-header">{dot_html} Agent Output</div>',
        unsafe_allow_html=True,
    )
    log_text = "".join(st.session_state.log_lines[-500:])  # last 500 chunks
    st.markdown(
        f'<div class="log-box">{log_text or "Starting…"}</div>',
        unsafe_allow_html=True,
    )

# ── Final result ──────────────────────────────────────────────────────────────
if st.session_state.final_result:
    import json
    try:
        body = json.dumps(st.session_state.final_result, indent=2, default=str)
    except Exception:
        body = str(st.session_state.final_result)

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">✓ Build Complete — Final State</div>
        <div class="result-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.error:
    st.markdown(f"""
    <div style="background:#200d0d;border:1px solid #ef444433;border-radius:12px;
                padding:1.2rem 1.6rem;max-width:760px;margin:0 auto 2rem;
                font-family:'Space Mono',monospace;font-size:0.78rem;color:#f87171;
                line-height:1.7;">
        <strong>ERROR</strong><br><br>{st.session_state.error}
    </div>
    """, unsafe_allow_html=True)

# ── Reset button ──────────────────────────────────────────────────────────────
if not st.session_state.running and (st.session_state.final_result or st.session_state.error):
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("↺  Start New Build", use_container_width=True):
            for key in ("running", "log_lines", "final_result", "error", "log_queue", "result_queue", "thread"):
                st.session_state[key] = None if "queue" in key or key == "thread" else ([] if key == "log_lines" else False if key == "running" else None)
            st.rerun()