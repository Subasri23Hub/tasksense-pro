import streamlit as st
from core.retriever import build_vectorstore


def render_settings():
    """Render the settings/preferences page."""
    st.markdown('<div class="section-header">⚙️ Settings & Preferences</div>', unsafe_allow_html=True)

    st.markdown("#### 🔑 API Configuration")
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.get("api_key_override", ""),
        placeholder="Leave blank to use .env file",
        help="Optionally override the API key from .env"
    )
    if api_key:
        st.session_state["api_key_override"] = api_key
        st.success("API key saved for this session.")

    st.divider()

    st.markdown("#### 🗂️ Vector Store")
    st.markdown(
        "The RAG knowledge base is embedded and stored locally. "
        "Rebuild if you update `data/productivity_knowledge.txt`."
    )
    if st.button("🔄 Rebuild Vector Store"):
        with st.spinner("Rebuilding vector store..."):
            try:
                build_vectorstore()
                st.success("Vector store rebuilt successfully!")
            except Exception as e:
                st.error(f"Failed to rebuild: {e}")

    st.divider()

    st.markdown("#### 🎨 About TaskSense Pro")
    st.markdown("""
    **TaskSense Pro** is a premium AI planning assistant built with:
    - 🔗 **LangChain** — prompt templates, RAG, retriever
    - 🤖 **Gemini** — LLM backbone
    - 📦 **FAISS** — local vector store
    - 🐍 **Pydantic** — structured output
    - 🖥️ **Streamlit** — UI layer

    *Version 1.0.0*
    """)
