import streamlit as st
import subprocess
import os
import vault
import numpy as np

vault.init_db()

st.set_page_config(page_title="PrivacyFirst AI", page_icon="🛡️", layout="wide")

if 'enroll_mode' not in st.session_state:
    st.session_state.enroll_mode = False

st.title("🛡️ PrivacyFirst Biometric Vault")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Secure Authentication")

    if st.button("Start Login", use_container_width=True):

        result = subprocess.run(
            ["python", "auth.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        full_output = (result.stdout + result.stderr).strip()

        if "Verified:" in full_output:
            user_name = full_output.split("Verified:")[-1].strip()
            st.success(f"Access Granted! Welcome back, {user_name}.")
            st.balloons()
        else:
            st.error("Access Denied: Face Unregistered or Challenge Failed.")

with col2:
    st.subheader("User Enrollment")

    if st.button("Capture Face Profile", use_container_width=True):
        subprocess.run(["python", "enroll.py"])
        if os.path.exists("temp_face.npy"):
            st.session_state.enroll_mode = True
            st.success("Face Captured! Enter credentials below.")

    if st.session_state.enroll_mode:
        with st.form("registration_form"):
            new_user_name = st.text_input("Enter Username / ID")
            submit_reg = st.form_submit_button("Register to Vault")

            if submit_reg and new_user_name:
                encoding = np.load("temp_face.npy")
                vault.save_user(new_user_name, encoding)
                os.remove("temp_face.npy")
                st.session_state.enroll_mode = False
                st.success(f"{new_user_name} successfully registered.")
                st.rerun()

st.markdown("---")
st.caption("Zero-Image Storage Enabled")