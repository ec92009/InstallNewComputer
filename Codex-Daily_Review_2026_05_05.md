# Codex Daily Review - 2026-05-05

## General Architecture
- The Bash wrapper is the right root: it handles "fresh Mac" constraints before Python is safe to assume.
- The Python script is still cohesive, but the app inventory now dominates the file; split data into a separate module if the list keeps growing.
- Bug: `--all` passes unselected items into `install_selected`, so it updates Homebrew but installs nothing.

## UI
- The curses checklist is austere in a good way for a bootstrap tool: no dependency tax, clear keyboard loop.
- Labels are readable, but the single long list will get tiring; grouping formulae, App Store, casks, and manual items would reduce scanning.

## UX
- Starting with everything unchecked is sane for a risky new-machine setup, while `--all --dry-run` gives a useful audit path.
- Auto-installing `mas` when App Store apps are selected is a strong affordance.
- Failed installs are easy to miss because each command keeps going; collect failures and print a final summary.

## Misc
- README and setup notes agree on the important Homebrew/admin constraint, which is the main foot-gun here.
- The manual app list is honest and useful; keep it visible rather than pretending everything is automatable.
- Add a tiny test for duplicate casks/App Store IDs and for `--all` selecting every installable item.
