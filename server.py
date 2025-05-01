"""
A generative AI chat interface using Streamlit.
Agent interacts with a Púca MCP server allowing live lookups of data from OpenStreetMap
"""

import asyncio
import os
import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP


def load_system_prompt(prompt_file):
    """Load the system prompt from a text file."""
    try:
        with open(prompt_file, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"System prompt file '{prompt_file}' not found!")
        return None
    except Exception as e:
        st.error(f"Error loading system prompt: {e}")
        return None


async def main():
    """Main function for running the streamlit interface with a pydantic AI agent"""
    st.set_page_config(
        page_title="Púca",
        page_icon="puca.svg",
        layout="centered",
        initial_sidebar_state="auto",
    )
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("puca.svg", use_container_width=True)
    with col2:        
        st.title("Púca")
    mcp_server_url = os.getenv("MCP_SERVER_URL")
    if not mcp_server_url:
        st.error("Environment variable MCP_SERVER_URL is not set!")
        return
    system_prompt = load_system_prompt("system_prompt.md")
    if not system_prompt:
        return

    server = MCPServerHTTP(url=mcp_server_url)
    agent = Agent(
        "openai:gpt-4o", mcp_servers=[server], system_prompt=system_prompt
    )

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "history" not in st.session_state:
        st.session_state.history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    async with agent.run_mcp_servers():
        if prompt := st.chat_input("Ask me anything?"):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                response = await agent.run(
                    user_prompt=prompt, message_history=st.session_state.history
                )
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.output}
                )
                st.session_state.history = response.all_messages()
                st.markdown(response.output)


if __name__ == "__main__":
    asyncio.run(main())
