#!/usr/bin/env python3
from __future__ import annotations

import argparse
import curses
import subprocess
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Formula:
    name: str


@dataclass(frozen=True)
class Cask:
    name: str


@dataclass(frozen=True)
class MasApp:
    app_id: str
    name: str


BREW_FORMULAE = [
    Formula("mas"),
]

MAS_APPS = [
    MasApp("1437681957", "Audiobook Builder"),
    MasApp("417375580", "BetterSnapTool"),
    MasApp("595191960", "CopyClip"),
    MasApp("524373870", "Due"),
    MasApp("1615988943", "Folder Peek"),
    MasApp("412448059", "ForkLift"),
    MasApp("1103915944", "Greenshot"),
    MasApp("789656124", "Image Vectorizer"),
    MasApp("409201541", "Pages"),
    MasApp("409203825", "Numbers"),
    MasApp("409183694", "Keynote"),
    MasApp("585396074", "MKV2MP4"),
    MasApp("463362050", "PhotoSweeper"),
    MasApp("1444636541", "Photomator"),
    MasApp("1289583905", "Pixelmator Pro"),
    MasApp("497799835", "Xcode"),
    MasApp("545519333", "Prime Video"),
    MasApp("764936294", "Purple Tree"),
    MasApp("6444322545", "SingleFile"),
    MasApp("1153157709", "Speedtest"),
    MasApp("1319778037", "iStat Menus"),
]

BREW_CASKS = [
    Cask("4k-video-downloader-plus"),
    Cask("bambu-studio"),
    Cask("bartender"),
    Cask("bettertouchtool"),
    Cask("ccleaner"),
    Cask("codex-app"),
    Cask("comfyui"),
    Cask("github"),
    Cask("docker"),
    Cask("firefox"),
    Cask("google-chrome"),
    Cask("discord"),
    Cask("visual-studio-code"),
    Cask("cursor"),
    Cask("claude"),
    Cask("chatgpt"),
    Cask("windsurf"),
    Cask("telegram"),
    Cask("whatsapp"),
    Cask("spotify"),
    Cask("steam"),
    Cask("warp"),
    Cask("raycast"),
    Cask("iina"),
    Cask("handbrake"),
    Cask("inkscape"),
    Cask("gimp"),
    Cask("freecad"),
    Cask("openscad"),
    Cask("calibre"),
    Cask("hammerspoon"),
    Cask("hazel"),
    Cask("keyboard-maestro"),
    Cask("ollama"),
    Cask("lm-studio"),
    Cask("db-browser-for-sqlite"),
    Cask("filezilla"),
    Cask("omnidisksweeper"),
    Cask("parallels"),
    Cask("parallels-toolbox"),
    Cask("plex-media-server"),
    Cask("shottr"),
    Cask("touchosc"),
    Cask("touchosc-bridge"),
    Cask("speedtest"),
    Cask("snapmaker-orca"),
    Cask("utm"),
    Cask("virtualbox"),
    Cask("vmware-fusion"),
    Cask("superduper"),
    Cask("surfshark"),
    Cask("forklift"),
    Cask("syncovery"),
]

MANUAL_APPS = [
    "Affinity",
    "Antigravity",
    "Bartender 4",
    "Blackmagic Proxy Generator Lite",
    "Blink",
    "ChatGPT Atlas",
    "ChessClock",
    "Create",
    "EMA App",
    "Edge Gallery",
    "FileZilla 2",
    "Focus Friend",
    "Google Docs",
    "Google Drive",
    "Google Sheets",
    "Google Slides",
    "HM Hospitales",
    "Happy",
    "HueForge",
    "Leroy Merlin",
    "Mi DIGI",
    "MyDigi",
    "NEPViewer",
    "Nespresso",
    "Pencil",
    "Quironsalud",
    "RENPHO Health",
    "Robot Control",
    "SF Symbols beta",
    "SHIELD TV",
    "Smart Printer",
    "Snapmaker",
    "ThumbHost3mf",
    "Waye",
    "appTaxi",
    "iStat Menus Helper Installer",
    "lichess",
]


@dataclass
class Item:
    kind: str
    key: str
    label: str
    selected: bool = True


def build_items() -> list[Item]:
    items: list[Item] = []
    items.extend(Item("formula", formula.name, f"brew formula: {formula.name}") for formula in BREW_FORMULAE)
    items.extend(Item("mas", app.app_id, f"App Store: {app.name} ({app.app_id})") for app in MAS_APPS)
    items.extend(Item("cask", cask.name, f"brew cask: {cask.name}") for cask in BREW_CASKS)
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Best-effort macOS app bootstrap with an interactive checklist.")
    parser.add_argument("--all", action="store_true", help="Install all brew and App Store items without showing the TUI.")
    parser.add_argument("--dry-run", action="store_true", help="Print the commands that would run without executing them.")
    parser.add_argument("--list-manual", action="store_true", help="Print the manual-install app list and exit.")
    return parser.parse_args()


def ensure_brew() -> None:
    if subprocess.run(["command", "-v", "brew"], shell=True).returncode != 0:
        print("Homebrew is not installed.")
        print("Install it first from https://brew.sh/")
        raise SystemExit(1)


def draw_menu(stdscr: curses.window, items: list[Item], cursor: int, offset: int) -> None:
    stdscr.erase()
    rows, cols = stdscr.getmaxyx()
    header = "LeadLight app setup | arrows move | space toggles | a toggles all | enter installs | q quits"
    stdscr.addnstr(0, 0, header, cols - 1, curses.A_BOLD)
    visible_rows = rows - 4
    for idx in range(visible_rows):
        item_index = offset + idx
        if item_index >= len(items):
            break
        item = items[item_index]
        prefix = "[x]" if item.selected else "[ ]"
        line = f"{prefix} {item.label}"
        attr = curses.A_REVERSE if item_index == cursor else curses.A_NORMAL
        stdscr.addnstr(idx + 2, 0, line, cols - 1, attr)
    footer = f"{sum(1 for item in items if item.selected)}/{len(items)} selected"
    stdscr.addnstr(rows - 1, 0, footer, cols - 1, curses.A_DIM)
    stdscr.refresh()


def run_tui(items: list[Item]) -> list[Item] | None:
    def inner(stdscr: curses.window) -> list[Item] | None:
        curses.curs_set(0)
        cursor = 0
        offset = 0
        while True:
            rows, _ = stdscr.getmaxyx()
            visible_rows = max(1, rows - 4)
            if cursor < offset:
                offset = cursor
            if cursor >= offset + visible_rows:
                offset = cursor - visible_rows + 1
            draw_menu(stdscr, items, cursor, offset)
            key = stdscr.getch()
            if key in (ord("q"), 27):
                return None
            if key in (curses.KEY_UP, ord("k")) and cursor > 0:
                cursor -= 1
            elif key in (curses.KEY_DOWN, ord("j")) and cursor < len(items) - 1:
                cursor += 1
            elif key == ord(" "):
                items[cursor].selected = not items[cursor].selected
            elif key == ord("a"):
                target = not all(item.selected for item in items)
                for item in items:
                    item.selected = target
            elif key in (10, 13, curses.KEY_ENTER):
                return items

    return curses.wrapper(inner)


def run(cmd: list[str], dry_run: bool, label: str | None = None) -> None:
    if label:
        print(label)
    print(" ", " ".join(cmd))
    if not dry_run:
        subprocess.run(cmd, check=False)


def install_selected(items: list[Item], dry_run: bool) -> None:
    print("Updating Homebrew...")
    run(["brew", "update"], dry_run, label="Homebrew update")

    for item in items:
        if not item.selected:
            continue
        if item.kind == "formula":
            run(["brew", "install", item.key], dry_run, label=f"Formula: {item.key}")
        elif item.kind == "mas":
            run(["mas", "install", item.key], dry_run, label=f"App Store: {item.label}")
        elif item.kind == "cask":
            run(["brew", "install", "--cask", item.key], dry_run, label=f"Cask: {item.label}")

    print()
    print("Manual follow-up apps from the source machine:")
    for app in MANUAL_APPS:
        print(f"  - {app}")


def main() -> int:
    args = parse_args()
    if args.list_manual:
        for app in MANUAL_APPS:
            print(app)
        return 0

    ensure_brew()
    items = build_items()
    if args.all:
        chosen = items
    else:
        chosen = run_tui(items)
        if chosen is None:
            print("Cancelled.")
            return 1
    install_selected(chosen, args.dry_run)
    print()
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
