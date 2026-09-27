
import streamlit as st
from langgraph_backend_sql_lite import chatbot,retrive_All_thread
from langchain_core.messages import HumanMessage
import uuid


#################### Utility Functions ####################

def generate_thread_id():
    return str(uuid.uuid4())


def reset_chat():
    st.session_state["thread_id"] = generate_thread_id()
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):

    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": str(thread_id)
            }
        }
    )

    if not state or not state.values:
        return []

    return state.values.get("messages", [])


#################### Session State ####################

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrive_All_thread()


add_thread(st.session_state["thread_id"])


#################### Sidebar ####################

st.sidebar.title("LangGraph Chatbot")


if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()


st.sidebar.header("My Conversations")


for thread_id in st.session_state["chat_threads"][::-1]:

    if st.sidebar.button(str(thread_id)):

        st.session_state["thread_id"] = thread_id

        messages = load_conversation(thread_id)

        temp_messages = []

        for message in messages:

            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"

            temp_messages.append({
                "role": role,
                "content": message.content
            })

        # IMPORTANT: outside the loop
        st.session_state["message_history"] = temp_messages

        st.rerun()


st.sidebar.text(
    f"Thread ID: {st.session_state['thread_id']}"
)


#################### Display Chat History ####################

for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):
        st.write(message["content"])


#################### Chat Input ####################

user_input = st.chat_input("Type here...")


if user_input:

    #################### User Message ####################

    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)


    #################### Correct LangGraph Config ####################

    config = {
        "configurable": {
            "thread_id": str(st.session_state["thread_id"])
        }
    }


    #################### AI Response ####################

    full_response = ""

    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        for message_chunk, metadata in chatbot.stream(
            {
                "messages": [
                    HumanMessage(content=user_input)
                ]
            },
            config=config,
            stream_mode="messages"
        ):

            if message_chunk.content:

                full_response += message_chunk.content

                message_placeholder.write(full_response)


    #################### Save AI Response ####################

    st.session_state["message_history"].append({
        "role": "assistant",
        "content": full_response
    })