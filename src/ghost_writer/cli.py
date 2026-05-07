import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
import questionary
from ghost_writer.audit.git_client import GitClient
from ghost_writer.audit.analyzer import AIAnalyzer
import sys
import os

app = typer.Typer(
    name="Ghost-Writer",
    help="AI-generated code provenance tracking and risk assessment tool.",
    add_completion=False,
    no_args_is_help=False,
)

console = Console()

def get_dashboard_header():
    banner = Text("\n   GHOST-WRITER   ", style="bold white on magenta")
    banner.append(" 🛡️  AI SECURITY & PROVENANCE ", style="bold magenta on black")
    return Align.center(banner)

def print_banner():
    console.print(get_dashboard_header())
    console.print(Align.center(Text("v0.1.0 • System Ready • Local LLM Active\n", style="italic dim white")))

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Main entry point. Shows interactive menu if no command is provided.
    """
    if ctx.invoked_subcommand is None:
        print_banner()
        choice = questionary.select(
            "What would you like to do?",
            choices=[
                "🔍 Run Git Audit (Detect AI Code)",
                "🧠 Stress-Test File (Risk Assessment)",
                "🛡️  Run Sandbox (Verify Risks)",
                "🚀 Full Pipeline Scan",
                "❌ Exit"
            ],
            style=questionary.Style([
                ('qmark', 'fg:#FF00FF bold'),
                ('question', 'bold'),
                ('answer', 'fg:#00FFFF bold'),
                ('pointer', 'fg:#00FFFF bold'),
                ('highlighted', 'fg:#00FFFF bold'),
                ('selected', 'fg:#00FFFF'),
            ])
        ).ask()

        if choice == "🔍 Run Git Audit (Detect AI Code)":
            audit()
        elif choice == "🧠 Stress-Test File (Risk Assessment)":
            stress_test()
        elif choice == "🛡️  Run Sandbox (Verify Risks)":
            sandbox_interactive()
        elif choice == "🚀 Full Pipeline Scan":
            full_scan()
        else:
            sys.exit(0)

@app.command()
def audit(
    path: str = typer.Option(".", help="Path to the repository to audit."),
    limit: int = typer.Option(50, "--limit", "-l", help="Number of recent commits to analyze."),
):
    """
    Scan git history to detect AI-generated code.
    """
    print_banner()
    
    if not os.path.exists(path):
        console.print(f"[bold red]Error:[/bold red] Path [cyan]{path}[/cyan] does not exist.")
        return

    console.print(Panel(f"Starting Git Audit on: [bold cyan]{path}[/bold cyan]", border_style="magenta"))
    
    try:
        client = GitClient(path)
        analyzer = AIAnalyzer()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return

    commit_data = []
    with console.status("[bold magenta]Traversing Git History...") as status:
        commits = client.get_commits(limit=limit)
        for i, commit in enumerate(commits):
            status.update(f"[bold magenta]Analyzing {i+1}/{len(commits)}: {commit.hexsha[:7]}")
            metadata = client.get_commit_metadata(commit)
            diffs = client.get_commit_diffs(commit)
            score = analyzer.analyze_commit(metadata, diffs)
            commit_data.append({"score": score, "diffs": diffs})
            
    heatmap = analyzer.generate_heatmap(commit_data)
    
    table = Table(
        title="[bold magenta]AI DETECTION HEATMAP[/bold magenta]", 
        border_style="magenta",
        header_style="bold magenta",
        box=None,
        expand=True
    )
    table.add_column("File Path", style="cyan")
    table.add_column("AI Confidence", justify="right")
    table.add_column("Security Status", justify="center")
    
    for file_path, score in sorted(heatmap.items(), key=lambda x: x[1], reverse=True):
        prob_str = f"{score*100:.1f}%"
        if score > 0.7:
            status_str = "[bold red]CRITICAL[/bold red]"
        elif score > 0.4:
            status_str = "[bold yellow]WARNING[/bold yellow]"
        else:
            status_str = "[bold green]SAFE[/bold green]"
        table.add_row(file_path, prob_str, status_str)
    
    console.print(Panel(table, border_style="magenta", padding=(1, 2)))
    console.print("\n[dim]Audit complete. Recommended: Stress-test files with >70% confidence.[/dim]")

@app.command()
def stress_test(
    file: str = typer.Option(None, "--file", "-f", help="Specific file to stress test."),
    model: str = typer.Option("llama3", "--model", "-m", help="Ollama model to use."),
):
    """
    Peer-review AI hunks and generate edge-case tests.
    """
    from ghost_writer.brain.langchain_client import BrainClient
    
    if not file:
        file = questionary.text("Enter the path to the file you want to stress-test:").ask()
        if not file or not os.path.exists(file):
            console.print("[bold red]Invalid file path.[/bold red]")
            return

    print_banner()
    console.print(Panel(f"Brain Phase: Assessing [bold cyan]{file}[/bold cyan]", border_style="cyan"))
    
    try:
        with open(file, "r", encoding="utf-8") as f:
            code_content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file:[/bold red] {str(e)}")
        return

    brain = BrainClient(model=model)
    with console.status(f"[bold cyan]Local LLM ({model}) is thinking...") as status:
        analysis = brain.analyze_code(code_content, file)
        
    console.print(Panel(
        analysis,
        title="[bold cyan]QA ENGINEER INSIGHTS[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Save tests
    os.makedirs("tests", exist_ok=True)
    test_file = f"tests/stress_{os.path.basename(file)}"
    try:
        test_code = analysis
        if "```python" in analysis:
            test_code = analysis.split("```python")[1].split("```")[0]
        
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(test_code)
        console.print(f"\n[bold green]Success:[/bold green] Stress tests saved to [cyan]{test_file}[/cyan]")
    except Exception as e:
        console.print(f"[bold red]Warning:[/bold red] Could not save tests: {str(e)}")

def sandbox_interactive():
    code_path = questionary.text("Path to the original code file:").ask()
    test_path = questionary.text("Path to the stress-test file:").ask()
    if code_path and test_path:
        sandbox(code_path, test_path)

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
    console.print(Panel(f"Sandbox Phase: Running [cyan]{test_path}[/cyan]", border_style="blue"))
    
    try:
        manager = DockerManager()
        with console.status("[bold blue]Spinning up Docker environment...") as status:
            result = manager.run_test(code_path, test_path)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        return
    
    if result["success"]:
        console.print(Panel("[bold green]PASS[/bold green]\nAll stress tests passed. AI code appears robust.", border_style="green"))
    else:
        console.print(Panel(f"[bold red]FAIL[/bold red]\nVulnerabilities detected or test error.\n\n[dim]{result['logs']}[/dim]", border_style="red"))

@app.command()
def full_scan(
    path: str = typer.Argument(".", help="Path to the repository to audit."),
):
    """
    Run the complete Ghost-Writer pipeline.
    """
    audit(path=path)

if __name__ == "__main__":
    app()
