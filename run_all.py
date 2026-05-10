import argparse
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
STREAMLIT_APP = PROJECT_ROOT / "src" / "streamlit_app.py"
REQUIRED_MODELS = ("llama3.2", "nomic-embed-text")


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True)


def check_ollama_available() -> tuple[bool, str]:
    if shutil.which("ollama") is None:
        return False, "Ollama CLI was not found on PATH. Install Ollama before starting NewsNexus."

    probe = run_command(["ollama", "list"])
    if probe.returncode != 0:
        stderr = probe.stderr.strip() or probe.stdout.strip() or "Unable to reach Ollama."
        return False, f"Ollama is installed but not reachable: {stderr}"

    installed_models = probe.stdout.lower()
    missing = [model for model in REQUIRED_MODELS if model.lower() not in installed_models]
    if missing:
        missing_list = ", ".join(missing)
        return False, f"Missing Ollama models: {missing_list}. Run `ollama pull` for each missing model."

    return True, "Ollama is reachable and required models are installed."


def validate_prerequisites() -> int:
    if not STREAMLIT_APP.exists():
        print(f"[ERROR] Streamlit entry point not found: {STREAMLIT_APP}")
        return 1

    ok, message = check_ollama_available()
    if not ok:
        print(f"[ERROR] {message}")
        return 1

    print(f"[OK] {message}")
    print(f"[OK] Streamlit entry point found: {STREAMLIT_APP}")
    return 0


def build_streamlit_command(host: str, port: int, headless: bool) -> list[str]:
    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(STREAMLIT_APP),
        "--server.address",
        host,
        "--server.port",
        str(port),
        "--server.headless",
        "true" if headless else "false",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Start NewsNexus with prerequisite checks.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface for Streamlit.")
    parser.add_argument("--port", default=8501, type=int, help="Port for Streamlit.")
    parser.add_argument("--headless", action="store_true", help="Run Streamlit in headless mode.")
    parser.add_argument("--check-only", action="store_true", help="Validate prerequisites and exit.")
    args = parser.parse_args()

    prereq_status = validate_prerequisites()
    if prereq_status != 0:
        return prereq_status

    if args.check_only:
        return 0

    command = build_streamlit_command(args.host, args.port, args.headless)
    print(f"[INFO] Launching NewsNexus on http://{args.host}:{args.port}")
    print(f"[INFO] Using interpreter: {sys.executable}")

    launched = subprocess.run(command)
    return launched.returncode


if __name__ == "__main__":
    raise SystemExit(main())