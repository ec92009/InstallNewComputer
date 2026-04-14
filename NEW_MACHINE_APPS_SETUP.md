# New Machine App Setup

This repo now includes a best-effort app bootstrap script based on the current
`/Applications` inventory from the source machine.

Scripts:

```bash
./scripts/setup_macos_apps.sh
```

```bash
python3 ./scripts/setup_macos_apps.py
```

Bootstrap behavior:

- `./scripts/setup_macos_apps.sh` is the preferred entrypoint
- it is Bash-only at startup
- if Homebrew is missing, it installs Homebrew first
- if `python3` is missing, it installs Homebrew Python
- then it launches the Python TUI
- if Homebrew is missing and the current macOS user is not an Administrator, it now stops early with a clear message instead of falling into the Homebrew installer failure loop

What it does:

- shows a basic terminal checklist where you can move with arrow keys and check/uncheck apps with space
- starts with every app unchecked so the default posture is selective, not everything-at-once
- installs a conservative Homebrew subset of the apps found in `/Applications`
- installs `mas` and uses recovered Mac App Store IDs where available
- installs a larger verified Homebrew cask subset for apps we confirmed are available in the current cask index
- prints a manual follow-up checklist for apps that are App Store, license-gated,
  custom/internal, or otherwise not reliable to automate through Homebrew alone

Interactive controls:

- `↑` / `↓` or `j` / `k` to move
- `space` to toggle the current app
- `a` to toggle all
- `enter` to install the selected set
- `q` to quit

Non-interactive mode:

```bash
python3 ./scripts/setup_macos_apps.py --all
```

Current `mas` app IDs wired in:

- `1437681957` — Audiobook Builder
- `417375580` — BetterSnapTool
- `595191960` — CopyClip
- `524373870` — Due
- `1615988943` — Folder Peek
- `412448059` — ForkLift
- `1103915944` — Greenshot
- `789656124` — Image Vectorizer
- `409201541` — Pages
- `409203825` — Numbers
- `409183694` — Keynote
- `585396074` — MKV2MP4
- `463362050` — PhotoSweeper
- `1444636541` — Photomator
- `1289583905` — Pixelmator Pro
- `497799835` — Xcode
- `545519333` — Prime Video
- `764936294` — Purple Tree
- `6444322545` — SingleFile
- `1153157709` — Speedtest
- `1319778037` — iStat Menus

Requirement:

- `mas install ...` only works when the machine is signed into the Mac App Store.
- I also checked `~/Applications`; no additional App Store IDs surfaced there beyond the `/Applications` set.
- the shell wrapper assumes the machine can reach Homebrew and GitHub in order to install Homebrew itself on a brand-new Mac

Notes:

- the script uses `|| true` for each install so one bad cask does not stop the rest
- it is intentionally conservative rather than pretending every app can be recovered perfectly through brew
- the brew automation scope was expanded to include additional confirmed casks such as `bambu-studio`, `bartender`, `bettertouchtool`, `codex-app`, `comfyui`, `hazel`, `keyboard-maestro`, `omnidisksweeper`, `parallels`, `parallels-toolbox`, `plex-media-server`, `snapmaker-orca`, `superduper`, `syncovery`, and `touchosc-bridge`
- if you want stricter behavior later, the next step is to split the list into:
  - verified brew casks
  - probable brew casks to test
  - App Store installs with `mas` IDs
  - fully manual installs
