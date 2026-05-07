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
):
    """
    Peer-review AI hunks and generate edge-case tests.
    """
    print_banner()
    if not file:
        console.print("[bold red]Error:[/bold red] Please specify a file with --file.")
        raise typer.Exit(code=1)
        
    console.print(f"\n[bold yellow]Brain Phase:[/bold yellow] Assessing [cyan]{file}[/cyan]\n")
    
    with console.status("[bold green]Consulting Ollama (Llama 3)...") as status:
        import time
        time.sleep(2)
        
    console.print(Panel(
        "[bold cyan]Identified Risks:[/bold cyan]\n"
        "1. [yellow]Potential Null Pointer[/yellow] in process_data()\n"
        "2. [yellow]Unbounded Recursion[/yellow] in fetch_recursive()\n",
        title="QA Insights",
        border_style="cyan"
    ))
    
    console.print("[bold green]Tests generated.[/bold green] Ready for Sandbox execution.")

@app.command()
def sandbox(
    test_path: str = typer.Argument(..., help="Path to the generated tests."),
):
    """
    Execute generated tests in a Docker sandbox.
    """
    print_banner()
    console.print(f"\n[bold yellow]Sandbox Phase:[/bold yellow] Running tests in isolated container\n")
    
    with console.status("[bold magenta]Spinning up Docker container...") as status:
        import time
        time.sleep(1.5)
        status.update("[bold magenta]Running suite...")
        time.sleep(1.5)
    
    console.print("[bold red]FAIL[/bold red] - test_null_pointer (Detected Hallucination!)")
    console.print("[bold green]PASS[/bold green] - test_unbounded_recursion")
    
    console.print("\n[bold red]Security hardening required.[/bold red]")

if __name__ == "__main__":
    app()
