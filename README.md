# Transcript Viewer Application

A Python application for viewing, translating, and managing HTML transcript files.

## Key Features

- Load and read HTML transcript files
- Navigate through lines with buttons or keyboard arrows
- English to Turkish translation using Google Translate
- Copy text to clipboard
- Save/resume reading position
- Dark theme interface

## Usage

1. Click "Load File" to select an HTML transcript file
2. Use Previous/Next buttons or arrow keys to navigate
3. Press "Translate" button or 'C' key to view Turkish translation
4. Click "Copy" to copy current text

## Shortcuts

- `Left/Right Arrow`: Navigate lines
- `Ctrl+C`: Copy text  
- `C`: Toggle translation
- `Enter`: Go to entered line number

## Dependencies

Required packages:
```
tkinter
pyperclip  
deep_translator
beautifulsoup4
```

Install via:
```bash
pip install -r requirements.txt
```

## Getting Started

1. Download an HTML transcript file from your source
2. Launch the application
3. Load the HTML file using the interface
4. Navigate through the transcript

The application automatically saves your position between sessions.
