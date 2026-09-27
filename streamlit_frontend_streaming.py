# import streamlit  as st
# from Langgraph_Backend import chatbot
# from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,SystemMessage
# import uuid

# #################### utility functions ####################
# CONFIG = {
#     "configurable": {
#         "thread_id": "st.session_state['thread_id']"
#     }
# }

# def generate_thread_id():
#     thread_id=uuid.uuid4()
#     return thread_id

# def reset_chat():
#     st.session_state['thread_id']=generate_thread_id()
#     add_thread(st.session_state['thread_id'])
#     st.session_state["message_history"]=[]

# def add_thread(thread_id):
#     if thread_id  not in st.session_state['chat_threads']:
#         st.session_state['chat_threads'].append(thread_id)


# def load_conversation(thread_id):
#     state = chatbot.get_state(
#         config={"configurable": {"thread_id": str(thread_id)}}
#     )

#     if not state or not state.values:
#         return []

#     return state.values.get("messages", [])
# # def load_conversation(thread_id):
# #     return chatbot.get_state(config={'configurable':{'thread_id':thread_id}}).values['messages']





# if 'thread_id' not in st.session_state:
#     st.session_state['thread_id']=generate_thread_id()

# # CONFIG={"configurabel":{'thread_id':'thread_id:-1'}}
# # 

# if "message_history" not in st.session_state:
#     st.session_state["message_history"]=[]

# if 'chat_threads' not in st.session_state:
#     st.session_state['chat_threads']=[]



# add_thread(st.session_state['thread_id'])


# st.sidebar.title("Langgraph Chatbot")
# if st.sidebar.button('New Chat'):
#     reset_chat()


# st.sidebar.header('My Conversatiom')
# for thread_id in st.session_state['chat_threads'][::-1]:
#     if st.sidebar.button(str(thread_id)):
#         st.session_state['thread_id']=thread_id
#         messages=load_conversation(thread_id)
#         temp_messgages=[]
#         for message in messages:
#             if isinstance(message,HumanMessage):
#                 role="user"
#                 temp_messgages.append({"role":role,"content":message.content})
#             else :
#                 role="assistant"
#                 temp_messgages.append({"role":role,"content":message.content})
#             st.session_state['message_history']=temp_messgages
            

# st.sidebar.text(st.session_state['thread_id'])


# #loading the chata
# for message in st.session_state["message_history"]:
#     with st.chat_message(message["role"]):
#         st.text(message["content"])

# # with st.chat_message("user"):
# #     st.text("hello i am a user")
# # with st.chat_message("Assistant"):
# #     st.text("hello i am an AI")

# user_input=st.chat_input("Type here...")

# if user_input:
#     st.session_state['message_history'].append({"role":"user","content":user_input})
#     # message_history.append({"role":"user","content":user_input})
#     with st.chat_message("user"):
#         st.text(user_input)

   
#     full_response=""
#     with st.chat_message("assistant"):
#         message_placeholder=st.empty()
#         for message_chunk ,metadata in chatbot.stream({
#                         "messages": [
#                             HumanMessage(content=user_input)
#                         ]}
#                     ,
#                     config=CONFIG,
#                     stream_mode="messages"):

#                 if message_chunk.content:
#                     full_response+=message_chunk.content
#                     message_placeholder.text(full_response)
#                     # st.session_state['message_history'].append({"role":"assistant","content":message_chunk.content})
#                     # with st.chat_message("assistant"):
#                     #     st.text(message_chunk.content)
#     # ai_messgae=response["messages"][-1]

#     # st.session_state['message_history'].append({"role":"assistant","content":ai_messgae.content})
#     # with st.chat_message("assistant"):
#     #     st.text(ai_messgae)




import streamlit as st
from Langgraph_Backend import chatbot
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
    st.session_state["chat_threads"] = []


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