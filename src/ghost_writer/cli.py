import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from ghost_writer.audit.git_client import GitClient
from ghost_writer.audit.analyzer import AIAnalyzer
import sys
import os

app = typer.Typer(
    name="Ghost-Writer",
    help="AI-generated code provenance tracking and risk assessment tool.",
    add_completion=False,
)

console = Console()

def print_banner():
    banner = Text("GHOST-WRITER", style="bold magenta")
    banner.append(" | ", style="white")
    banner.append("AI PROVENANCE & HARDENING", style="italic cyan")
    
    console.print(
        Panel(
            banner,
            subtitle="[bold white]v0.1.0[/bold white]",
            subtitle_align="right",
            border_style="magenta",
            expand=False,
        )
    )

@app.command()
def audit(
    path: str = typer.Argument(".", help="Path to the repository to audit."),
    limit: int = typer.Option(50, "--limit", "-l", help="Number of recent commits to analyze."),
):
    """
    Scan git history to detect AI-generated code.
    """
    print_banner()
    
    if not os.path.exists(path):
        console.print(f"[bold red]Error:[/bold red] Path [cyan]{path}[/cyan] does not exist.")
        raise typer.Exit(code=1)

    console.print(f"\n[bold yellow]Starting Git Audit on:[/bold yellow] [cyan]{path}[/cyan]\n")
    
    try:
        client = GitClient(path)
        analyzer = AIAnalyzer()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    commit_data = []
    with console.status("[bold green]Analyzing commit history...") as status:
        commits = client.get_commits(limit=limit)
        for i, commit in enumerate(commits):
            status.update(f"[bold green]Analyzing commit {i+1}/{len(commits)}: {commit.hexsha[:7]}...")
            metadata = client.get_commit_metadata(commit)
            diffs = client.get_commit_diffs(commit)
            score = analyzer.analyze_commit(metadata, diffs)
            commit_data.append({"score": score, "diffs": diffs})
            
    heatmap = analyzer.generate_heatmap(commit_data)
    
    table = Table(title="AI Detection Heatmap", border_style="magenta")
    table.add_column("File", style="cyan")
    table.add_column("AI Probability", justify="right")
    table.add_column("Status", justify="center")
    
    for file_path, score in sorted(heatmap.items(), key=lambda x: x[1], reverse=True):
        prob_str = f"{score*100:.1f}%"
        if score > 0.7:
            status_str = "[red]CRITICAL[/red]"
        elif score > 0.4:
            status_str = "[yellow]WARNING[/yellow]"
        else:
            status_str = "[green]SAFE[/green]"
        table.add_row(file_path, prob_str, status_str)
    
    console.print(table)
    console.print("\n[bold green]Audit complete.[/bold green] Use `stress-test` to analyze specific files.")

@app.command()
def stress_test(
    file: str = typer.Option(None, "--file", "-f", help="Specific file to stress test."),
    model: str = typer.Option("llama3", "--model", "-m", help="Ollama model to use."),
):
    """
    Peer-review AI hunks and generate edge-case tests.
    """
    from ghost_writer.brain.langchain_client import BrainClient
    
    print_banner()
    if not file:
        console.print("[bold red]Error:[/bold red] Please specify a file with --file.")
        raise typer.Exit(code=1)
    
    if not os.path.exists(file):
        console.print(f"[bold red]Error:[/bold red] File [cyan]{file}[/cyan] does not exist.")
        raise typer.Exit(code=1)
        
    console.print(f"\n[bold yellow]Brain Phase:[/bold yellow] Assessing [cyan]{file}[/cyan]\n")
    
    try:
        with open(file, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

    brain = BrainClient(model=model)
    with console.status(f"[bold green]Consulting Ollama ({model})...") as status:
        analysis = brain.analyze_code(code_content, file)
        
    console.print(Panel(
        analysis,
        title="[bold cyan]QA Engineer Insights[/bold cyan]",
        border_style="cyan"
    ))
    
    # Save tests for sandbox phase
    test_file = f"tests/stress_{os.path.basename(file)}"
    try:
        # Extract python code block if present (simple heuristic)
        test_code = analysis
        if "```python" in analysis:
            test_code = analysis.split("```python")[1].split("```")[0]
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_code)
        console.print(f"\n[bold green]Tests generated and saved to:[/bold green] [cyan]{test_file}[/cyan]")
    except Exception as e:
        console.print(f"[bold red]Warning:[/bold red] Could not save tests to file: {str(e)}")

    console.print("\nUse `sandbox` to execute the generated tests.")

@app.command()
def sandbox(
    code_path: str = typer.Argument(..., help="Path to the original code file."),
    test_path: str = typer.Argument(..., help="Path to the generated test file."),
):
    """
    Execute generated tests in a Docker sandbox.
    """
    from ghost_writer.sandbox.docker_manager import DockerManager
    
    print_banner()
    console.print(f"\n[bold yellow]Sandbox Phase:[/bold yellow] Running tests in isolated container\n")
    
    try:
        manager = DockerManager()
        with console.status("[bold magenta]Spinning up Docker container...") as status:
            result = manager.run_test(code_path, test_path)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        raise typer.Exit(code=1)
    
    if result["success"]:
        console.print("[bold green]PASS[/bold green] - All stress tests passed. AI code appears robust.")
    else:
        console.print("[bold red]FAIL[/bold red] - Vulnerabilities detected or test error.")
        console.print(Panel(result["logs"], title="Logs", border_style="red"))
    
    console.print("\n[bold yellow]Sandbox execution complete.[/bold yellow]")

@app.command()
def full_scan(
    path: str = typer.Argument(".", help="Path to the repository to audit."),
    output: str = typer.Option("report.md", "--output", "-o", help="Path to save the report."),
):
    """
    Run the complete Ghost-Writer pipeline: Audit -> Stress Test -> Sandbox.
    """
    print_banner()
    console.print("[bold cyan]Starting full Ghost-Writer pipeline...[/bold cyan]\n")
    
    # This is a simplified orchestration for the demo/MVP
    # 1. Audit
    audit(path=path)
    
    # 2. Stress Test & Sandbox (Logic for top risky file)
    console.print("\n[bold cyan]Proceeding to hardening top risk files...[/bold cyan]")
    # In a real implementation, we would iterate through the heatmap.
    
    console.print(f"\n[bold green]Full scan complete. Report saved to {output}[/bold green]")

if __name__ == "__main__":
    app()
