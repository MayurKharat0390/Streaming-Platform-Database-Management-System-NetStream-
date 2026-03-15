import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# Import modules
from database import init_db
import queries

# Page Configuration
st.set_page_config(
    page_title="NetStream | Unlimited Movies & Series",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for ULTRA-PREMIUM Netflix Aesthetic
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

    /* Global Typography */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #050505 !important;
    }
    
    h1, h2, h3, .hero-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 800;
        letter-spacing: -1.5px;
    }

    /* Ultra Dark Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #250505 0%, #050505 100%);
        color: #f0f0f0;
    }

    /* Floating Metric Cards with Neon Glow */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    div[data-testid="stMetric"]:hover {
        border-color: #E50914;
        transform: translateY(-8px);
        background: rgba(229, 9, 20, 0.05);
    }

    /* Premium Button Style (Netflix Neon) */
    .stButton>button {
        background: linear-gradient(90deg, #E50914 0%, #ff4d4d 100%);
        color: white;
        border-radius: 100px;
        border: none;
        padding: 0.8rem 3.5rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 15px 45px rgba(229, 9, 20, 0.7);
        transform: scale(1.03);
        color: white;
    }

    /* Interactive Movie Cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .movie-card:hover {
        transform: scale(1.05);
        z-index: 10;
        background: rgba(255, 255, 255, 0.1);
        border-color: #E50914;
        box-shadow: 0 30px 60px rgba(0,0,0,0.9);
    }
    
    /* Overlay Content on Hover */
    .card-footer {
        padding: 20px;
        background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, transparent 100%);
    }

    /* Pill Filter Styling */
    .filter-pill {
        padding: 8px 25px;
        border-radius: 100px;
        background: rgba(255,255,255,0.05);
        color: #aaa;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.1);
        cursor: pointer;
        transition: 0.3s;
        margin-right: 15px;
    }
    .filter-pill:hover {
        background: #E50914;
        color: white;
        border-color: #E50914;
    }
            /* Ultimate Tab/Navbar Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 10px 30px;
        border-radius: 100px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent !important;
        border: none !important;
        color: #aaa !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] {
        color: #E50914 !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] div {
        color: #E50914 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: white !important;
    }

    /* User Profile section */
    .user-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(255,255,255,0.05);
        padding: 5px 15px;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-thumb { background: #E50914; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'my_list' not in st.session_state:
    st.session_state.my_list = []

# Initialize Database
@st.cache_resource
def startup_db():
    ddl = os.path.join(os.path.dirname(__file__), '..', 'schema', 'ddl.sql')
    dummy = os.path.join(os.path.dirname(__file__), '..', 'schema', 'dummy_data.sql')
    return init_db(ddl, dummy)

startup_db()

# --- TOP NAVIGATION BAR ---
header_col1, header_col2, header_col3 = st.columns([1.5, 3, 1.5])
with header_col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=140)
with header_col3:
    st.markdown("""
        <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
            <div class="user-profile">
                <span style="color: #666; font-size: 0.8rem;">ADMIN</span>
                <span style="color: white; font-weight: 600;">Root User</span>
                <div style="width: 32px; height: 32px; background: #E50914; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">R</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Create Navigation Tabs at the top
tabs = st.tabs(["📊 Dashboard", "👥 Users", "💳 Plans", "🎥 Content", "🏷️ Genres", "📜 History", "⭐ Ratings"])

# --- RENDER TABS ---

# 1. DASHBOARD
with tabs[0]:
    # IMAX Hero (Updated for Faculty)
    st.markdown("""
        <div class="imax-hero" style="background-image: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&q=80');">
            <div class="imax-overlay"></div>
            <div class="imax-content">
                <span style="background:rgba(229, 9, 20, 0.9); padding: 5px 15px; border-radius: 5px; font-weight: 800; font-size: 0.8rem; letter-spacing: 2px;">PREMIUM DOCUMENTARY</span>
                <h1 style='font-size: 5rem; color: white;'>Our Planet</h1>
                <p style='font-size: 1.2rem; color: #ddd; max-width: 650px; line-height: 1.6;'>
                    Experience our planet's natural beauty and examine how climate change impacts all living creatures in this ambitious documentary.
                </p>
                <div style="display: flex; gap: 20px; margin-top: 35px;">
                    <div style="background: white; color: black; padding: 12px 40px; border-radius: 8px; font-weight: 800; cursor: pointer; display: flex; align-items: center; gap: 10px;">
                        <span>▶</span> WATCH NOW
                    </div>
                    <div style="background: rgba(255,255,255,0.15); backdrop-filter: blur(10px); color: white; padding: 12px 40px; border-radius: 8px; font-weight: 800; cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
                        ⓘ DETAILS
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Glow Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GLOBAL AUDIENCE", f"{queries.get_total_users():,}", "↑ 12%")
    with col2:
        st.metric("LIBRARY SIZE", queries.get_total_content(), "Standard")
    with col3:
        top_rated = queries.get_top_rated_content()
        val = top_rated[0]['title'] if top_rated else "N/A"
        st.metric("CURRENT FAVORITE", val)
    with col4:
        st.metric("STREAM QUALITY", "4K Ultra HD", "HDR10+")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Trending Content (Neon Cards)
    st.markdown("<h2 style='color: #E50914; margin-bottom: 30px;'>🔥 TRENDING NOW</h2>", unsafe_allow_html=True)
    content = queries.get_all_content()
    if content:
        cols = st.columns(4)
        for i, item in enumerate(content[:4]):
            with cols[i]:
                st.markdown(f"""
                <div class="movie-card">
                    <div style="height: 180px; background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); display: flex; align-items: center; justify-content: center; position: relative; border-bottom: 2px solid #E50914;">
                        <span style="font-size: 4rem; filter: drop-shadow(0 0 10px rgba(229,9,20,0.5));">🎬</span>
                        <div style="position: absolute; top: 10px; right: 10px; background: #E50914; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: bold;">TOP 10</div>
                    </div>
                    <div style="padding: 20px;">
                        <h4 style="margin:0; font-family: 'Outfit'; color: white; font-size: 1.2rem;">{item['title']}</h4>
                        <div style="display: flex; gap: 10px; align-items: center; margin-top: 8px;">
                            <span style="color: #46d369; font-weight: bold; font-size: 0.8rem;">98% Match</span>
                            <span style="color: #888; border: 1px solid #444; padding: 0px 5px; font-size: 0.6rem; border-radius: 3px;">HD</span>
                        </div>
                        <p style="color: #999; font-size: 0.85rem; line-height: 1.4; margin-top: 15px;">{item['description'][:95]}...</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    
    # Data Insights
    st.markdown("<h2 style='color: white;'>📈 PERFORMANCE ANALYTICS</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        pop_genres = queries.get_popular_genres()
        if pop_genres:
            df_pop = pd.DataFrame(pop_genres)
            st.bar_chart(df_pop.set_index('genre_name'), color="#E50914")
    with c2:
        if top_rated:
            st.markdown("<div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
            st.markdown("**CRITICAL RATINGS**")
            st.dataframe(pd.DataFrame(top_rated)[['title', 'avg_rating']], hide_index=True, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# 2. USERS
with tabs[1]:
    st.header("User Management")
    tab1, tab2 = st.tabs(["View Users", "Add New User"])
    with tab1:
        users = queries.get_all_users()
        if users:
            df = pd.DataFrame(users)
            st.dataframe(df, use_container_width=True)
            user_to_del = st.selectbox("Select User to Delete", df['user_id'].tolist(), format_func=lambda x: df[df['user_id']==x]['username'].values[0])
            if st.button("🗑️ Delete User"):
                if queries.delete_user(user_to_del):
                    st.success("User deleted!")
                    st.rerun()
        else:
            st.info("No users found.")
    with tab2:
        with st.form("add_user_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("➕ Add User")
            if submitted:
                if queries.add_user(username, email, password):
                    st.success(f"User {username} created!")
                
# 3. PLANS
with tabs[2]:
    st.header("Subscription Plans")
    t1, t2, t3 = st.tabs(["Active Subscriptions", "Assign Subscription", "Manage Plans"])
    with t1:
        subs = queries.get_user_subscriptions()
        if subs:
            st.dataframe(pd.DataFrame(subs), use_container_width=True)
            
    with t2:
        users = queries.get_all_users()
        plans = queries.get_all_plans()
        if users and plans:
            with st.form("assign_sub"):
                u_id = st.selectbox("User", [u['user_id'] for u in users], format_func=lambda x: next(u['username'] for u in users if u['user_id']==x))
                p_id = st.selectbox("Plan", [p['plan_id'] for p in plans], format_func=lambda x: next(p['plan_name'] for p in plans if p['plan_id']==x))
                start = st.date_input("Start Date", datetime.now())
                duration = next(p['duration_months'] for p in plans if p['plan_id']==p_id)
                end = start + timedelta(days=30*duration)
                st.info(f"End date will be automatically set to: {end}")
                
                if st.form_submit_button("✅ Assign"):
                    if queries.assign_subscription(u_id, p_id, start, end):
                        st.success("Subscription assigned!")
        else:
            st.warning("Ensure users and plans exist.")

    with t3:
        with st.form("add_plan"):
            p_name = st.text_input("Plan Name")
            price = st.number_input("Price ($)", min_value=0.0)
            dur = st.number_input("Duration (Months)", min_value=1)
            if st.form_submit_button("➕ Add Plan"):
                if queries.add_plan(p_name, price, dur):
                    st.success("Plan added!")

# 4. CONTENT
with tabs[3]:
    st.header("Content Management")
    c_tab1, c_tab2 = st.tabs(["Explore Content", "Add Content"])
    
    with c_tab1:
        search = st.text_input("🔍 Search by Title or Director")
        if search:
            content = queries.search_content(search)
        else:
            content = queries.get_all_content()
            
        if content:
            st.dataframe(pd.DataFrame(content), use_container_width=True)
        else:
            st.info("No content found.")
            
    with c_tab2:
        with st.form("add_content"):
            title = st.text_input("Title")
            ctype = st.selectbox("Type", ["Movie", "Series"])
            year = st.number_input("Release Year", min_value=1900, max_value=2025, value=2024)
            dur = st.number_input("Duration (min)", min_value=1, value=120)
            director = st.text_input("Director")
            desc = st.text_area("Description")
            
            if st.form_submit_button("➕ Add Content"):
                if queries.add_content(title, ctype, year, dur, director, desc):
                    st.success(f"{ctype} '{title}' added!")

# 5. GENRES
with tabs[4]:
    st.header("Genre Management")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Add Genre")
        gname = st.text_input("Genre Name")
        if st.button("➕ Create"):
            queries.add_genre(gname)
            st.success("Genre created!")
            
    with c2:
        st.subheader("Assign Genre to Content")
        all_c = queries.get_all_content()
        all_g = queries.get_genres()
        if all_c and all_g:
            c_id = st.selectbox("Content", [c['content_id'] for c in all_c], format_func=lambda x: next(c['title'] for c in all_c if c['content_id']==x))
            g_id = st.selectbox("Genre", [g['genre_id'] for g in all_g], format_func=lambda x: next(g['genre_name'] for g in all_g if g['genre_id']==x))
            if st.button("🔗 Link"):
                queries.link_content_genre(c_id, g_id)
                st.success("Linked successfully!")

# 6. HISTORY
with tabs[5]:
    st.header("Global Watch History")
    
    with st.expander("➕ Record New Watch Event"):
        users = queries.get_all_users()
        content = queries.get_all_content()
        if users and content:
            u_id = st.selectbox("Who watched?", [u['user_id'] for u in users], format_func=lambda x: next(u['username'] for u in users if u['user_id']==x))
            c_id = st.selectbox("What was watched?", [c['content_id'] for c in content], format_func=lambda x: next(c['title'] for c in content if c['content_id']==x))
            if st.button("💾 Record"):
                queries.add_watch_history(u_id, c_id)
                st.success("History updated!")
    
    history = queries.get_watch_history()
    if history:
        st.table(pd.DataFrame(history))

# 7. RATINGS
with tabs[6]:
    st.header("Ratings & Reviews")
    
    with st.expander("✍️ Leave a Review"):
        users = queries.get_all_users()
        content = queries.get_all_content()
        if users and content:
            u_id = st.selectbox("User", [u['user_id'] for u in users], format_func=lambda x: next(u['username'] for u in users if u['user_id']==x), key="rate_u")
            c_id = st.selectbox("Content", [c['content_id'] for c in content], format_func=lambda x: next(c['title'] for c in content if c['content_id']==x), key="rate_c")
            score = st.slider("Rating", 1, 5, 5)
            rev = st.text_area("Review")
            if st.button("⭐ Submit Rating"):
                queries.add_rating(u_id, c_id, score, rev)
                st.success("Review submitted/updated!")

    ratings = queries.get_ratings_with_details()
    if ratings:
        st.dataframe(pd.DataFrame(ratings), use_container_width=True)
