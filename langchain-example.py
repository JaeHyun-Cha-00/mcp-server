from langchain_community.llms import VLLM
from langchain.tools import Tool
from langchain.agents import initialize_agent

# Add Models Here
llm = VLLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    trust_remote_code=True,
    max_new_tokens=256,
    top_k=10,
    top_p=0.95,
    temperature=0.7,
)

# Testing fucntion (Tool)
def evaluate_satisfaction(response: str) -> str:
    """
    Evaluate satisfaction score (1–10) using vLLM-backed Llama-3.1 model.
    """
    prompt = f"""Evaluate the following response on a scale of 1 to 10 based on satisfaction.
                    Response: {response}
                    Score:
            """
    return llm(prompt)

# Tool definition
evaluation_tool = Tool(
    name="SatisfactionEvaluator",
    func=evaluate_satisfaction,
    description="Evaluates the satisfaction score (1–10) of a given response."
)

# initialize agent with the tool
agent = initialize_agent(
    tools=[evaluation_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Example usage
if __name__ == "__main__":
    claude_response = "LangChain is a framework for developing applications powered by language models."
    evaluation_result = agent.run(f"Evaluate this response: {claude_response}")
    print("Evaluation Result:", evaluation_result)
