
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from typing import List, Dict
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import webbrowser

BreakApp = typer.Typer(help="Anime news break mode")
console = Console()

RSS_URL = "https://www.animenewsnetwork.com/all/rss.xml"

def fetch_anime_news() -> List[Dict]:
    try:
        response = requests.get(RSS_URL, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = []


        for item in root.findall('.//item')[:5]:  
            title_elem = item.find('title')
            link_elem = item.find('link')
            pub_date_elem = item.find('pubDate')

            if title_elem is not None and link_elem is not None:
                title = title_elem.text or "No title"
                link = link_elem.text or ""
                pub_date = pub_date_elem.text if pub_date_elem is not None else "Unknown"

                try:
                    parsed_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
                    formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = pub_date

                items.append({
                    "title": title,
                    "link": link,
                    "pub_date": formatted_date
                })

        return items
    except requests.RequestException as e:
        rprint(f"[red]Error fetching news: {e}[/red]")
        return []
    except ET.ParseError as e:
        rprint(f"[red]Error parsing RSS: {e}[/red]")
        return []

@BreakApp.command()
def news(
    open_link: int = typer.Option(None, "--open", "-o", help="Open news item by index (1-5)")
):
    """Show latest anime news headlines."""
    rprint("[blue]Fetching latest anime news...[/blue]")

    headlines = fetch_anime_news()

    if not headlines:
        rprint("[red]Could not fetch anime news. Please check your internet connection.[/red]")
        raise typer.Exit(1)

    
    table = Table(title="📺 Latest Anime News", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="cyan")
    table.add_column("Published", style="green", justify="right")

    for i, item in enumerate(headlines, 1):
        table.add_row(
            str(i),
            item["title"],
            item["pub_date"]
        )

    console.print(table)

    
    if open_link:
        if 1 <= open_link <= len(headlines):
            url = headlines[open_link - 1]["link"]
            rprint(f"[blue]Opening: {headlines[open_link - 1]['title']}[/blue]")
            try:
                webbrowser.open(url)
            except Exception as e:
                rprint(f"[red]Could not open browser: {e}[/red]")
                rprint(f"[yellow]URL: {url}[/yellow]")
        else:
            rprint(f"[red]Invalid index. Use 1-{len(headlines)}[/red]")
    else:
        rprint("\n[dim]Use --open <index> to open a news item in your browser[/dim]")

@BreakApp.command()
def quick():
    """Quick break - just show headlines without formatting."""
    headlines = fetch_anime_news()

    if not headlines:
        rprint("[red]Could not fetch news.[/red]")
        return

    rprint("[bold blue]🎌 Quick Anime News Break:[/bold blue]\n")

    for i, item in enumerate(headlines, 1):
        rprint(f"[cyan]{i}.[/cyan] {item['title']}")
        rprint(f"   [dim]{item['pub_date']}[/dim]\n")