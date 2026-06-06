# Smart File Classification

A Python-based file organization tool that automatically sorts and categorizes files based on their extensions.

## Overview

Smart File Classification is a lightweight utility designed to help you organize cluttered directories by automatically categorizing files into folders based on their file extensions. Perfect for cleaning up downloads, projects, or any directory with mixed file types.

## Features

- **Automatic File Categorization**: Organizes files into logical categories (Documents, Images, Videos, Audio, Archives, Code, etc.)
- **Extension-Based Classification**: Uses file extensions to determine the appropriate category
- **Batch Processing**: Process entire directories with a single command
- **Safe Organization**: Creates category folders if they don't exist

## Installation

### Requirements
- Python 3.6+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Talal-Ali/Smart_File_Classification.git
cd Smart_File_Classification
```

2. No external dependencies required - uses Python standard library only

## Usage

```python
# Basic usage example
python smart_file_classification.py /path/to/directory
```

### Example

Organize files in your Downloads folder:
```bash
python smart_file_classification.py ~/Downloads
```

## Supported Categories

The tool organizes files into the following categories:

- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.xlsx`, `.pptx`, etc.
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, etc.
- **Videos**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, etc.
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.m4a`, etc.
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, etc.
- **Code**: `.py`, `.js`, `.java`, `.cpp`, `.html`, `.css`, etc.
- **Others**: Files that don't fit into above categories

## Project Structure

```
Smart_File_Classification/
├── README.md
├── smart_file_classification.py
└── [other source files]
```

## How It Works

1. **Scans** the specified directory for all files
2. **Identifies** file extensions
3. **Categorizes** files based on predefined extension mappings
4. **Creates** category folders if needed
5. **Moves** files to their corresponding category folders

## Roadmap

- [x] Initial file classification logic
- [ ] GUI interface
- [ ] Custom category configuration
- [ ] Undo functionality
- [ ] Configuration file support
- [ ] Advanced filtering options

## Contributing

Contributions are welcome! Feel free to fork this project and submit pull requests with improvements.

## Issues & Feedback

If you encounter any issues or have suggestions for improvement, please open an issue on GitHub.

## License

This project is open source and available under the MIT License.

## Author

**Talal-Ali** - [GitHub Profile](https://github.com/Talal-Ali)

---

**Note**: This is the first iteration of Smart File Classification. Expect updates and improvements as the project evolves!
