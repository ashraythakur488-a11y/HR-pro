import streamlit as st
import sqlite3
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS complaints
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  room TEXT,
                  issue TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

def add_complaint(name, room, issue):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO complaints (name, room, issue, timestamp) VALUES (?, ?, ?, ?)",
              (name, room, issue, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_complaints():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM complaints ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# Initialize database
init_db()

# Streamlit UI
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Submit Complaint", "Admin Dashboard"])

if page == "Submit Complaint":
    st.title("PG Complaint System")
    st.write("Please fill out the form below to report an issue.")

    with st.form("complaint_form"):
        name = st.text_input("Your Name")
        room = st.text_input("Room Number")
        issue = st.text_area("Describe the issue")
        submit = st.form_submit_button("Submit Complaint")

        if submit:
            if name and room and issue:
                add_complaint(name, room, issue)
                st.success("Your complaint has been submitted successfully!")
            else:
                st.error("Please fill in all fields.")

elif page == "Admin Dashboard":
    st.title("Admin Dashboard")
    password = st.text_input("Enter admin password", type="password")

    if password == "admin123":
        st.success("Access granted!")
        complaints = get_complaints()

        if complaints:
            for comp in complaints:
                st.write(f"**ID:** {comp[0]} | **Name:** {comp[1]} | **Room:** {comp[2]} | **Issue:** {comp[3]} | **Time:** {comp[4]}")
        else:
            st.info("No complaints submitted yet.")
    else:
        if password:
            st.error("Incorrect password")
