from langgraph.graph import StateGraph ,START,END
from typing import TypedDict ,Annotated
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage,SystemMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import sqlite3

# from streamlit_frontent import CONFIG

llm=ChatOllama(model="llama3:latest",temperature=0)
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)
    return {'messages':[response]}

conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)


checkpointer=SqliteSaver(conn=conn)
graph=StateGraph(ChatState)
graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

chatbot=graph.compile(checkpointer=checkpointer)

def  retrive_All_thread():
   all_thread=set()

   for checkpoints in checkpointer.list(None):
    all_thread.add(checkpoints.config["configurable"]["thread_id"])

   return all_thread