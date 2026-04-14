#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

require_admin_user_for_brew_install() {
  if [[ "$(id -u)" -eq 0 ]]; then
    echo "Do not run this script with sudo."
    echo "Homebrew must be installed as a normal macOS user, not root."
    exit 1
  fi

  if dseditgroup -o checkmember -m "$(id -un)" admin | grep -q "yes"; then
    return
  fi

  echo "Homebrew is not installed, and this user is not a macOS Administrator."
  echo "Homebrew installation requires an administrator account."
  echo "Log in as an admin user or grant admin rights to $(id -un), then rerun this script."
  exit 1
}

ensure_brew() {
  if command -v brew >/dev/null 2>&1; then
    return
  fi

  require_admin_user_for_brew_install
  echo "Homebrew not found. Installing Homebrew..."
  NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  elif [[ -x /usr/local/bin/brew ]]; then
    eval "$(/usr/local/bin/brew shellenv)"
  fi
}

ensure_python3() {
  if command -v python3 >/dev/null 2>&1; then
    return
  fi

  echo "python3 not found. Installing Python with Homebrew..."
  brew install python
}

ensure_brew
ensure_python3

exec python3 "$SCRIPT_DIR/setup_macos_apps.py" "$@"
