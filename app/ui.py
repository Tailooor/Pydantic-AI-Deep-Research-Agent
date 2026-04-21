from __future__ import annotations

from typing import Any

import gradio as gr

from app.agent import build_agent
from app.config import get_settings


CUSTOM_CSS = """
.gradio-container {
    max-width: 900px !important;
}
#app-shell {
    border: 1px solid #d9e1d7;
    border-radius: 24px;
    background:
        radial-gradient(circle at top left, #eef7ea 0%, transparent 30%),
        linear-gradient(180deg, #fbf8ef 0%, #f7f3e8 100%);
    box-shadow: 0 20px 60px rgba(63, 74, 52, 0.08);
}
"""


def build_demo() -> gr.Blocks:
    settings = get_settings()
    agent = build_agent(settings)

    def chat(
        message: str, chat_history: list[dict[str, Any]], model_history: list[Any]
    ) -> tuple[list[dict[str, Any]], str, list[Any]]:
        user_message = message.strip()
        if not user_message:
            return chat_history, "", model_history

        result = agent.run_sync(
            user_message,
            message_history=model_history or None,
        )
        reply = result.output.strip()

        updated_chat = list(chat_history)
        updated_chat.append({"role": "user", "content": user_message})
        updated_chat.append({"role": "assistant", "content": reply})

        return updated_chat, "", result.all_messages()

    def clear_chat() -> tuple[list[Any], list[Any]]:
        return [], []

    with gr.Blocks(title=settings.app_title, fill_width=True) as demo:
        gr.Markdown(
            f"# {settings.app_title}\n"
            f"Simple Pydantic AI agent using `{settings.openrouter_model}` through OpenRouter.\n"
            "Responses are intentionally short."
        )

        with gr.Column(elem_id="app-shell"):
            chatbot = gr.Chatbot(height=520, show_label=False, layout="bubble")
            model_history = gr.State([])

            with gr.Row():
                prompt = gr.Textbox(
                    placeholder="Ask something...",
                    lines=2,
                    scale=8,
                    show_label=False,
                )
                send = gr.Button("Send", variant="primary", scale=1)

            clear = gr.Button("Clear chat")

        send.click(
            fn=chat,
            inputs=[prompt, chatbot, model_history],
            outputs=[chatbot, prompt, model_history],
        )
        prompt.submit(
            fn=chat,
            inputs=[prompt, chatbot, model_history],
            outputs=[chatbot, prompt, model_history],
        )
        clear.click(fn=clear_chat, outputs=[chatbot, model_history])

    return demo


def launch_app() -> None:
    settings = get_settings()
    demo = build_demo()
    demo.launch(
        server_name=settings.app_host,
        server_port=settings.app_port,
        theme=gr.themes.Soft(
            primary_hue="green",
            secondary_hue="amber",
            neutral_hue="stone",
        ),
        css=CUSTOM_CSS,
    )
