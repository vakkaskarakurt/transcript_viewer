# transcript_viewer
A minimal and intuitive transcript viewer to read, translate, and navigate TV show transcripts easily. Initially designed for "https://tvshowtranscripts.ourboard.org/", but extensible for other use cases.

# Transcript Viewer

Transcript Viewer is a Python-based application that allows you to navigate, read, and translate transcripts of TV shows easily. This app is currently optimized for transcripts copied from [TV Show Transcripts](https://tvshowtranscripts.ourboard.org/), but it can be adapted for other sources.

## Features

- **Easy Navigation**: Navigate through transcripts with `Next` and `Previous` buttons or jump to specific lines.
- **Translation**: Translate selected transcript text into English using the Google Translator API.
- **Copy Functionality**: Quickly copy text to your clipboard for external use.
- **State Saving**: Automatically saves your position in the transcript, so you can continue from where you left off.
- **Keyboard Shortcuts**: Use shortcuts for quick navigation and actions.

## Keyboard Shortcuts

- `Right Arrow`: Go to the next transcript line.
- `Left Arrow`: Go to the previous transcript line.
- `C` : Toggle translation for the current transcript.
- `"` : Toggle translation for the current transcript.
- `Enter`: Jump to a specific line using the input field.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/vakkaskarakurt/transcript_viewer.git
   cd transcript_viewer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## How to Use

1. Copy transcript content from [TV Show Transcripts](https://tvshowtranscripts.ourboard.org/). 
Supernatural Season 1 Episode 10 Example:  "https://tvshowtranscripts.ourboard.org/viewtopic.php?f=105&t=6570"
!!!(Not compatible with the text in this link: https://tvshowtranscripts.ourboard.org/viewtopic.php?f=105&t=6570&view=print)

2. Save it to a file named `transcript.txt` in the same directory as the script.
3. Launch the app, and start navigating and translating the transcript!

## Planned Features

- Support for directly loading transcripts from the website.
- Enhanced translation options for multiple languages.
- Improved UI/UX with themes and customization.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.
