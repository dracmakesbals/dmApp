import streamlit as st
import pandas as pd
import random
import os

FOLLOWERS_FILE = "usernamesMS.csv"
ASSIGNED_FILE = "assigned_followers.csv"

# Load followers from CSV
def load_followers():
    if os.path.exists(FOLLOWERS_FILE):
        df = pd.read_csv(FOLLOWERS_FILE)
        return df["Username"].tolist()
    return []

# Save updated followers back to CSV (removes assigned followers)
def save_followers(followers):
    df = pd.DataFrame(followers, columns=["Username"])
    df.to_csv(FOLLOWERS_FILE, index=False)

# Load assigned followers from CSV
def load_assigned_followers():
    if os.path.exists(ASSIGNED_FILE):
        df = pd.read_csv(ASSIGNED_FILE)
        return df["Assigned"].tolist()
    return []

# Save assigned follower to CSV
def save_assigned_follower(username):
    df = pd.DataFrame([username], columns=["Assigned"])
    df.to_csv(ASSIGNED_FILE, mode="a", header=not os.path.exists(ASSIGNED_FILE), index=False)

# Initialize session state
if "assigned_follower" not in st.session_state:
    st.session_state.assigned_follower = None

# Load available followers
followers = load_followers()
assigned_followers = load_assigned_followers()

# Remove already assigned followers from the available list
followers = [f for f in followers if f not in assigned_followers]

st.title("Random Username DM Task")

if st.session_state.assigned_follower:
    st.success(f"Your assigned follower: **{st.session_state.assigned_follower}**")
else:
    if followers:
        if st.button("Get a Random Username to DM"):
            chosen_follower = random.choice(followers)
            followers.remove(chosen_follower)
            save_followers(followers)  # Update available followers
            save_assigned_follower(chosen_follower)  # Save assigned follower
            
            # Store in session state
            st.session_state.assigned_follower = chosen_follower

            st.success(f"Your assigned follower: **{chosen_follower}**")
    else:
        st.error("No more followers left!")
