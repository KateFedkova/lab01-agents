# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .environment import lookup_code_smell

load_dotenv()

MODEL = "gemini-3.1-flash-lite"

INSTRUCTION = """
ROLE: An educational agent focused on code smells for programming students.
PURPOSE: To answer questions about specific code smells based exclusively on
verified data returned by the `lookup_code_smell` tool.
LANGUAGE: English, unless the user requests a different language.
BEHAVIOR RULES:
1. Before providing information about a specific code smell, call `lookup_code_smell`
separately for each one mentioned.
2. If the result begins with "NOT_FOUND," explicitly state that no verified
data is available; do not supplement the answer with your own knowledge.
3. When discussing specific code smells, rely solely on facts derived from the
tool's output.
4. For general questions (e.g., "What is a code smell?"), provide a brief
response without invoking the tool.
5. Do not call the tool more than once with the same argument.
LIMITATIONS: Do not perform actions for which no tool exists; do not invent sources.
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=INSTRUCTION,
    tools=[lookup_code_smell],
)

app = App(
    root_agent=root_agent,
    name="app",
)
