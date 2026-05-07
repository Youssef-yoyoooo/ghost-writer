# Ghost-Writer

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.ai/)
[![Docker](https://img.shields.io/badge/Runtime-Docker-blue.svg)](https://www.docker.com/)

**Ghost-Writer** is a cutting-edge security and provenance auditing tool designed for the AI-assisted coding era. It tracks the lineage of your codebase, identifies AI-generated hunks, assesses them for logical vulnerabilities, and verifies them in a sandboxed environment.

---

## Features

- **Phase 1: Git Provenance Tracking**: 
  - Analyzes commit velocity and metadata to distinguish between human and AI intent.
  - Generates an interactive "Heatmap" of your repository's AI density.
- **Phase 2: ISTQB-Certified Risk Assessment**:
  - Leverages local LLMs (via Ollama) applying **Boundary Value Analysis (BVA)** and **Equivalence Partitioning (EP)**.
  - Automatically identifies "Deceptively Simple" bugs and AI hallucinations.
- **Phase 3: Auto-Hardening Engine**:
  - Batch-processes risky files based on user-defined confidence thresholds.
  - Executes ISTQB-standard tests in isolated Docker containers to verify code integrity.
- **Phase 4: Premium Reporting**:
  - Beautiful Warp-inspired terminal dashboard.
  - Exportable Markdown and HTML audit reports.

---

## Tech Stack

- **Logic**: Python 3.9+ (Click, Typer)
- **Aesthetics**: `rich` (Warp-like terminal UI)
- **Git Integration**: GitPython
- **LLM Orchestration**: LangChain + Ollama (Llama 3)
- **Containerization**: Docker SDK for Python

---

## Installation

### Prerequisites

1.  **Ollama**: Install from [ollama.ai](https://ollama.ai) and pull Llama 3:
    ```bash
    ollama pull llama3
    ```
2.  **Docker**: Ensure Docker Desktop is running.
3.  **Git**: Local git repository to audit.

### Setup

```bash
git clone https://github.com/Youssef-yoyoooo/ghost-writer.git
cd ghost-writer
pip install -e .
```

---

## Usage

Ghost-Writer features a **Warp-inspired interactive dashboard**. No need to memorize complex commands.

### The Dashboard
Simply run the helper script to enter the interactive menu:
```powershell
.\ghost.ps1
```

### Step-by-Step Pipeline:

1.  **Git Audit**: Select this to scan your history. Look for files marked as **CRITICAL**.
2.  **Stress-Test**: Pick a risky file. **Llama 3** will find logic flaws and generate Pytest cases.
3.  **Sandbox**: Execute those tests in an isolated **Docker container** to verify if the code breaks under pressure.
4.  **Full Scan**: Orchestrate the entire pipeline in one go.
```bash
ghost-writer full-scan --output report.md
```

---

## Architecture

```mermaid
graph TD
    A[Local Repo] --> B(Git Audit)
    B --> C{AI Detection}
    C -- Heatmap --> D[Reporter]
    C -- AI Hunks --> E(Brain / LangChain)
    E -- Unit Tests --> F(Sandbox / Docker)
    F -- Pass/Fail --> D
    D --> G[Final Audit Report]
```

---

## Contributing

Contributions are welcome! Please read the [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
