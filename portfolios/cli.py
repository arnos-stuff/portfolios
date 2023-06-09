import typer
import rich
import toml

from pathlib import Path
from itertools import cycle
from rich.table import Table
from rich.markdown import Markdown
from datetime import datetime as dt

from .markowitz import experiment
from .progression import console
from .utils import flatten, toMatrix, pkgdir, rootdir, store_markowitz, load_markowitz

app = typer.Typer(
    name="ptfio",
    help="A CLI for portfolio optimization experiments.",
    add_completion=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
    no_args_is_help=True,
    )


@app.command("markowitz")
def markowitz(
    gamma_lower: float = typer.Option(-4, '-gl', '--gamma-lower', help="Lower bound for gamma parameter on a [bold yellow]logarithmic scale[/bold yellow]."),
    gamma_upper: float = typer.Option(4, '-gu', '--gamma-upper', help="Upper bound for gamma parameter on a [bold yellow]logarithmic scale[/bold yellow]."),
    gamma_samples: int = typer.Option(100, '-N', '--num-samples', help="Number of samples [bold red]N[/bold red] for gamma parameter on a [bold yellow]linear scale[/bold yellow]."),
    save: bool = typer.Option(False, help="Save the results to a CSV file."),
    outdir: str = typer.Option(pkgdir / "data", help="Directory to save the results to."),
    synth: bool = typer.Option(True, help="Use synthetic data."),
    file: Path = typer.Option(None, help="Path to a CSV file containing the data if not using synthetic data."),
    ):
    """Run experiments using Markowitz's portfolio optimization model.

    Args:
        gamma_lower (float, optional): Lower bound for the gamma value (log axis). Defaults to typer.Option(-4, help="Lower bound for gamma parameter on a [bold yellow]logarithmic scale[/bold yellow].").
        gamma_upper (float, optional): Upper bound for the gamma value. Defaults to typer.Option(4, help="Upper bound for gamma parameter on a [bold yellow]logarithmic scale[/bold yellow].").
        gamma_samples (int, optional): Number of gamma values to solve the QCQP for. Defaults to typer.Option(100, help="Number of samples [bold red]N[/bold red] for gamma parameter on a [bold yellow]linear scale[/bold yellow].").
    """
    data = experiment(gamma_lower, gamma_upper, gamma_samples)
    if save:
        data["date"] = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
        data["name"] = f"markowitz@N={gamma_samples}@gl={str(gamma_lower).replace('-', 'neg')}@gu={str(gamma_upper).replace('-', 'neg')}"
        store_markowitz(data, outdir)
    else:
        console.print("[dim green]Tip: use --save if you want to save the results to a .csv file[/dim green]")
    
@app.command("explain")
def explain():  # sourcery skip: avoid-builtin-shadow
    """Print the explanations contained in `explanations.toml` about the project.
    For more information, DM me on Twitter: @arno_shae
    """
    explanations = toml.load(rootdir / "explanations.toml")
    table = Table(show_header=True, header_style="bold magenta", show_lines=True, box=rich.box.ROUNDED)
    matexpl = toMatrix(explanations)
    
    colors = cycle(["bold red", "bold green", "bold blue", "bold yellow", "bold magenta", "bold cyan", "bold white"])
    columns = ["Section", "Name", "Value"]
    
    columns += [f"Explanation {i}" for i in range(len(matexpl[0]) - 3)]
    
    
    callable = lambda x: Markdown(str(x))
    
    for col in columns:
        table.add_column(col, justify="center", style=next(colors))
    for row in matexpl:
        table.add_row(*list(map(callable, row)))
        
    console.print(table)
    
    console.print("[dim]Note: The explanations are stored in [bold]explanations.toml[/bold].[/dim]")
    
