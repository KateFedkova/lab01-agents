"""Decision-making component: LLM as a policy, policy(state) -> action."""
 
import json
import os
 
from dotenv import load_dotenv
from google import genai
from google.genai import types
 
from .errors import DecisionError
 
load_dotenv()
 
MODEL = os.getenv("GEMINI_MODEL")
 
AGENT_INSTRUCTION = """
You are the decision component of a small educational AI agent.
You do not chat. On every call you choose exactly one action.
 
Available actions:
1. lookup_code_smell
   Use it when verified information about a code smell is needed.
   Arguments: {"name": string}  e.g. "duplicated code", "long method", "large class"
2. finish
   Use it when the verified observations are enough to reach the goal,
   or when the environment reported that the information does not exist.
   Arguments: {"answer": string}   final answer in Ukrainian
 
Return valid JSON only:
{
    "action": "lookup_code_smell | finish",
    "arguments": {...},
    "decision_summary": "one short sentence: why this action"
}
 
Rules:
- Use only facts from VERIFIED OBSERVATIONS in the final answer.
- If an observation starts with NOT_FOUND, say the information is missing; do not invent it.
- If an observation starts with ERROR, fix your previous decision.
- Do not repeat a lookup that is already present in the observations.
- decision_summary is one sentence; do not reveal hidden chain-of-thought.
"""
 
_client: genai.Client | None = None
 
 
def get_client() -> genai.Client:
    """Lazy initialization: tests without a network import the module without a key."""
    global _client
    if _client is None:
        _client = genai.Client()
    return _client
 
 
def build_observation(goal: str, observations: list[str], step: int, max_steps: int) -> str:
    """OBSERVE: forms what the model sees at the current step."""
    known = "\n".join(f"- {item}" for item in observations) or "None yet."
    return (
        f"GOAL:\n{goal}\n\n"
        f"CURRENT STEP: {step} of {max_steps}\n\n"
        f"VERIFIED OBSERVATIONS:\n{known}\n\n"
        "AVAILABLE ACTIONS: lookup_lifecycle, finish\n"
        "Choose the next action."
    )
 
 
def parse_decision(text: str | None) -> dict:
    """Converts the model's response text into a dictionary or raises a DecisionError."""
    try:
        decision = json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise DecisionError(f"invalid JSON from model: {exc}") from exc
    if not isinstance(decision, dict):
        raise DecisionError("decision must be a JSON object")
    return decision
 
 
def get_decision(goal: str, observations: list[str], step: int, max_steps: int) -> dict:
    """REASON: A single LLM call returns a single structured solution."""
    prompt = build_observation(goal, observations, step, max_steps)
    response = get_client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=AGENT_INSTRUCTION,
            response_mime_type="application/json",
        ),
    )
    return parse_decision(response.text)
