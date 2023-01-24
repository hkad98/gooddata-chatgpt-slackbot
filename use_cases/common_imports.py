from __future__ import annotations

import os
from typing import Any

# Socker Mode Client, but this time not using official Python SDK but more high-level slack_bolt module to ease
# development of conversations
import slack_bolt

# loading env. variables
from dotenv import load_dotenv

# ChatGPT unofficial Python package
from revChatGPT.ChatGPT import Chatbot
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
