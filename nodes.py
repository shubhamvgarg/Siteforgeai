from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from state import *
load_dotenv()

def get_llm():
    return ChatNVIDIA(
        # model="nvidia/ising-calibration-1-35b-a3b",
        model="google/gemma-3n-e4b-it",
        temperature=0.2,
        top_p=0.7,
    max_tokens=1024,
  )

def analyse_input(state):
    user_input = state.get("user_input")

    structured_llm = get_llm().with_structured_output(PromptOutput)

    prompt = f"""
    Analyze the following user input and generate a clear, high-quality plain English prompt
    that can be used to create a website.

    User input: {user_input}
    """

    res = structured_llm.invoke(prompt)

    return {"prompt_to_use_from_user": res.website_prompt}

def analyse_requirements(state):
    prompt_to_use_from_user = state.get("prompt_to_use_from_user")
    structured_llm = get_llm().with_structured_output(RequirementsOutput)

    prompt = f"""
    You are a Technical lead Senior developer and Analyze the following user input and breakdown high-quality plain English requirements required for given input

    User input: {prompt_to_use_from_user}
    """

    res = structured_llm.invoke(prompt)

    return {"requirements": res}
