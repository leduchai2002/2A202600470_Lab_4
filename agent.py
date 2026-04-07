from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv()

# 1. Đọc system prompt 
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=system_prompt)] + messages

    response = llm_with_tools.invoke(messages)

    # ===LOGGING===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"Trả lời trực tiếp")

    return {"messages": [response]}

# 5. Xây dựng StateGraph

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    tools_condition,
    {"tools": "tools", "__end__": END},
)
# After executing tools, go back to the agent so the model can synthesize final response.
builder.add_edge("tools", "agent")

graph = builder.compile()

# 6. Chat loop

if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý du lịch thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")
        result = graph.invoke({"messages": [HumanMessage(content=user_input)]})
        final = result["messages"][-1]
        print(f"\nTravelBuddy: {final.content}")

