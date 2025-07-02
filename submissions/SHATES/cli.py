import typer
from rich.console import Console
from rich import print as rprint
import sys
from pathlib import Path
from plotter import PlotterApp
from tracker.timer import TrackerApp
from breaktime.headlines import BreakApp

app = typer.Typer(
    name="viscli",
    help="VisCLI - A versatile CLI tool for visualization, time tracking, and breaks",
    rich_markup_mode="rich"
)
console = Console()

app.add_typer(PlotterApp, name="plot", help="Data visualization tools")
app.add_typer(TrackerApp, name="track", help="File time tracking")
app.add_typer(BreakApp, name="break", help="Anime news break mode")

@app.command()
def version():
    """Show VisCLI version."""
    rprint("[bold blue]VisCLI[/bold blue] [dim]v1.0.0[/dim]")

if __name__ == "__main__":
    app()
