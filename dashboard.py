import os
import subprocess
import sys

import numpy as np
import streamlit as st

import vault


vault.init_db()

st.set_page_config(page_title="LiveLock", page_icon="🔐", layout="wide")

if "enroll_mode" not in st.session_state:
    st.session_state.enroll_mode = False
if "last_user" not in st.session_state:
    st.session_state.last_user = None


def local_script(name):
    return subprocess.run(
        [sys.executable, name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def parse_verified_user(output):
    for line in output.splitlines():
        if "Verified:" in line:
            return line.split("Verified:", 1)[-1].strip()
    return None


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 18% 8%, rgba(47, 196, 154, 0.16), transparent 28rem),
            linear-gradient(135deg, #101512 0%, #151c18 48%, #171511 100%);
        color: #edf7f0;
    }
    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
    }
    h1, h2, h3 {
        letter-spacing: 0;
    }
    .hero {
        border: 1px solid rgba(143, 176, 155, 0.24);
        border-radius: 8px;
        padding: 1.4rem 1.5rem;
        background: rgba(17, 24, 20, 0.78);
        margin-bottom: 1rem;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
    }
    .hero-copy {
        color: #aebdb3;
        font-size: 1rem;
        max-width: 780px;
    }
    .status-pill {
        display: inline-block;
        border: 1px solid rgba(79, 209, 165, 0.42);
        border-radius: 999px;
        padding: 0.25rem 0.65rem;
        color: #91f0cf;
        background: rgba(79, 209, 165, 0.09);
        font-size: 0.82rem;
        margin-bottom: 0.8rem;
    }
    div[data-testid="stForm"], div[data-testid="stMetric"] {
        border: 1px solid rgba(143, 176, 155, 0.22);
        border-radius: 8px;
        padding: 1rem;
        background: rgba(17, 24, 20, 0.64);
    }
    .info-panel {
        border: 1px solid rgba(143, 176, 155, 0.18);
        border-radius: 8px;
        padding: 1rem;
        background: rgba(17, 24, 20, 0.48);
        color: #c6d4cb;
    }
    .small-muted {
        color: #9fb0a6;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <div class="status-pill">Zero-image biometric storage</div>
        <div class="hero-title">LiveLock Biometric Vault</div>
        <div class="hero-copy">
            Privacy-first face authentication using encrypted embeddings and a local liveness challenge.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

users = vault.get_all_users()
col_a, col_b, col_c = st.columns(3)
col_a.metric("Registered profiles", len(users))
col_b.metric("Storage mode", "Encrypted")
col_c.metric("Raw images saved", "0")

st.markdown("---")

login_col, enroll_col = st.columns(2, gap="large")

with login_col:
    st.subheader("Secure Authentication")
    st.markdown(
        '<div class="small-muted">Run the OpenCV liveness challenge, then match against encrypted face embeddings.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if st.button("Start Login", type="primary", use_container_width=True):
        with st.spinner("Opening authentication console..."):
            result = local_script("auth.py")

        full_output = (result.stdout + result.stderr).strip()
        user_name = parse_verified_user(full_output)

        if result.returncode == 0 and user_name:
            st.session_state.last_user = user_name
            st.success(f"Access granted. Welcome back, {user_name}.")
            st.balloons()
        else:
            st.error("Access denied: face unregistered or challenge failed.")
            if full_output:
                with st.expander("Show console output"):
                    st.code(full_output)

    if st.session_state.last_user:
        st.info(f"Last verified user: {st.session_state.last_user}")

with enroll_col:
    st.subheader("User Enrollment")
    st.markdown(
        '<div class="small-muted">Capture one face profile, then register it with a username.</div>',
        unsafe_allow_html=True,
    )
    st.write("")

    if st.button("Capture Face Profile", use_container_width=True):
        with st.spinner("Opening enrollment console..."):
            result = local_script("enroll.py")

        if result.returncode == 0 and os.path.exists("temp_face.npy"):
            st.session_state.enroll_mode = True
            st.success("Face captured. Enter credentials below.")
        else:
            st.error("Face capture was cancelled or no face was detected.")

    if st.session_state.enroll_mode:
        with st.form("registration_form"):
            new_user_name = st.text_input("Username / ID", max_chars=80)
            submit_reg = st.form_submit_button("Register to Vault", use_container_width=True)

        if submit_reg:
            if not new_user_name.strip():
                st.warning("Please enter a username.")
            elif not os.path.exists("temp_face.npy"):
                st.error("Capture a face profile first.")
            else:
                try:
                    encoding = np.load("temp_face.npy")
                    vault.save_user(new_user_name.strip(), encoding)
                    os.remove("temp_face.npy")
                    st.session_state.enroll_mode = False
                    st.success(f"{new_user_name.strip()} successfully registered.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Registration failed: {exc}")

st.markdown("---")

info_1, info_2, info_3 = st.columns(3)
with info_1:
    st.markdown(
        """
        <div class="info-panel">
            <strong>Encrypted embeddings</strong><br>
            <span class="small-muted">Only the numerical face vector is stored, not the original image.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with info_2:
    st.markdown(
        """
        <div class="info-panel">
            <strong>Liveness challenge</strong><br>
            <span class="small-muted">Head movement and blink checks help reduce basic spoofing attempts.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with info_3:
    st.markdown(
        """
        <div class="info-panel">
            <strong>Local vault</strong><br>
            <span class="small-muted">SQLite and Fernet keep the prototype simple and explainable.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("LiveLock prototype • No raw facial images stored")
