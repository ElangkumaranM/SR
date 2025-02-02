import streamlit as st
import pandas as pd
import re
from datetime import datetime, time

def parse_chat(file, brand_name):
    chats = []
    content = file.getvalue().decode("utf-8")  # Read and decode the file content
    for line in content.split("\n"):  # Process each line
        match = re.match(r'(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}) - (.*?): (.*)', line)
        if match:
            timestamp, sender, message = match.groups()
            chats.append((timestamp, brand_name, sender, message))
    return pd.DataFrame(chats, columns=['Timestamp', 'Brand', 'Sender', 'Message'])

def filter_by_date(df, selected_date):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%y, %H:%M', errors='coerce')
    df['Date'] = df['Timestamp'].dt.date
    return df[df['Date'] == selected_date]

st.title("Chat Management System")

uploaded_files = st.file_uploader("Upload multiple chat text files", type=["txt"], accept_multiple_files=True)

if uploaded_files:
    dataframes = []
    for uploaded_file in uploaded_files:
        brand_name = uploaded_file.name.replace(".txt", "")  # Extract brand name from filename
        df = parse_chat(uploaded_file, brand_name)
        dataframes.append(df)
    
    all_chats = pd.concat(dataframes, ignore_index=True)
    
    brand_list = all_chats['Brand'].unique()
    selected_brand = st.selectbox("Select Brand", brand_list)  # Moved brand selection here
    brand_chats = all_chats[all_chats['Brand'] == selected_brand]
    
    selected_date = st.date_input("Select Date", datetime.today())
    
    # Filter chats by the selected date
    filtered_chats = filter_by_date(brand_chats, selected_date)

    # Define time slots for the day
    time_slots = {
        "Morning (8:30 - 10:00)": (time(8, 30), time(10, 0)),
        "Midday (12:00 - 1:30)": (time(12, 0), time(13, 30)),
        "Afternoon (3:00 - 4:30)": (time(15, 0), time(16, 30)),
        "Daily Task (5:30 - 7:00)": (time(17, 30), time(19, 0)),
    }

    # Prepare the table for displaying message status
    status_data = []
    for slot_name, (start, end) in time_slots.items():
        messages_in_slot = filtered_chats[
            filtered_chats['Timestamp'].dt.time.between(start, end)
        ]
        
        if not messages_in_slot.empty:
            # Only show the time slot and a tick if there are messages in that slot
            status_data.append({
                "Time Slot": slot_name,
                "Status": "✔️",  # Tick if messages were sent in this time slot
                "Notes": "Messages were sent during this time! 🎉📩"  # Add some emojis as notes
            })
        else:
            # Indicate no messages were sent in this slot
            status_data.append({
                "Time Slot": slot_name,
                "Status": "❌",  # Indicate no messages sent
                "Notes": "No messages sent during this time. 😞🚫"  # Add emojis for no messages
            })

    # Create a DataFrame for the status data
    status_df = pd.DataFrame(status_data)

    st.write(f"### Message Status for {selected_brand} on {selected_date}")
    st.dataframe(status_df)
