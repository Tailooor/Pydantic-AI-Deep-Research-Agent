from __future__ import annotations

import json

import gradio as gr

from app.config import get_settings
from app.research import DeepResearchService


CUSTOM_CSS = """
.gradio-container {
    max-width: 1100px !important;
}
#app-shell {
    border: 1px solid #d6ddd0;
    border-radius: 26px;
    background:
        radial-gradient(circle at top left, #edf7e7 0%, transparent 28%),
        radial-gradient(circle at bottom right, #f6ecd8 0%, transparent 26%),
        linear-gradient(180deg, #f9f6ed 0%, #f3efe3 100%);
    box-shadow: 0 22px 70px rgba(59, 71, 43, 0.08);
}
#report-box {
    border-radius: 18px;
}
"""


def build_demo() -> gr.Blocks:
    settings = get_settings()
    research_service = DeepResearchService(settings)

    def generate_report(user_input: str) -> tuple[str, str]:
        cleaned_input = user_input.strip()
        if not cleaned_input:
            return "Please enter a stock ticker or research query.", "{}"

        try:
            run = research_service.run(cleaned_input)
        except Exception as exc:
            return f"Research failed: {exc}", "{}"

        plan_json = json.dumps(run.plan.model_dump(), indent=2)
        return run.to_markdown(), plan_json

    with gr.Blocks(title=settings.app_title, fill_width=True) as demo:
        gr.Markdown(
            f"# {settings.app_title}\n"
            f"Enter a stock ticker like `NVDA` or a free-text research question. "
            f"The app uses DuckDuckGo for multi-step web discovery and `{settings.openrouter_model}` for planning and report writing."
        )

        with gr.Column(elem_id="app-shell"):
            prompt = gr.Textbox(
                label="Research input",
                placeholder="Examples: NVDA | Tesla competition and market positioning | AI infrastructure demand outlook",
                lines=3,
            )

            with gr.Row():
                run_button = gr.Button("Generate Report", variant="primary")
                clear_button = gr.Button("Clear")

            report = gr.Markdown(elem_id="report-box")
            plan_view = gr.Code(label="Research plan", language="json")

            gr.Examples(
                examples=[
                    ["NVDA"],
                    ["MSFT"],
                    ["AI infrastructure demand outlook 2026"],
                    ["Open-source coding agents competitive landscape"],
                ],
                inputs=prompt,
            )

        run_button.click(fn=generate_report, inputs=prompt, outputs=[report, plan_view])
        prompt.submit(fn=generate_report, inputs=prompt, outputs=[report, plan_view])
        clear_button.click(fn=lambda: ("", "", "{}"), outputs=[prompt, report, plan_view])

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
