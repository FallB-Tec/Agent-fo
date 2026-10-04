from langchain.agents import create_agent
from langchain.messages import AIMessage
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from agent_setup import ResponseFormat, get_company_stock_info, get_date, retrieve_documents

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
    system_prompt="""You are a financial assistant.

    Use tools whenever they are needed to obtain accurate information.

    When answering a user's question:
    - Answer only what the user asked for.
    - Do not provide additional financial metrics, trends, events, or analysis unless explicitly requested.
    - Do not add information simply because it is available from a tool.
    - Do not speculate, estimate, or invent financial information.
    - Any numerical financial information must come directly from a tool result or a deterministic calculation performed by a tool.
    - Do not perform financial calculations yourself when a tool can perform them.
    - Clearly distinguish between stock Open, High, Low, and Close prices.

    When using company_metrics:
    - Select only the metric necessary to answer the user's question.
    - Do not request or calculate additional metrics unless the user asks for them.
    - Use the exact metric that matches the user's request.
    - Treat the tool result as the source of truth for numerical values.

    Keep the final answer concise and directly relevant to the user's question.""",
    checkpointer=checkpointer,
    response_format=ResponseFormat
)

def run_agent():
    while True:
        question = input("\nYou: ")

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        print("Assistant: ", end="", flush=True)

        for message, _ in agent.stream(
            {
                "messages": [
                    {"role": "user", "content": question}
                ]
            },
            config=config,
            stream_mode="messages",
        ):
            if isinstance(message, AIMessage) and message.content:
                print(message.content, end="", flush=True)

        print()
        
