# InstallNewComputer

Best-effort macOS app bootstrap for recreating the app set from the source machine.

## Entry Point

Run:

```bash
bash ./scripts/setup_macos_apps.sh
```

That wrapper is intentionally Bash-first:

- if Homebrew is missing, it tries to install Homebrew
- if `python3` is missing, it installs Homebrew Python
- then it launches the Python checklist UI

## Important Homebrew Constraint

Homebrew installation must be run by a normal macOS user who is an Administrator.

So:

- do not run the setup script with `sudo`
- if the current user is not an admin, the script now stops early with a clear message
- if the current user is an admin and Homebrew is missing, the script will prompt once with `sudo -v` before launching the non-interactive Homebrew installer

If Homebrew is already installed, the rest of the script can proceed normally.

## Interactive Usage

```bash
bash ./scripts/setup_macos_apps.sh
```

That form is intentional: after downloading and unzipping from GitHub, the shell script's execute bit may be missing.

Controls:

- `↑` / `↓` or `j` / `k` to move
- `space` to toggle the current app
- `a` to toggle all
- `enter` to install the selected set
- `q` to quit

The checklist starts with everything unchecked.

## Non-Interactive Usage

Install everything currently automatable:

```bash
python3 ./scripts/setup_macos_apps.py --all
```

Dry run:

```bash
python3 ./scripts/setup_macos_apps.py --all --dry-run
```

List manual follow-up apps:

```bash
python3 ./scripts/setup_macos_apps.py --list-manual
```

## Scope

The repo currently automates three groups:

- Homebrew formulae
- Homebrew casks
- Mac App Store apps via `mas`

Anything still outside those paths is printed as a manual follow-up list.

## Related File

More detailed notes live in [NEW_MACHINE_APPS_SETUP.md](./NEW_MACHINE_APPS_SETUP.md).
