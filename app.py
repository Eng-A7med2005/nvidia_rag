"""
Gradio UI Frontend.
Provides a web interface for uploading documents and chatting with the RAG system.

Run with:  python -m smart_contract_assistant.app
       or: python main.py ui
"""

import os
import gradio as gr

from smart_contract_assistant.config import (
    validate_api_key,
    GRADIO_PORT,
    API_HOST,
    API_PORT,
    logger,
)
from smart_contract_assistant.ingestion import ingest_documents, save_index, load_index
from smart_contract_assistant.rag_chain import build_rag_chain, query


# ── UI Callback Functions ──────────────────────────────────────────────────


def ui_ingest(files, state):
    """Handles file upload and ingestion from the UI."""
    if not files:
        return "⚠️ Please upload files first.", state

    try:
        file_paths = [f.name for f in files]
        vectorstore = ingest_documents(file_paths)

        if vectorstore is None:
            return "❌ Failed to ingest documents. Check the logs.", state

        save_index(vectorstore)
        state = vectorstore
        return (
            f"✅ Successfully ingested **{len(file_paths)}** files. "
            f"Index saved to disk."
        ), state

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        return f"❌ Error during ingestion: {e}", state


def ui_query(message, history, state):
    """Handles chat queries from the UI."""
    if state is None:
        # Try loading from disk
        state = load_index()

    if state is None:
        return "⚠️ Please upload and ingest documents first (Tab 1).", history

    try:
        chain = build_rag_chain(state)
        result = query(chain, message)
        return result["formatted"], history

    except Exception as e:
        logger.error(f"Query error: {e}")
        return f"❌ Error: {e}", history


# ── Gradio App ─────────────────────────────────────────────────────────────


def create_ui():
    """Creates the Gradio Blocks interface."""
    with gr.Blocks(theme=gr.themes.Soft(), title="Smart Contract Assistant") as demo:
        # Shared state (replaces global variable)
        vs_state = gr.State(None)

        gr.Markdown("# 📜 Smart Contract Assistant v2")
        gr.Markdown(
            "Modular RAG system with **Citations**, **LangServe API**, and **Evaluation**."
        )

        # ── Tab 1: Ingestion ───────────────────────────────────────────
        with gr.Tab("📥 1. Ingestion"):
            gr.Markdown("Upload your contract files (PDF, TXT, DOCX) to build the knowledge base.")
            file_input = gr.File(
                label="Upload Contracts",
                file_count="multiple",
                file_types=[".pdf", ".txt", ".docx"],
            )
            ingest_btn = gr.Button("🚀 Ingest & Save Index", variant="primary")
            ingest_status = gr.Textbox(label="Status", interactive=False)

            ingest_btn.click(
                fn=ui_ingest,
                inputs=[file_input, vs_state],
                outputs=[ingest_status, vs_state],
            )

        # ── Tab 2: Chat ────────────────────────────────────────────────
        with gr.Tab("💬 2. Chat"):
            gr.Markdown("Ask questions about your uploaded contracts.")
            chatbot = gr.Chatbot(label="Conversation", height=400)
            msg_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g. What is the termination clause?",
            )
            send_btn = gr.Button("Send", variant="primary")

            def chat_handler(message, chat_history, state):
                if not message.strip():
                    return "", chat_history, state
                bot_reply, _ = ui_query(message, chat_history, state)
                chat_history = chat_history + [[message, bot_reply]]
                return "", chat_history, state

            send_btn.click(
                fn=chat_handler,
                inputs=[msg_input, chatbot, vs_state],
                outputs=[msg_input, chatbot, vs_state],
            )
            msg_input.submit(
                fn=chat_handler,
                inputs=[msg_input, chatbot, vs_state],
                outputs=[msg_input, chatbot, vs_state],
            )

            gr.Examples(
                examples=[
                    "What is the termination clause?",
                    "Are there any penalties for breach of contract?",
                    "What are the payment terms?",
                    "Who are the parties involved?",
                ],
                inputs=msg_input,
            )

        # ── Tab 3: API Info ────────────────────────────────────────────
        with gr.Tab("🖥️ 3. API Server"):
            gr.Markdown(f"""
### LangServe Backend Microservice

To start the REST API server:

1. Open a terminal in the project directory
2. Run: `python main.py serve`
3. Access:
   - **API Docs:** [http://{API_HOST}:{API_PORT}/docs](http://{API_HOST}:{API_PORT}/docs)
   - **Playground:** [http://{API_HOST}:{API_PORT}/contract-assistant/playground](http://{API_HOST}:{API_PORT}/contract-assistant/playground)
""")

    return demo


def launch():
    """Launches the Gradio UI."""
    validate_api_key()
    demo = create_ui()
    logger.info(f"Launching Gradio UI on port {GRADIO_PORT}...")
    demo.launch(share=True, server_port=GRADIO_PORT)


if __name__ == "__main__":
    launch()
