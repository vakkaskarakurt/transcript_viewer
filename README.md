# Transcript Viewer Application

---

## Overview
The Transcript Viewer is a Python-based application designed for reading, translating, and managing transcripts from websites. This tool provides a user-friendly graphical interface built with `tkinter`, enabling seamless navigation, text translation, and other text-related functionalities.

---

## Features
- **Load Transcripts from URL**: Fetch and display transcript text directly from specified URLs.
- **Text Navigation**: Navigate through transcript lines with "Previous" and "Next" buttons or keyboard shortcuts.
- **Translation**: Translate text between English and Turkish using Google Translator.
- **Text Management**:
  - Copy text to the clipboard.
  - View current progress with line counters.
  - Save and resume transcript reading position.
- **Customizable Interface**: Includes a dark theme with styled buttons and text areas for an enhanced user experience.
- **Keyboard Shortcuts**:
  - `Left Arrow`: Show the previous line.
  - `Right Arrow`: Show the next line.
  - `Ctrl+C`: Copy the current text.
  - `C`: Toggle translation view.

---

## Dependencies
The application requires the following Python libraries:

- **Core Libraries**:
  - `tkinter` (GUI components)
  - `pyperclip` (Clipboard management)
  - `asyncio` (Asynchronous tasks)
  - `json` (Data storage)
  - `os`, `threading`, `time` (System and threading utilities)
- **Third-party Libraries**:
  - `deep_translator` (Google Translator integration)
  - `undetected_chromedriver` (Browser automation for undetected usage)
  - `selenium` (Web scraping and interaction)

To simplify installation, a `requirements.txt` file is provided. Install all dependencies by running:
```bash
pip install -r requirements.txt
