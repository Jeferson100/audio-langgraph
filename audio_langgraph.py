from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from typing import Annotated, List
from langchain_core.messages import HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    SystemMessage
)
from langgraph.graph.message import add_messages

load_dotenv()

chat = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    temperature=0
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(content="""You are a helpful assistant that can answer any question. 
                      You can also say 'I don't know' if you don't know the answer.
                      Your answer should be in Portuguese."""),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)


def chat_groq(state):
    message = state['messages'][-1]
    response = chat.invoke(prompt_template.format(input=message))
    return {"messages": response.content}
    

def graph_builder():
    graph_buil = StateGraph(State)

    graph_buil.add_node("chat_groq", chat_groq)
    graph_buil.add_edge(START, "chat_groq")
    graph_buil.add_edge("chat_groq", END)

    return graph_buil

graph = graph_builder().compile()

if __name__ == "__main__":
    initial_state = {"messages": ["ola mundo"]}
    result = graph.invoke(initial_state)
    print("Resultado:", result)

