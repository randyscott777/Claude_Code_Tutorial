"""Fetch live prices for holdings and display a rich portfolio table.

Usage:
    python stock_values.py
    python stock_values.py --history   (show last 10 snapshots)
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import yfinance as yf
from rich.console import Console
from rich.table import Table
from rich import box

DB_PATH = Path(__file__).parent / "portfolio.db"

SHARES = {
    "venture": 521.438,
    "ultra":   1275.517,
    "mainst":  1254.238,
    "global":  626.092,
}

TICKERS = {
    "venture": "JANVX",
    "ultra":   "TWCUX",
    "mainst":  "MSIGX",
    "global":  "OPPAX",
}


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS snapshots (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            fetched_at    TEXT NOT NULL,
            friendly_name TEXT NOT NULL,
            ticker        TEXT NOT NULL,
            shares        REAL NOT NULL,
            price         REAL NOT NULL,
            value         REAL NOT NULL
        )
        """
    )
    return conn


def fetch_prices() -> dict[str, float]:
    symbols = list(TICKERS.values())
    data = yf.Tickers(" ".join(symbols))
    prices = {}
    for name, symbol in TICKERS.items():
        try:
            hist = data.tickers[symbol].history(period="1d")
            if hist.empty:
                prices[name] = 0.0
            else:
                prices[name] = float(hist["Close"].iloc[-1])
        except Exception:
            prices[name] = 0.0
    return prices


def save_snapshot(fetched_at: str, prices: dict[str, float]) -> None:
    conn = get_conn()
    try:
        for name, price in prices.items():
            value = SHARES[name] * price
            conn.execute(
                "INSERT INTO snapshots (fetched_at, friendly_name, ticker, shares, price, value) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (fetched_at, name, TICKERS[name], SHARES[name], price, value),
            )
        conn.commit()
    finally:
        conn.close()


def show_history() -> None:
    conn = get_conn()
    try:
        rows = conn.execute(
            "SELECT fetched_at, friendly_name, ticker, shares, price, value "
            "FROM snapshots ORDER BY id DESC LIMIT 40"
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        print("No snapshots saved yet.")
        return

    console = Console()
    table = Table(title="Portfolio History (last 40 rows)", box=box.ROUNDED, show_lines=True)
    table.add_column("Fetched At",    style="dim")
    table.add_column("Holding",       style="cyan")
    table.add_column("Ticker",        style="yellow")
    table.add_column("Shares",        justify="right")
    table.add_column("Price",         justify="right", style="green")
    table.add_column("Value",         justify="right", style="bold green")

    for fetched_at, name, ticker, shares, price, value in rows:
        table.add_row(
            fetched_at,
            name,
            ticker,
            f"{shares:,.3f}",
            f"${price:,.2f}",
            f"${value:,.2f}",
        )
    console.print(table)


def show_current() -> None:
    console = Console()
    console.print("[bold cyan]Fetching prices…[/bold cyan]")

    prices = fetch_prices()
    fetched_at = datetime.now().isoformat(timespec="seconds")
    save_snapshot(fetched_at, prices)

    table = Table(
        title=f"Portfolio Value  —  {fetched_at[:10]}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Holding",  style="cyan",         min_width=10)
    table.add_column("Ticker",   style="yellow",       min_width=6)
    table.add_column("Shares",   justify="right",      min_width=10)
    table.add_column("Price",    justify="right",      style="green",      min_width=10)
    table.add_column("Value",    justify="right",      style="bold green", min_width=12)

    grand_total = 0.0
    for name, shares in SHARES.items():
        ticker = TICKERS[name]
        price = prices[name]
        value = shares * price
        grand_total += value

        price_str = f"${price:,.2f}" if price else "[red]No price found[/red]"
        value_str = f"${value:,.2f}" if price else "[red]—[/red]"

        table.add_row(name, ticker, f"{shares:,.3f}", price_str, value_str)

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]", "", "", "",
        f"[bold cyan]${grand_total:,.2f}[/bold cyan]",
    )

    console.print(table)
    console.print(
        "[dim]Note: mutual fund NAV updates once daily after market close (4 PM ET)[/dim]"
    )


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--history":
        show_history()
    else:
        show_current()


if __name__ == "__main__":
    main()
