# Smart File Classification

Smart File Classification is a lightweight Python utility that automatically sorts and organizes files into category folders based on file extensions. It's designed to declutter directories (Downloads, Desktop, etc.) by moving files into meaningful categories, with support for real-time monitoring and persistent configuration.

## Key Features

- Automatic file categorization by extension (Documents, Images, Video, Audio, Developer, etc.)
- Real-time directory monitoring (watches for new files and organizes them automatically)
- Batch processing for existing files in a directory
- Safe organization: automatically creates category folders when needed
- Database-driven mappings: manage file-extension → category associations in SQLite
- Dynamic categories: add, edit, and remove categories without changing code
- Settings UI for easy configuration and mapping management
- Configuration file support for simple setup and automation

## Requirements

- Python 3.6+
- SQLite3 (or compatible)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Talal-Ali/Smart_File_Classification.git
cd Smart_File_Classification
```

2. (Recommended) create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

There are two ways to configure watched and target directories:

1. config.txt (simple text configuration)

```
WATCH_DIRECTORY=C:/Users/YourName/Downloads
TARGET_DIRECTORY=C:/Users/YourName/Downloads/Organized_Files
```

2. Settings UI — launch the UI to configure directories and manage file type mappings (recommended for non-technical users).

## Usage

Run the organizer to process existing files and start live monitoring:

```bash
python Smart_File_Classification_System.py
```

What the script does:
- Loads configuration from the database or config file
- Organizes existing files in the watch directory
- Starts monitoring the watch directory for new files
- Opens the Settings UI (if available)
- Press `Ctrl+C` to stop

Open the Settings UI separately (if needed):

```bash
python settings_ui.py
```

## Supported Categories

Categories are customizable via the database. Default examples include:

- Documents: `.pdf`, `.doc`, `.docx`, `.pptx`, `.txt`, `.xlsx`, etc.
- Pictures: `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, etc.
- Developer: `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, etc.
- Video: `.mp4`, `.avi`, `.mov`, `.mkv`, etc.
- Audio: `.mp3`, `.wav`, `.flac`, `.aac`, etc.
- Other: files that don't match any category

## How it works (brief)

1. Read watch/target directories from config or database
2. Initialize or open the SQLite database for file-type mappings
3. Optionally scan and organize existing files in the watch directory
4. Monitor the directory for new files and organize them based on extension
5. Log actions to console; settings changes apply immediately (via UI)

## Example

```
Downloads/
├── document.pdf     → Organized/Documents/
├── photo.jpg        → Organized/Pictures/
├── script.py        → Organized/Developer/
├── video.mp4        → Organized/Video/
└── song.mp3         → Organized/Audio/
```

## Project Structure

```
Smart_File_Classification/
├── README.md
├── Smart_File_Classification_System.py
├── settings_ui.py
├── database.py
├── config.txt
├── file_categories.db
├── Datatypes.xlsx
├── requirements.txt
└── .gitattributes
```

## Contributing

Contributions are welcome. To contribute:
1. Fork the repository
2. Create a feature branch
3. Open a pull request with a clear description of changes

## Issues & Feedback

Open an issue on GitHub if you find bugs or have feature requests.

## License

This project is licensed under the MIT License.

## Author

Talal-Ali — https://github.com/Talal-Ali
