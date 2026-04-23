import streamlit as st
from retrieve import retrieve
from rag import generate_answer

st.set_page_config(
    page_title="Incident RAG Assistant",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ Smart Incident Knowledge Assistant (RAG)")
st.caption("Ask questions about past incidents to find root causes and fixes")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



user_query = st.chat_input("Describe your incident issue...")

if user_query is not None:

    # ✅ Normalize type (fixes Streamlit warning)
    user_query = str(user_query)

    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Retrieve similar incidents
    with st.spinner("Searching incident history..."):
        results = retrieve(user_query)

    # Generate answer using Claude
    with st.spinner("Analyzing with AI..."):
        answer = generate_answer(user_query, results)

    # Show assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    # Sidebar: Similar incidents
    with st.sidebar:
        st.subheader("🔍 Similar Incidents")

        for r in results:
            m = r["metadata"]

            with st.expander(f"{m.get('title')} ({m.get('severity')}) — {r['confidence']}% match"):
                st.write(f"**Service:** {m.get('service')}")
                st.write(f"**Symptoms:** {m.get('symptoms')}")
                st.write(f"**Root Cause:** {m.get('root_cause')}")
                st.write(f"**Resolution:** {m.get('resolution')}")
                st.write(f"**Distance:** {round(r['distance'], 3)}")
                st.progress(max(0.0, min(1.0, r['confidence'] / 100)))
                st.write(f"**Confidence:** {r['confidence']}%")