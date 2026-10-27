import streamlit as st

from chunking import chunk_pages
from loaders import SUPPORTED, load_pages
from rag import answer
from store import VectorStore

st.set_page_config(page_title="DocuMind", page_icon="📄")


@st.cache_resource
def get_store() -> VectorStore:
    return VectorStore()


store = get_store()
st.session_state.setdefault("messages", [])

with st.sidebar:
    st.header("Documents")
    files = st.file_uploader("Upload", type=list(SUPPORTED), accept_multiple_files=True)
    if st.button("Index files", disabled=not files):
        with st.spinner("Indexing..."):
            for f in files:
                pages = load_pages(f.name, f.getvalue())
                n = store.add(chunk_pages(f.name, pages))
                st.success(f"{f.name}: {n} chunks")
    st.divider()
    for src in store.sources():
        if st.button(f"🗑 {src}", key=f"del-{src}"):
            store.delete_source(src)
            st.rerun()

st.title("DocuMind")
st.caption("Ask questions about your documents.")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if q := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            text, hits = answer(store, q)
        st.markdown(text)
        with st.expander("Sources"):
            for i, h in enumerate(hits, 1):
                st.markdown(f"**[{i}] {h.source}, p.{h.page}** (sim {h.score:.2f})")
                st.caption(h.text[:300] + "...")
    st.session_state.messages.append({"role": "assistant", "content": text})
