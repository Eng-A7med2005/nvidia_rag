"""
Smart Contract Assistant — CLI Entry Point.

Usage (from ANY directory):
    python main.py ingest --files contract1.pdf contract2.pdf
    python main.py serve
    python main.py ui
    python main.py evaluate
"""

import sys
import os
import argparse
from pathlib import Path

# ── Fix Python Path ────────────────────────────────────────────────────────
# Add the project root to sys.path so the package can be found
# regardless of which directory the script is run from.
_this_file = Path(__file__).resolve()
_project_root = _this_file.parent.parent if _this_file.parent.name == "smart_contract_assistant" else _this_file.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def cmd_ingest(args):
    """Ingest documents into the FAISS vector store."""
    from smart_contract_assistant.config import validate_api_key
    from smart_contract_assistant.ingestion import ingest_documents, save_index

    validate_api_key()

    if not args.files:
        print("❌ No files specified. Use: python main.py ingest --files file1.pdf file2.pdf")
        sys.exit(1)

    vectorstore = ingest_documents(args.files)
    if vectorstore is None:
        print("❌ Ingestion failed. No documents were loaded.")
        sys.exit(1)

    save_index(vectorstore)
    print("✅ Ingestion complete. FAISS index saved to disk.")


def cmd_serve(args):
    """Start the LangServe API server."""
    import uvicorn
    from smart_contract_assistant.config import API_HOST, API_PORT

    print(f"🚀 Starting API server at http://{API_HOST}:{API_PORT}")
    print(f"📄 API docs:   http://{API_HOST}:{API_PORT}/docs")
    print(f"🎮 Playground: http://{API_HOST}:{API_PORT}/contract-assistant/playground")

    uvicorn.run(
        "smart_contract_assistant.server:app",
        host=API_HOST,
        port=API_PORT,
        reload=False,
    )


def cmd_ui(args):
    """Launch the Gradio UI."""
    from smart_contract_assistant.app import launch
    launch()


def cmd_evaluate(args):
    """Run evaluation on the RAG chain."""
    from smart_contract_assistant.config import validate_api_key
    from smart_contract_assistant.ingestion import load_index
    from smart_contract_assistant.rag_chain import build_rag_chain
    from smart_contract_assistant.evaluation import run_evaluation

    validate_api_key()

    vectorstore = load_index()
    if vectorstore is None:
        print("❌ No FAISS index found. Run 'python main.py ingest' first.")
        sys.exit(1)

    chain = build_rag_chain(vectorstore)
    results = run_evaluation(chain)

    print(f"\n{'='*60}")
    print(f"📊 Evaluation Results: {results['passed']}/{results['total']} passed ({results['score']:.0%})")
    print(f"{'='*60}")

    for r in results["results"]:
        status = "✅" if r["passed"] else "❌"
        print(f"\n{status} Q: {r['question']}")
        print(f"   A: {r['answer'][:150]}...")


def main():
    parser = argparse.ArgumentParser(
        prog="Smart Contract Assistant",
        description="RAG-based Smart Contract Analysis System",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── ingest ─────────────────────────────────────────────────────────
    p_ingest = subparsers.add_parser("ingest", help="Ingest documents into FAISS")
    p_ingest.add_argument(
        "--files", nargs="+", required=True,
        help="File paths to ingest (PDF, TXT, DOCX)",
    )
    p_ingest.set_defaults(func=cmd_ingest)

    # ── serve ──────────────────────────────────────────────────────────
    p_serve = subparsers.add_parser("serve", help="Start the LangServe API server")
    p_serve.set_defaults(func=cmd_serve)

    # ── ui ─────────────────────────────────────────────────────────────
    p_ui = subparsers.add_parser("ui", help="Launch the Gradio UI")
    p_ui.set_defaults(func=cmd_ui)

    # ── evaluate ───────────────────────────────────────────────────────
    p_evaluate = subparsers.add_parser("evaluate", help="Run evaluation pipeline")
    p_evaluate.set_defaults(func=cmd_evaluate)

    # ── Parse & Execute ────────────────────────────────────────────────
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
