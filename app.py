import streamlit as st

from src.adaptive_router import route_query
from src.retriver import retrieve
from src.generator import generate_answer


st.set_page_config(
    page_title="Adaptive RAG College Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Adaptive RAG College Assistant")
st.caption("Powered by Python, Semantic Search and Ollama Llama 3.2")

# Sidebar
with st.sidebar:
    st.title("About Project")
    st.write(
        "An intelligent college assistant using "
        "Adaptive Retrieval-Augmented Generation."
    )

    st.divider()
    st.subheader("Technologies")
    st.write("🐍 Python")
    st.write("🧠 Sentence Transformers")
    st.write("🦙 Ollama - Llama 3.2")
    st.write("🔎 Semantic Search")
    st.write("🌐 Streamlit")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View Sources and Evidence"):

                st.write("Selected Documents:")
                for filename in message["selected_files"]:
                    st.write(f"📄 {filename}")

                st.divider()

                for score, filename, sentence in message["sources"]:
                    st.write(f"**Source:** {filename}")
                    st.write(f"**Similarity:** {score:.3f}")
                    st.write(f"**Evidence:** {sentence}")
                    st.divider()


# Chat input
query = st.chat_input("Ask something about your college...")


if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):

        with st.spinner("Searching documents and generating answer..."):

            try:
                selected_files = route_query(query)

                if not selected_files:
                    answer = (
                        "I couldn't find a matching college document "
                        "for your question."
                    )
                    results = []

                else:
                    results = retrieve(query)

                    if not results:
                        answer = (
                            "I couldn't find sufficiently relevant "
                            "information in the available documents."
                        )
                    else:
                        answer = generate_answer(query, results)

                st.markdown(answer)

                if results:
                    with st.expander("View Sources and Evidence"):

                        st.write("Selected Documents:")
                        for filename in selected_files:
                            st.write(f"📄 {filename}")

                        st.divider()

                        for score, filename, sentence in results:
                            st.write(f"**Source:** {filename}")
                            st.write(f"**Similarity:** {score:.3f}")
                            st.write(f"**Evidence:** {sentence}")
                            st.divider()

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "selected_files": selected_files,
                    "sources": results
                })

            except Exception as error:
                st.error(f"Something went wrong: {error}")