#!/usr/bin/env python3
import time
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
from rich.rule import Rule
from rich.box import ROUNDED, DOUBLE, HEAVY
from rich.prompt import Prompt, Confirm
from rich import print as rprint

console = Console()

def clear_screen():
    console.clear()

def animated_title():
    title_text = """
██╗   ██╗██╗███████╗ ██████╗██╗     ██╗
██║   ██║██║██╔════╝██╔════╝██║     ██║
██║   ██║██║███████╗██║     ██║     ██║
╚██╗ ██╔╝██║╚════██║██║     ██║     ██║
 ╚████╔╝ ██║███████║╚██████╗███████╗██║
  ╚═══╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝
    """

    subtitle = Text("The Ultimate CLI Tool for Developers", style="bold cyan")
    subtitle.justify = "center"

    panel = Panel(
        Align.center(title_text + "\n" + str(subtitle)),
        title="🚀 Welcome to VisCLI",
        subtitle="Visualize • Track • Break",
        box=DOUBLE,
        border_style="bright_blue",
        padding=(1, 2)
    )

    console.print(panel)
    time.sleep(1)

def feature_overview():
    console.print("\n")

    # Create feature boxes
    features = [
        {
            "title": "📊 VISUALIZER",
            "desc": "Transform data into\nbeautiful terminal charts",
            "items": ["Bar Charts", "Line Plots", "Pie Charts", "Multi-format Input"],
            "color": "cyan"
        },
        {
            "title": "⏱️ TIME TRACKER", 
            "desc": "Monitor coding time\nwith precision",
            "items": ["Session Tracking", "SQLite Storage", "Rich Reports", "Visual Analytics"],
            "color": "green"
        },
        {
            "title": "🎌 BREAK MODE",
            "desc": "Stay updated with\nanime news",
            "items": ["Live RSS Feed", "Browser Links", "Quick Headlines", "Formatted Tables"],
            "color": "magenta"
        }
    ]

    panels = []
    for feature in features:
        items_text = "\n".join([f"• {item}" for item in feature["items"]])
        content = f"{feature['desc']}\n\n{items_text}"

        panel = Panel(
            content,
            title=feature["title"],
            border_style=feature["color"],
            box=ROUNDED,
            expand=True
        )
        panels.append(panel)

    console.print(Columns(panels, equal=True, expand=True))

def visualizer_demo():
    clear_screen()

    header = Panel(
        "📊 VISUALIZER MODULE - Turn Data Into Art",
        style="bold cyan",
        box=HEAVY
    )
    console.print(header)

    # Data source options
    console.print("\n[bold]🎯 Multiple Data Sources:[/bold]")

    data_sources = Table(show_header=True, header_style="bold magenta", box=ROUNDED)
    data_sources.add_column("Method", style="cyan", width=15)
    data_sources.add_column("Command Example", style="green")
    data_sources.add_column("Use Case", style="yellow")

    data_sources.add_row(
        "CLI Data",
        "viscli plot bar --data 'Python=45,JS=30,Go=25'",
        "Quick data visualization"
    )
    data_sources.add_row(
        "File Input", 
        "viscli plot line --file data.csv --title 'Growth'",
        "Large datasets from files"
    )
    data_sources.add_row(
        "Piped Input",
        "cat data.txt | viscli plot pie",
        "Unix pipeline integration"
    )

    console.print(data_sources)

    # Chart types
    console.print("\n[bold]📈 Chart Types Available:[/bold]")

    chart_examples = [
        {
            "type": "BAR CHART",
            "command": "viscli plot bar --data 'Frontend=40,Backend=35,DevOps=25'",
            "desc": "Perfect for comparing categories",
            "icon": "📊"
        },
        {
            "type": "LINE CHART", 
            "command": "viscli plot line --data 'Jan=100,Feb=120,Mar=140'",
            "desc": "Great for trends over time",
            "icon": "📈"
        },
        {
            "type": "PIE CHART",
            "command": "viscli plot pie --data 'Mobile=60,Desktop=40'",
            "desc": "Show proportions beautifully",
            "icon": "🥧"
        }
    ]

    for chart in chart_examples:
        code_panel = Panel(
            f"[bold green]$ {chart['command']}[/bold green]",
            title=f"{chart['icon']} {chart['type']}",
            subtitle=chart['desc'],
            border_style="bright_green",
            box=ROUNDED
        )
        console.print(code_panel)
        console.print()

def tracker_demo():
    clear_screen()

    header = Panel(
        "⏱️ TIME TRACKER MODULE - Master Your Productivity",
        style="bold green",
        box=HEAVY
    )
    console.print(header)
    console.print("\n[bold]🔄 Complete Workflow:[/bold]")

    workflow_tree = Tree("⏱️ Time Tracking Workflow", style="bold blue")

    start_branch = workflow_tree.add("🟢 Start Session", style="green")
    start_branch.add("viscli track start /path/to/project.py")
    start_branch.add("💾 Auto-saves to ~/.viscli/tracker.db")

    monitor_branch = workflow_tree.add("👀 Monitor Progress", style="yellow")
    monitor_branch.add("viscli track status")
    monitor_branch.add("⏰ Shows current duration & file")

    stop_branch = workflow_tree.add("🛑 Stop Session", style="red")
    stop_branch.add("viscli track stop")
    stop_branch.add("📊 Calculates & stores duration")

    report_branch = workflow_tree.add("📈 Generate Reports", style="magenta")
    report_branch.add("viscli track report --chart")
    report_branch.add("🎯 Visual analytics of your time")

    console.print(workflow_tree)
    console.print("\n[bold]⚡ Command Showcase:[/bold]")

    commands = [
        {
            "cmd": "viscli track start myproject.py",
            "desc": "Start tracking time on a file",
            "icon": "▶️"
        },
        {
            "cmd": "viscli track status", 
            "desc": "Check current session status",
            "icon": "ℹ️"
        },
        {
            "cmd": "viscli track stop",
            "desc": "Stop and save current session", 
            "icon": "⏹️"
        },
        {
            "cmd": "viscli track report --chart --limit 5",
            "desc": "Visual report of top 5 files",
            "icon": "📊"
        }
    ]

    for cmd in commands:
        syntax = Syntax(cmd["cmd"], "bash", theme="monokai", line_numbers=False)
        panel = Panel(
            syntax,
            title=f"{cmd['icon']} {cmd['desc']}",
            border_style="bright_green",
            box=ROUNDED
        )
        console.print(panel)

def break_mode_demo():
    clear_screen()

    header = Panel(
        "🎌 BREAK MODE - Your Anime News Companion",
        style="bold magenta", 
        box=HEAVY
    )
    console.print(header)

    console.print("\n[bold]📰 Live Anime News Features:[/bold]")

    features_table = Table(show_header=True, header_style="bold cyan", box=ROUNDED)
    features_table.add_column("Feature", style="yellow", width=20)
    features_table.add_column("Command", style="green")
    features_table.add_column("Description", style="blue")

    features_table.add_row(
        "📰 Latest Headlines",
        "viscli break news",
        "Fetches top 5 stories from Anime News Network"
    )
    features_table.add_row(
        "🔗 Open in Browser", 
        "viscli break news --open 2",
        "Opens selected news item in your browser"
    )
    features_table.add_row(
        "⚡ Quick Mode",
        "viscli break quick", 
        "Simplified headlines without formatting"
    )

    console.print(features_table)

    console.print("\n[bold]👀 Sample Output Preview:[/bold]")

    sample_news = Table(title="📺 Latest Anime News", show_header=True, header_style="bold magenta", box=ROUNDED)
    sample_news.add_column("#", style="dim", width=3)
    sample_news.add_column("Title", style="cyan")
    sample_news.add_column("Published", style="green", justify="right")

    sample_news.add_row("1", "New Studio Ghibli Film Announced", "2024-01-15 10:30")
    sample_news.add_row("2", "Attack on Titan Final Season Details", "2024-01-15 09:15")
    sample_news.add_row("3", "Demon Slayer Movie Box Office Record", "2024-01-14 16:45")
    sample_news.add_row("4", "One Piece Live Action Season 2 Update", "2024-01-14 14:20")
    sample_news.add_row("5", "Spirited Away Stage Play Premiere", "2024-01-14 11:30")

    console.print(sample_news)

    tip = Panel(
        "💡 [bold]Pro Tip:[/bold] Use --open <index> to quickly jump to any article!",
        style="dim",
        border_style="dim"
    )
    console.print(tip)

def installation_guide():
    clear_screen()

    header = Panel(
        "🚀 INSTALLATION & SETUP GUIDE",
        style="bold blue",
        box=HEAVY
    )
    console.print(header)

    console.print("\n[bold]📦 Step 1: Install Dependencies[/bold]")

    install_cmd = "pip install typer[all] rich plotext requests"
    syntax = Syntax(install_cmd, "bash", theme="monokai", line_numbers=False)
    panel = Panel(syntax, title="💻 Installation Command", border_style="green")
    console.print(panel)

    console.print("\n[bold]📁 Step 2: Project Structure[/bold]")

    structure = """viscli/
├── cli.py                 # Entry point
├── plotter.py            # Visualization module  
├── tracker/
│   ├── __init__.py
│   ├── db.py             # Database operations
│   └── timer.py          # Time tracking commands
├── breaktime/
│   ├── __init__.py
│   └── headlines.py      # Anime news module
└── requirements.txt      # Dependencies"""

    structure_panel = Panel(
        structure,
        title="🏗️ Directory Structure",
        border_style="cyan",
        box=ROUNDED
    )
    console.print(structure_panel)

    console.print("\n[bold]✅ Step 3: Verification[/bold]")

    verify_commands = [
        "python cli.py --help",
        "python cli.py plot bar --data 'Test=10,Demo=20'",
        "python cli.py break quick"
    ]

    for cmd in verify_commands:
        syntax = Syntax(cmd, "bash", theme="monokai", line_numbers=False)
        console.print(f"[dim]$[/dim] {syntax.code}")

def advanced_examples():
    """Show advanced usage examples"""
    clear_screen()

    header = Panel(
        "⚡ ADVANCED USAGE EXAMPLES",
        style="bold yellow",
        box=HEAVY
    )
    console.print(header)

    examples = [
        {
            "title": "🔄 Pipeline Integration",
            "desc": "Integrate VisCLI with Unix pipelines",
            "commands": [
                "ps aux | grep python | wc -l | xargs -I {} echo 'Processes={}' | viscli plot bar",
                "git log --oneline | wc -l | xargs -I {} echo 'Commits={}' | viscli plot bar"
            ]
        },
        {
            "title": "📊 Data Analysis Workflow", 
            "desc": "Complete data analysis pipeline",
            "commands": [
                "# Start tracking your analysis session",
                "viscli track start data_analysis.py",
                "",
                "# Visualize your data",
                "viscli plot line --file monthly_sales.csv --title 'Sales Trend'",
                "",
                "# Take a break and check news",
                "viscli break news --open 1",
                "",
                "# Stop tracking when done",
                "viscli track stop"
            ]
        },
        {
            "title": "🎯 Productivity Monitoring",
            "desc": "Monitor your daily coding productivity",
            "commands": [
                "# Morning: Start tracking main project",
                "viscli track start ./src/main.py",
                "",
                "# Switch to different file",
                "viscli track stop && viscli track start ./tests/test_main.py", 
                "",
                "# End of day: Generate productivity report",
                "viscli track report --chart --limit 10"
            ]
        }
    ]

    for example in examples:
        console.print(f"\n[bold]{example['title']}[/bold]")
        console.print(f"[dim]{example['desc']}[/dim]\n")

        for cmd in example['commands']:
            if cmd.startswith('#'):
                console.print(f"[dim]{cmd}[/dim]")
            elif cmd.strip() == "":
                console.print()
            else:
                syntax = Syntax(cmd, "bash", theme="monokai", line_numbers=False)
                console.print(f"[green]$[/green] {syntax.code}")

def interactive_menu():
    while True:
        clear_screen()

        menu_title = Panel(
            "🎮 INTERACTIVE VisCLI EXPLORER",
            style="bold cyan",
            box=DOUBLE
        )
        console.print(menu_title)

        menu_table = Table(show_header=False, box=ROUNDED, border_style="bright_blue")
        menu_table.add_column("Option", style="bold cyan", width=8)
        menu_table.add_column("Feature", style="bold white", width=25)
        menu_table.add_column("Description", style="dim")

        menu_table.add_row("1", "📊 Visualizer Demo", "Explore data visualization features")
        menu_table.add_row("2", "⏱️ Time Tracker Demo", "Learn about productivity tracking")
        menu_table.add_row("3", "🎌 Break Mode Demo", "Discover anime news features")
        menu_table.add_row("4", "🚀 Installation Guide", "Step-by-step setup instructions")
        menu_table.add_row("5", "⚡ Advanced Examples", "Power user tips and tricks")
        menu_table.add_row("6", "🎯 Feature Overview", "Quick feature summary")
        menu_table.add_row("q", "👋 Exit", "Quit the demo")

        console.print(menu_table)

        choice = Prompt.ask(
            "\n[bold]Choose an option",
            choices=["1", "2", "3", "4", "5", "6", "q"],
            default="q"
        )

        if choice == "1":
            visualizer_demo()
        elif choice == "2":
            tracker_demo()
        elif choice == "3":
            break_mode_demo()
        elif choice == "4":
            installation_guide()
        elif choice == "5":
            advanced_examples()
        elif choice == "6":
            feature_overview()
        elif choice == "q":
            break

        if choice != "q":
            console.print(f"\n[dim]Press Enter to return to menu...[/dim]", end="")
            input()

def loading_animation():
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Initializing VisCLI Demo...", total=100)

        steps = [
            "Loading modules...",
            "Preparing visualizations...", 
            "Setting up time tracker...",
            "Fetching anime news...",
            "Ready to explore!"
        ]

        for i, step in enumerate(steps):
            progress.update(task, description=step, completed=(i + 1) * 20)
            time.sleep(0.5)

def goodbye_message():
    clear_screen()

    goodbye_art = """
╔══════════════════════════════════════════════════════════════╗
║                    Thanks for exploring!                     ║
║                                                              ║
║  🚀 Ready to boost your productivity with VisCLI?           ║
║                                                              ║
║  📊 Visualize your data                                      ║
║  ⏱️ Track your time                                          ║
║  🎌 Take anime breaks                                        ║
║                                                              ║
║            Happy coding! 💻✨                                ║
╚══════════════════════════════════════════════════════════════╝
    """

    panel = Panel(
        Align.center(goodbye_art),
        style="bold green",
        box=DOUBLE,
        border_style="bright_green"
    )

    console.print(panel)

    # Final tips
    tips = Panel(
        "[bold]🎯 Quick Start Commands:[/bold]\n\n"
        "[green]pip install typer[all] rich plotext requests[/green]\n"
        "[cyan]python cli.py plot bar --data 'Python=45,JS=30'[/cyan]\n"
        "[yellow]python cli.py track start myfile.py[/yellow]\n"
        "[magenta]python cli.py break news[/magenta]",
        title="💡 Remember These",
        border_style="dim"
    )
    console.print(tips)

def main():
    try:
        loading_animation()
        animated_title()
        time.sleep(2)

        if Confirm.ask("\n[bold]Would you like to explore VisCLI features interactively?[/bold]"):
            interactive_menu()
        else:
            feature_overview()
            time.sleep(3)

        goodbye_message()

    except KeyboardInterrupt:
        console.print("\n\n[yellow]Demo interrupted. Thanks for checking out VisCLI![/yellow]")
    except Exception as e:
        console.print(f"\n[red]An error occurred: {e}[/red]")
        console.print("[dim]Please ensure you have 'rich' installed: pip install rich[/dim]")

if __name__ == "__main__":
    main()