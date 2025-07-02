import typer
import sys
from typing import Optional, List
from pathlib import Path
import json
import csv
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
import plotext as plt

PlotterApp = typer.Typer(help="Data visualization commands")
console = Console()

def parse_data_string(data_str: str) -> dict:
    try:  
        data = {}
        pairs = data_str.split(',')
        for pair in pairs:
            if '=' not in pair:
                raise ValueError(f"Invalid format: {pair}")
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            try:
                value = float(value)
                if value.is_integer():
                    value = int(value)
            except ValueError:
                pass  
            data[key] = value
        return data
    except Exception as e:
        raise typer.BadParameter(f"Invalid data format: {e}")

def read_file_data(file_path: Path) -> dict:
    try:
        if file_path.suffix.lower() == '.json':
            with open(file_path, 'r') as f:
                return json.load(f)
        elif file_path.suffix.lower() == '.csv':
            data = {}
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    cols = list(row.keys())
                    if len(cols) >= 2:
                        key = row[cols[0]]
                        value = row[cols[1]]
                        try:
                            value = float(value)
                            if value.is_integer():
                                value = int(value)
                        except ValueError:
                            pass
                        data[key] = value
            return data
        else:
            raise ValueError("Unsupported file format. Use .json or .csv")
    except Exception as e:
        raise typer.BadParameter(f"Error reading file: {e}")

def read_piped_data() -> dict:
    try:
        if sys.stdin.isatty():
            return {}

        lines = sys.stdin.read().strip().split('\n')
        data = {}

        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                try:
                    value = float(value)
                    if value.is_integer():
                        value = int(value)
                except ValueError:
                    pass
                data[key] = value
            elif ',' in line or '\t' in line:
                parts = line.replace('\t', ',').split(',')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    try:
                        value = float(value)
                        if value.is_integer():
                            value = int(value)
                    except ValueError:
                        pass
                    data[key] = value

        return data
    except Exception as e:
        raise typer.BadParameter(f"Error reading piped data: {e}")

@PlotterApp.command()
def bar(
    data: Optional[str] = typer.Option(None, "--data", help="Data in key=value,key2=value2 format"),
    file: Optional[Path] = typer.Option(None, "--file", help="JSON or CSV file path"),
    title: str = typer.Option("Bar Chart", "--title", help="Chart title"),
    width: int = typer.Option(80, "--width", help="Chart width"),
    height: int = typer.Option(20, "--height", help="Chart height")
):
    
    chart_data = {}


    if data:
        chart_data = parse_data_string(data)
    elif file:
        chart_data = read_file_data(file)
    else:
        chart_data = read_piped_data()

    if not chart_data:
        rprint("[red]No data provided. Use --data, --file, or pipe data.[/red]")
        raise typer.Exit(1)


    plt.clf()
    plt.bar(list(chart_data.keys()), list(chart_data.values()))
    plt.title(title)
    plt.plotsize(width, height)
    plt.show()

@PlotterApp.command()
def line(
    data: Optional[str] = typer.Option(None, "--data", help="Data in key=value,key2=value2 format"),
    file: Optional[Path] = typer.Option(None, "--file", help="JSON or CSV file path"),
    title: str = typer.Option("Line Chart", "--title", help="Chart title"),
    width: int = typer.Option(80, "--width", help="Chart width"),
    height: int = typer.Option(20, "--height", help="Chart height")
):

    chart_data = {}


    if data:
        chart_data = parse_data_string(data)
    elif file:
        chart_data = read_file_data(file)
    else:
        chart_data = read_piped_data()

    if not chart_data:
        rprint("[red]No data provided. Use --data, --file, or pipe data.[/red]")
        raise typer.Exit(1)

    plt.clf()
    plt.plot(list(chart_data.keys()), list(chart_data.values()))
    plt.title(title)
    plt.plotsize(width, height)
    plt.show()

@PlotterApp.command()
def pie(
    data: Optional[str] = typer.Option(None, "--data", help="Data in key=value,key2=value2 format"),
    file: Optional[Path] = typer.Option(None, "--file", help="JSON or CSV file path"),
    title: str = typer.Option("Pie Chart", "--title", help="Chart title")
):

    chart_data = {}

    if data:
        chart_data = parse_data_string(data)
    elif file:
        chart_data = read_file_data(file)
    else:
        chart_data = read_piped_data()

    if not chart_data:
        rprint("[red]No data provided. Use --data, --file, or pipe data.[/red]")
        raise typer.Exit(1)

    total = sum(float(v) for v in chart_data.values())
    percentages = {k: (float(v) / total) * 100 for k, v in chart_data.items()}

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Category", style="cyan")
    table.add_column("Value", justify="right", style="green")
    table.add_column("Percentage", justify="right", style="yellow")
    table.add_column("Visual", style="blue")

    for category, value in chart_data.items():
        pct = percentages[category]
        bar_length = int(pct / 5)  # Scale to fit
        visual_bar = "█" * bar_length + "░" * (20 - bar_length)
        table.add_row(
            category,
            str(value),
            f"{pct:.1f}%",
            visual_bar
        )

    console.print(table)