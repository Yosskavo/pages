# Inverted Environment Dotfiles

This repository contains the configuration files and dependencies required to replicate the Abyss desktop and terminal environment. It is built around a tiling window manager, a heavily customized Zsh shell, and modern Rust-based command-line utilities.

---

## 1. Core System & Window Management
These packages form the graphical foundation of the environment.

*   **i3wm**: The core tiling window manager.
*   **Picom**: The X11 compositor (handles transparency and window glow effects).
*   **Polybar**: The customizable status bar.
*   **Rofi**: The application launcher and custom menu engine (used for keybinds, settings, etc.).
*   **Dunst**: The lightweight notification daemon.

---

## 2. Terminal & Shell
The terminal is optimized for speed, aesthetics, and efficient keyboard navigation.

*   **Kitty**: The GPU-accelerated terminal emulator.
*   **Zsh**: The default shell.
*   **Oh My Zsh**: The framework for managing the Zsh configuration.
*   **Starship**: The cross-shell prompt (configured via `starship.toml`).

---

## 3. Zsh Plugins
These plugins must be installed for the shell configuration to source correctly without errors.

*   **fzf-tab**: Replaces standard Zsh completion with an interactive fuzzy-finder menu.
*   **zsh-autosuggestions**: Provides fish-like ghost text suggestions based on history.
*   **zsh-syntax-highlighting**: Colors commands as they are typed (customized with Tokyo Night hex codes).
*   **fzf**: The general-purpose command-line fuzzy finder.

---

## 4. CLI Utilities & Modern Replacements
Standard UNIX commands are aliased to modern, feature-rich alternatives.

*   **lsd**: Modern replacement for `ls` with icons and colors (aliases: `ls`, `la`, `ll`, `lt`).
*   **bat**: Modern replacement for `cat` with syntax highlighting and Git integration.
*   **glow**: CLI Markdown renderer used by the custom `cat` function to read `.md` files.
*   **yazi**: Blazing fast terminal file manager.
*   **fastfetch**: System information fetcher.
*   **btop** & **htop**: Resource monitors.
*   **grc** (Generic Colouriser): Used to colorize terminal output for specific tools like Valgrind.

---

## 5. Development Tools
Tools specifically configured for C/C++ development and general text editing.

*   **Neovim**: The core text editor and manpager.
*   **clangd**: The C/C++ language server.
*   **lazygit**: The terminal UI for Git commands.
*   **Valgrind**: Memory debugging tool (aliased to use `grc` for readable colored output).

---

## Directory Structure Overview
Based on the repository layout, here is what each folder controls:

*   `bat/`: Syntax highlighting themes and configurations.
*   `btop/` & `htop/`: System monitor visual themes and layouts.
*   `clangd/`: Global C/C++ language server settings.
*   `dunst/`: Notification appearance and geometry rules.
*   `fastfetch/`: ASCII art and system module configurations.
*   `glow/`: Markdown rendering themes (Tokyo Night style).
*   `i3/`: Window manager keybinds, workspaces, and window rules.
*   `kitty/`: Terminal fonts, padding, and color schemes.
*   `lazygit/`: Git TUI keybinds and styling.
*   `lsd/`: Icon and color configurations for directory listings.
*   `picom/`: Shadow, fade, and transparency rules.
*   `polybar/`: Status bar modules and hardware sensors.
*   `rofi/`: App launcher themes and custom bash menu scripts.
*   `starship/`: Shell prompt styling.
*   `yazi/`: File manager layout and previews.
*   `zsh/` & `.zshrc`: Shell aliases, environment variables, and Vi-mode bindings.
