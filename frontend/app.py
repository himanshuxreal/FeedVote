import streamlit as st
import requests
import os
from typing import Optional

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="FeedVote",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .feedback-card {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .vote-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .top-idea-card {
        border-left: 4px solid #FFD700;
        padding: 15px;
        margin: 10px 0;
        background-color: #fffbf0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None


def create_user(username: str, email: str) -> Optional[dict]:
    """Create a new user"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/users/",
            json={"username": username, "email": email},
            timeout=5
        )
        if response.status_code == 201:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Failed to create user')}")
            return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None


def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/users/{username}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return None


def submit_feedback(title: str, description: str, user_id: int) -> bool:
    """Submit feedback"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/feedback/?user_id={user_id}",
            json={"title": title, "description": description},
            timeout=5
        )
        if response.status_code == 201:
            st.success("✅ Feedback submitted successfully!")
            return True
        else:
            st.error(f"Error: {response.json().get('detail', 'Failed to submit feedback')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False


def get_all_feedback() -> list:
    """Get all feedback"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/feedback/",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return []


def get_top_ideas(limit: int = 10) -> list:
    """Get top voted ideas"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/vote/top/?limit={limit}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return []


def submit_vote(feedback_id: int, user_id: int, vote_type: str) -> bool:
    """Submit a vote"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/vote/",
            json={
                "feedback_id": feedback_id,
                "user_id": user_id,
                "vote_type": vote_type
            },
            timeout=5
        )
        if response.status_code == 201:
            st.success(f"✅ {vote_type.capitalize()} submitted!")
            return True
        else:
            st.error(f"Error: {response.json().get('detail', 'Failed to vote')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False


# SIDEBAR - Login/Register
with st.sidebar:
    st.title("🔐 FeedVote")
    st.divider()
    
    if st.session_state.user_id is None:
        st.subheader("Authentication")
        auth_tab = st.radio("Choose action:", ["Login", "Register"])
        
        if auth_tab == "Register":
            with st.form("register_form"):
                reg_username = st.text_input("Username", max_chars=100)
                reg_email = st.text_input("Email", max_chars=100)
                reg_submit = st.form_submit_button("Register")
                
                if reg_submit:
                    if reg_username and reg_email:
                        user = create_user(reg_username, reg_email)
                        if user:
                            st.session_state.user_id = user.get("id")
                            st.session_state.username = user.get("username")
                            st.success("✅ Registration successful! Logged in.")
                            st.rerun()
                    else:
                        st.error("Please fill in all fields")
        
        else:  # Login
            with st.form("login_form"):
                login_username = st.text_input("Username")
                login_submit = st.form_submit_button("Login")
                
                if login_submit:
                    if login_username:
                        user = get_user_by_username(login_username)
                        if user:
                            st.session_state.user_id = user.get("id")
                            st.session_state.username = user.get("username")
                            st.success("✅ Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("❌ User not found. Please register first.")
                    else:
                        st.error("Please enter username")
    
    else:
        st.success(f"✅ Logged in as: **{st.session_state.username}**")
        if st.button("Logout", key="logout_btn"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    st.divider()
    
    # Navigation
    st.subheader("📍 Navigation")
    page = st.radio(
        "Select Page:",
        ["🏠 Home", "✍️ Submit Feedback", "📋 View Ideas", "🏆 Top Voted"],
        label_visibility="collapsed"
    )


# MAIN CONTENT - Pages

# Home Page
if page == "🏠 Home":
    st.title("📌 Welcome to FeedVote")
    st.markdown("""
    **FeedVote** is a collaborative feedback and voting platform where:
    - 💬 Users can submit ideas and feedback
    - 👍 Community members vote on ideas
    - 🏆 Popular ideas rise to the top
    
    ### How to use:
    1. **Login/Register** using the sidebar
    2. **Submit Feedback** with your ideas
    3. **Vote** on ideas posted by others
    4. **View Top Ideas** to see what's trending
    
    Start by logging in or registering in the sidebar!
    """)


# Submit Feedback Page
elif page == "✍️ Submit Feedback":
    if st.session_state.user_id is None:
        st.warning("⚠️ Please login or register first (see sidebar)")
    else:
        st.title("✍️ Submit Feedback")
        st.markdown("Share your ideas and suggestions with the community!")
        
        with st.form("feedback_form"):
            title = st.text_input(
                "💡 Idea Title",
                max_chars=255,
                placeholder="e.g., Add dark mode feature"
            )
            description = st.text_area(
                "📝 Description",
                placeholder="Describe your idea in detail...",
                height=200
            )
            submit_btn = st.form_submit_button("📤 Submit Feedback", use_container_width=True)
            
            if submit_btn:
                if title and description:
                    if submit_feedback(title, description, st.session_state.user_id):
                        st.rerun()
                else:
                    st.error("❌ Please fill in both title and description")


# View Ideas Page
elif page == "📋 View Ideas":
    st.title("📋 All Ideas")
    
    feedback_list = get_all_feedback()
    
    if not feedback_list:
        st.info("ℹ️ No ideas yet. Be the first to submit one!")
    else:
        st.markdown(f"Showing **{len(feedback_list)}** ideas")
        
        for feedback in feedback_list:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.subheader(feedback.get("title", "Untitled"))
                    st.markdown(f"_{feedback.get('description', 'No description')}_")
                    st.caption(f"By user {feedback.get('user_id')} • Posted {feedback.get('created_at', 'recently')}")
                
                with col2:
                    if st.session_state.user_id is not None:
                        col_upvote, col_downvote = st.columns(2)
                        with col_upvote:
                            if st.button("👍", key=f"upvote_{feedback['id']}", help="Upvote"):
                                submit_vote(feedback["id"], st.session_state.user_id, "upvote")
                                st.rerun()
                        with col_downvote:
                            if st.button("👎", key=f"downvote_{feedback['id']}", help="Downvote"):
                                submit_vote(feedback["id"], st.session_state.user_id, "downvote")
                                st.rerun()
                    else:
                        st.info("👤 Login to vote")
            
            st.divider()


# Top Voted Page
elif page == "🏆 Top Voted":
    st.title("🏆 Top Voted Ideas (Leaderboard)")
    
    top_ideas = get_top_ideas(limit=20)
    
    if not top_ideas:
        st.info("ℹ️ No votes yet. Check back later!")
    else:
        st.markdown(f"🏅 Top **{len(top_ideas)}** ideas")
        
        for idx, idea in enumerate(top_ideas, 1):
            with st.container():
                medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
                
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"### {medal} {idea.get('title', 'Untitled')}")
                    st.markdown(f"_{idea.get('description', 'No description')}_")
                    
                    upvotes = idea.get('upvotes', 0)
                    downvotes = idea.get('downvotes', 0)
                    net_votes = idea.get('vote_count', 0)
                    
                    st.metric(
                        "Score",
                        f"{net_votes}",
                        delta=f"{upvotes} 👍 • {downvotes} 👎"
                    )
                    st.caption(f"By **{idea.get('username', 'Unknown')}** • {idea.get('created_at', 'recently')}")
                
                if st.session_state.user_id is not None:
                    with col2:
                        col_upvote, col_downvote = st.columns(2)
                        with col_upvote:
                            if st.button("👍", key=f"top_upvote_{idea['id']}", help="Upvote"):
                                submit_vote(idea["id"], st.session_state.user_id, "upvote")
                                st.rerun()
                        with col_downvote:
                            if st.button("👎", key=f"top_downvote_{idea['id']}", help="Downvote"):
                                submit_vote(idea["id"], st.session_state.user_id, "downvote")
                                st.rerun()
            
            st.divider()
