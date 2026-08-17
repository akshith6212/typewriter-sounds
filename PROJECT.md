# Typewriter Sounds Emulator

## Overview

A Python desktop utility that plays realistic typewriter sound effects in response to every keystroke, providing a vintage typing experience. It listens for **global** keyboard events (works across all applications, not just a terminal) and maps different key categories to distinct typewriter audio samples.

## Architecture

This is a single-file Python application (`typewriter_sounds.py`) with no build system, no tests, and no package configuration.

### Core Class: `TypeWriterSounds`

Located in `typewriter_sounds.py`. Encapsulates all logic in one class instantiated at module-level via `if __name__ == '__main__'`.

**Initialization flow:**
1. Initializes `pygame.mixer` with a small 512-byte buffer (for low-latency audio playback).
2. Loads 7 `.wav` sound samples from the `samples/` directory into a `keysounds` dictionary.
3. Plays an introductory bell + enter sound.
4. Starts a blocking `pynput.keyboard.Listener` that calls `on_key_press` on every global keypress.
5. Runs until the user sends `CTRL-C` (`KeyboardInterrupt`).

**Key-to-sound mapping (`on_key_press`):**

| Key Category | Keys | Sound File | Dict Key |
|---|---|---|---|
| Enter/Return | `Key.enter` | `manual_return.wav` | `enter` |
| Space | `Key.space` | `manual_space.wav` | `space` |
| Delete/Backspace | `Key.delete`, `Key.backspace` | `manual_backspace.wav` | `delete` |
| Modifier/Navigation | Shift, Ctrl, Alt, Cmd, arrows, Tab, Caps Lock, F1-F12, Esc | `manual_shift.wav` | `shift` |
| Page navigation | Page Up/Down, Home, End | `manual_load_long.wav` | `load` |
| All other keys | Alphanumeric, symbols, etc. | `manual_key.wav` | `key` |

**Bell mechanism:**
- A `bellcount` counter increments on each regular key or space press.
- Backspace decrements it (clamped to 0).
- Enter resets it to 0.
- When it reaches **70**, the typewriter bell (`manual_bell.wav`) plays and the counter resets — simulating the margin bell on a real typewriter.

## Dependencies

| Package | Purpose | Version Notes |
|---|---|---|
| `pynput` | Cross-platform global keyboard event listener | Any recent version |
| `pygame` | Audio mixer for low-latency `.wav` playback | 2.x |

Both are pure pip-installable. There is no `requirements.txt`, `setup.py`, or `pyproject.toml` in the repo.

Install manually:
```bash
pip install pynput pygame
```

## File Structure

```
typewriter-sounds/
  typewriter_sounds.py    # Entire application (114 lines)
  README.md               # Original project readme
  samples/                # WAV audio samples (from freesound.org)
    manual_backspace.wav
    manual_bell.wav
    manual_feed.wav        # Present but unused in code
    manual_key.wav
    manual_return.wav
    manual_load_long.wav
    manual_shift.wav
    manual_space.wav
```

## Running

```bash
cd typewriter-sounds
python typewriter_sounds.py
```

Stop with `CTRL-C`.

**Platform notes:**
- On macOS, the terminal (or Python) needs **Accessibility permissions** in System Settings > Privacy & Security > Accessibility for `pynput` to capture global keystrokes.
- On Linux, may need to run with elevated privileges or add the user to the `input` group.
- On Windows, works out of the box.

## History

- Originally written for Python 2.7 using Xlib (X11-only, Linux).
- Upgraded to Python 3 with `pynput` for cross-platform support (commit `7a69a42`).
- Author: Manuel Arturo Izquierdo (`aizquier@gmail.com`).

## Notable Details

- `manual_feed.wav` exists in `samples/` but is **not loaded or used** by the code.
- The `bellcount` threshold of 70 characters roughly matches the column width of a standard typewriter carriage.
- The pygame mixer buffer is set to 512 bytes for minimal audio latency; increasing it may cause perceptible delay between keypress and sound.
- There are no command-line arguments, configuration files, or settings — behavior is entirely hardcoded.
- No graceful shutdown beyond catching `KeyboardInterrupt`.
