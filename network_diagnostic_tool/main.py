from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print
try:
    from .diagnostics import check_internet_connection, get_ip_info, run_speed_test, ping_host
except ImportError:
    from diagnostics import check_internet_connection, get_ip_info, run_speed_test, ping_host

console = Console()

def display_header():
    console.print(Panel.fit("[bold cyan]Network Diagnostic Tool[/bold cyan]\n[yellow]Windows | Linux | Android[/yellow]", border_style="cyan"))

def run_full_diagnostic():
    console.print("\n[bold]Running Full Diagnostic...[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:

        # Internet Check
        task1 = progress.add_task(description="Checking Internet Connection...", total=None)
        connected = check_internet_connection()
        progress.remove_task(task1)
        if connected:
            console.print("[green]✔ Internet Connection: Active[/green]")
        else:
            console.print("[red]✖ Internet Connection: Inactive[/red]")
            return # Stop if no internet

        # IP Info
        task2 = progress.add_task(description="Fetching IP Information...", total=None)
        ip_info = get_ip_info()
        progress.remove_task(task2)

        table = Table(title="IP Information")
        table.add_column("Type", style="cyan")
        table.add_column("Address", style="magenta")
        table.add_row("Local IP", ip_info['local_ip'])
        table.add_row("Public IP", ip_info['public_ip'])
        console.print(table)

        # Speed Test
        console.print("\n[bold]Running Speed Test (this may take a minute)...[/bold]")
        task3 = progress.add_task(description="Measuring Speed...", total=None)
        speed_results = run_speed_test()
        progress.remove_task(task3)

        if speed_results.get("success"):
            table = Table(title="Speed Test Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Server", speed_results['server'])
            table.add_row("Ping", f"{speed_results['ping']} ms")
            table.add_row("Download", f"{speed_results['download']} Mbps")
            table.add_row("Upload", f"{speed_results['upload']} Mbps")
            console.print(table)
        else:
            console.print(f"[red]Speed Test Failed: {speed_results.get('error')}[/red]")

def run_quick_check():
    console.print("\n[bold]Running Quick Connectivity Check...[/bold]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Checking connectivity...", total=None)
        connected = check_internet_connection()
        ip_info = get_ip_info()
        progress.remove_task(task)

    if connected:
        console.print("[green]✔ Internet: Connected[/green]")
    else:
        console.print("[red]✖ Internet: Disconnected[/red]")

    table = Table(title="IP Info")
    table.add_column("Type", style="cyan")
    table.add_column("Address", style="magenta")
    table.add_row("Local IP", ip_info['local_ip'])
    table.add_row("Public IP", ip_info['public_ip'])
    console.print(table)

def run_speed_test_only():
    console.print("\n[bold]Running Speed Test...[/bold]")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Testing speed...", total=None)
        results = run_speed_test()
        progress.remove_task(task)

    if results.get("success"):
        table = Table(title="Speed Test Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Server", results['server'])
        table.add_row("Ping", f"{results['ping']} ms")
        table.add_row("Download", f"{results['download']} Mbps")
        table.add_row("Upload", f"{results['upload']} Mbps")
        console.print(table)
    else:
        console.print(f"[red]Speed Test Failed: {results.get('error')}[/red]")

def ping_specific_host():
    host = console.input("[bold yellow]Enter host to ping (e.g., google.com): [/bold yellow]")
    console.print(f"Pinging {host}...")
    latency = ping_host(host)
    if latency is not None:
        console.print(f"[green]✔ Reply from {host}: time={latency}ms[/green]")
    else:
        console.print(f"[red]✖ No reply from {host}[/red]")

def main():
    while True:
        display_header()
        console.print("\n[1] Full Diagnostic")
        console.print("[2] Quick Connectivity Check")
        console.print("[3] Speed Test Only")
        console.print("[4] Ping Specific Host")
        console.print("[5] Exit")

        choice = console.input("\n[bold cyan]Select an option: [/bold cyan]")

        if choice == '1':
            run_full_diagnostic()
        elif choice == '2':
            run_quick_check()
        elif choice == '3':
            run_speed_test_only()
        elif choice == '4':
            ping_specific_host()
        elif choice == '5':
            console.print("[bold green]Goodbye![/bold green]")
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

        console.input("\nPress Enter to continue...")
        console.clear()

if __name__ == "__main__":
    main()
