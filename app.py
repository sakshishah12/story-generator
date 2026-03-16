import streamlit as st
from scene_loader import get_themes, get_random_query
from retriever import hybrid_retrieval
from llm import generate_story

st.title("📜 Ramayana Story Explorer")

themes = get_themes()

selected_theme = st.selectbox(
    "Choose a theme",
    themes
)

if st.button("Generate Story"):

    query = get_random_query(selected_theme)

    st.subheader("Scene Prompt")
    st.write(query)

    with st.spinner("Retrieving verses..."):
        contexts= hybrid_retrieval(query)
    
    clean_docs = []

    for d in contexts:
        clean_docs.append({
            "kanda": d.metadata.get("kanda"),
            "canto": d.metadata.get("canto"),
            "scene_id": d.metadata.get("scene_id"),
            "theme": d.metadata.get("theme"),
            "characters": d.metadata.get("characters"),
            "text": d.page_content
        })

    with st.spinner("Generating story..."):
        story = generate_story(query, contexts)

    st.subheader("Generated Story")
    st.write(story)

    st.subheader("Source Passages")

    for c in contexts:
        st.markdown(f"""
        **Kanda:** {c.metadata["kanda"]}
        **Canto:** {c.metadata['canto']}

        {c['page_content'][:400]}...
        """)