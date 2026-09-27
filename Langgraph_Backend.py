from langgraph.graph import StateGraph ,START,END
from typing import TypedDict ,Annotated
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,SystemMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

# from streamlit_frontent import CONFIG

llm=ChatOllama(model="llama3:latest",temperature=0)
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}

checkpointer=InMemorySaver()
graph=StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)
# CONFIG = {
#     "configurable": {
#         "thread_id": "thread_id:-1"
#     }
# }
# for message_chunk ,metadata in chatbot.stream({
#                 "messages": [
#                     HumanMessage(content="how to make pasta")
#                 ]}
#             ,
#             config=CONFIG,
#             stream_mode="messages"):
#     # print(message_chunk,"__")
#     print(message_chunk.content, end="", flush=True)
        



