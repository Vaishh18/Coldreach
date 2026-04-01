import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="ColdReach", layout="wide")

st.title("📧 ColdReach Dashboard")
st.caption("Automated Email + Reply Tracking System")

st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
send_btn = st.sidebar.button("🚀 Send Emails")
check_btn = st.sidebar.button("📬 Check Replies")


def load_data():
    conn = sqlite3.connect("emails.db")
    df = pd.read_sql("SELECT * FROM emails", conn)
    conn.close()
    return df


try:
    df_db = load_data()
except:
    df_db = pd.DataFrame()

col1, col2, col3 = st.columns(3)

total = len(df_db)
replied = len(df_db[df_db["replied"] == 1]) if not df_db.empty else 0
pending = total - replied

col1.metric("📨 Total Emails", total)
col2.metric("✅ Replies", replied)
col3.metric("⏳ Pending", pending)

st.divider()

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 CSV Preview")
    st.dataframe(df, width="stretch")

    if send_btn:
        from send import send_from_uploaded_csv
        send_from_uploaded_csv(uploaded_file)
        st.success("All emails sent 🚀")

if check_btn:
    from check_replies import check_for_replies
    check_for_replies()
    st.success("Checked for replies 📬")

st.divider()

st.subheader("📋 Email Tracking Table")

if not df_db.empty:
    st.dataframe(df_db, width="stretch")
else:
    st.info("No emails yet")