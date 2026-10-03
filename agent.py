from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from agent_setup import get_company_stock_info, get_date, retrieve_documents

#Model, it is a local model
model = ChatOllama(
     base_url="http://localhost:11434",
    model="qwen3",
    temperature=0.1
)

#allow to save chat history
checkpointer = InMemorySaver()


#config threads for memory test
config = {
    "configurable": {
        "thread_id": 1
    }
}

#agent 
agent = create_agent(
    model=model,
    tools=[get_company_stock_info, get_date, retrieve_documents],
    system_prompt="You are a financial assistant. You have access to the following tools: get_company_stock_info, get_date, retrieve_documents. Use these tools to provide accurate and relevant information to the user.",
    checkpointer=checkpointer
)

def run_agent():
    while True:
        question = input("\nYou: ")

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!") 
            break

        print("Assistant: ", end="", flush=True)

        for chunk in agent.stream(
            {
                "messages": [
                    {"role": "user", "content": question}
                ]
            },
            config=config,
            stream_mode="messages",
        ):
            message, metadata = chunk

            if message.content:
                print(message.content, end="", flush=True)

        print()
        
