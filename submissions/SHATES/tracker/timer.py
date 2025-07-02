# tracker/timer.py - Time tracking commands
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from pathlib import Path
from datetime import datetime, timedelta
import plotext as plt

from .db import TrackerDB

TrackerApp = typer.Typer(help="File time tracking commands")
console = Console()

@TrackerApp.command()
def start(file_path: str):
    db = TrackerDB()
    active = db.get_active_session()
    if active:
        rprint(f"[red]Already tracking: {active['file_path']}[/red]")
        rprint("[yellow]Use 'track stop' to stop the current session first.[/yellow]")
        raise typer.Exit(1)
    resolved_path = str(Path(file_path).resolve())

    if db.start_session(resolved_path):
        rprint(f"[green]Started tracking: {resolved_path}[/green]")
        rprint(f"[dim]Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
    else:
        rprint("[red]Failed to start tracking session.[/red]")
        raise typer.Exit(1)

@TrackerApp.command()
def stop():
    db = TrackerDB()

    session = db.stop_session()
    if session:
        duration = timedelta(seconds=session['duration'])
        rprint(f"[green]Stopped tracking: {session['file_path']}[/green]")
        rprint(f"[dim]Duration: {duration}[/dim]")
    else:
        rprint("[yellow]No active tracking session found.[/yellow]")

@TrackerApp.command()
def status():
    db = TrackerDB()

    active = db.get_active_session()
    if active:
        current_duration = datetime.now() - active['start_time']
        rprint(Panel(
            f"[green]Currently tracking:[/green] {active['file_path']}\n"
            f"[dim]Started:[/dim] {active['start_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[dim]Duration:[/dim] {current_duration}",
            title="Active Session",
            border_style="green"
        ))
    else:
        rprint("[yellow]No active tracking session.[/yellow]")

@TrackerApp.command()
def report(
    limit: int = typer.Option(10, "--limit", "-l", help="Number of files to show"),
    chart: bool = typer.Option(False, "--chart", "-c", help="Show bar chart")
):
    db = TrackerDB()

    data = db.get_time_report()
    if not data:
        rprint("[yellow]No tracking data found.[/yellow]")
        return

    data = data[:limit]

    if chart:
        files = [Path(item['file_path']).name for item in data]
        hours = [item['total_duration'] / 3600 for item in data]

        plt.clf()
        plt.bar(files, hours)
        plt.title("Time Spent per File (Hours)")
        plt.plotsize(100, 20)
        plt.show()
    else:
        table = Table(title="Time Tracking Report", show_header=True, header_style="bold magenta")
        table.add_column("File", style="cyan")
        table.add_column("Total Time", justify="right", style="green")
        table.add_column("Sessions", justify="right", style="yellow")
        table.add_column("Avg/Session", justify="right", style="blue")

        for item in data:
            file_name = Path(item['file_path']).name
            total_seconds = item['total_duration']
            total_time = str(timedelta(seconds=total_seconds))
            sessions = item['session_count']
            avg_seconds = total_seconds / sessions if sessions > 0 else 0
            avg_time = str(timedelta(seconds=int(avg_seconds)))

            table.add_row(file_name, total_time, str(sessions), avg_time)

        console.print(table)