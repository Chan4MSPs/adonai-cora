import streamlit as st
from datetime import datetime
from utils import helpers, db
from pathlib import Path

def render():
    st.title("Create / Edit Post")
    st.markdown("Create a new post or edit an existing one. This demo stores media locally.")

    session = db.get_session()
    post_id = st.session_state.get("editing_post_id", None)
    edit_post = None
    if post_id:
        edit_post = helpers.get_post_by_id(post_id)

    # Pre-fill date from calendar navigation if provided
    initial_date = st.session_state.pop("editor_date", None)

    with st.form("post_form"):
        title = st.text_input("Post title", value=edit_post.title if edit_post else "")
        platform = st.selectbox("Platform", options=["Instagram", "Facebook", "Both"], index=["Instagram", "Facebook", "Both"].index(edit_post.platform if edit_post else "Instagram"))
        scheduled_at = st.datetime_input("Scheduled date & time (optional)", value=edit_post.scheduled_at if edit_post and edit_post.scheduled_at else (datetime.fromisoformat(initial_date) if initial_date else None))
        caption = st.text_area("Caption", value=edit_post.caption if edit_post else "", height=180)
        hashtags = st.text_input("Hashtags (comma-separated)", value=edit_post.hashtags if edit_post else "")
        st.markdown("Upload an image (required for Approved/Scheduled)")
        # If editing and existing media, show preview
        if edit_post and edit_post.media_path:
            st.image(edit_post.media_path, caption="Current media", width=240)

        status = st.selectbox("Status", options=["Draft", "Approved", "Scheduled", "Posted", "Failed"], index=["Draft", "Approved", "Scheduled", "Posted", "Failed"].index(edit_post.status if edit_post else "Draft"))

        submitted = st.form_submit_button("Save")
        if submitted:
            # Validation
            errors = []
            if status == "Scheduled" and not scheduled_at:
                errors.append("Scheduled posts require date and time.")
            if status in ("Approved", "Scheduled") and (not caption.strip() or (not uploaded and not (edit_post and edit_post.media_path))):
                errors.append("Approved/Scheduled posts require caption and media.")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                media_path = edit_post.media_path if edit_post else None
                if uploaded:
                    media_path = helpers.save_uploaded_media(uploaded)
                if edit_post:
                    helpers.update_post(edit_post.id, title=title, platform=platform, scheduled_at=scheduled_at, caption=caption, hashtags=hashtags, media_path=media_path, status=status)
                    st.success("Post updated.")
                else:
                    new = helpers.create_post(title=title, platform=platform, scheduled_at=scheduled_at, caption=caption, hashtags=hashtags, media_path=media_path, status=status)
                    st.success("Post created.")
                # After save, clear editor state and go to Dashboard
                st.session_state.pop("editing_post_id", None)
                st.session_state["page"] = "Dashboard"
                st.experimental_rerun()

    st.markdown("---")
    # Actions for existing post
    if edit_post:
        col1, col2, col3 = st.columns(3)
        if col1.button("Approve"):
            helpers.update_post(edit_post.id, status="Approved")
            st.success("Post approved.")
            st.experimental_rerun()
        if col2.button("Mark as Posted"):
            helpers.update_post(edit_post.id, status="Posted")
            helpers.record_publish_log(edit_post.id, result="success", message="Marked as posted (demo).")
            st.success("Marked as posted.")
            st.experimental_rerun()
        if col3.button("Delete"):
            helpers.delete_post(edit_post.id)
            st.success("Deleted post.")
            st.session_state["page"] = "Dashboard"
            st.experimental_rerun()

    # Quick list of recent posts to edit
    st.sidebar.subheader("Recent posts")
    recent = helpers.get_posts(limit=10)
    for p in recent:
        if st.sidebar.button(f"Edit: {p.title}", key=f"edit_{p.id}"):
            st.session_state["editing_post_id"] = p.id
            st.experimental_rerun()
