import streamlit as st
from datetime import datetime, date
import calendar
from utils import helpers

def render():
    st.title("Calendar")
    st.markdown("Month view — click a day to see posts or add one.")

    # Filters
    status_filter = st.multiselect("Filter by status", options=["Draft", "Approved", "Scheduled", "Posted", "Failed"], default=[])
    platform_filter = st.multiselect("Filter by platform", options=["Instagram", "Facebook", "Both"], default=[])\n
    # Choose month to render
    today = date.today()
    year = st.selectbox("Year", [today.year - 1, today.year, today.year + 1], index=1)
    month = st.selectbox("Month", list(range(1, 13)), index=today.month - 1)

    cal = calendar.monthcalendar(year, month)
    posts_by_date = helpers.get_posts_grouped_by_day(year, month, status_filter=status_filter, platform_filter=platform_filter)

    cols = st.columns(7)
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for idx, wd in enumerate(weekdays):
        cols[idx].markdown(f"**{wd}**")

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            with cols[i]:
                if day == 0:
                    st.write("")
                else:
                    day_date = date(year, month, day)
                    st.write(f"**{day}**")
                    day_posts = posts_by_date.get(day_date.isoformat(), [])
                    for p in day_posts:
                        badge = f"[{p.status}]"
                        st.markdown(f"- **{p.title}** {badge}")
                    if st.button("View / Add", key=f"view_{year}_{month}_{day}"):
                        # Set session state and navigate to Post editor with date
                        st.session_state["page"] = "Create / Edit Post"
                        st.session_state["editor_date"] = day_date.isoformat()
                        st.experimental_rerun()