# Smart File Classification

A Python-based file organization tool that automatically sorts and categorizes files based on their extensions. Perfect for organizing cluttered directories with ease.

## Overview

Smart File Classification is a lightweight utility designed to help you organize directories by automatically categorizing files into folders based on their file extensions. The system watches directories for new files, organizes existing files, and provides extensibility through configuration and database support.

## 🎯 Key Features

- **Automatic File Categorization**: Organizes files into logical categories (Documents, Images, Videos, Audio, Developer, etc.)
- **File Extension-Based Classification**: Uses file extensions to determine the appropriate category
- **Real-Time Monitoring**: Watches directories and automatically sorts new files as they arrive
- **Batch Processing**: Organize all existing files in a directory with a single command
- **Safe Organization**: Creates category folders automatically if they don't exist
- **Configuration-Driven**: Simple config file for specifying watch and target directories
- **Extensible Architecture**: Foundation ready for database and custom category support

## 📋 Scope & Roadmap

### ✅ Completed
- [x] File classification based on extension
- [x] Real-time file monitoring and organization
- [x] Batch processing of existing files
- [x] Configuration file support
- [x] Automatic folder creation

### 🚀 Planned Features
- [ ] **GUI Interface**: Simple button-based file explorer integration for one-click organization
- [ ] **Database Support**: Read file type mappings from a database for managing vast amounts of file types
- [ ] **Custom Categories**: Allow users to define their own file types and categories
- [ ] **Undo Functionality**: Ability to revert file movements
- [ ] **Advanced Filtering**: Filter files by date, size, or custom criteria
- [ ] **System Tray Integration**: Windows Explorer context menu integration

## 📥 Installation

### Requirements
- Python 3.6+

### Dependencies
```bash
pip install watchdog
```

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Talal-Ali/Smart_File_Classification.git
cd Smart_File_Classification
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the directories (see Configuration section below)

## ⚙️ Configuration

Edit `config.txt` to specify your watch and target directories:

```
WATCH_DIRECTORY=C:/Users/YourName/Downloads
TARGET_DIRECTORY=C:/Users/YourName/Downloads/Organized_Files
```

- **WATCH_DIRECTORY**: The folder where new files appear (files here will be organized)
- **TARGET_DIRECTORY**: Where organized files will be sorted into category subfolders

## 🚀 Usage

### Run the Organizer
```bash
python Smart_File_Classification_System.py
```

The script will:
1. Load your configuration
2. Organize all existing files in the watch directory
3. Start monitoring for new files
4. Press `Ctrl+C` to stop

### Example

Organize files in your Downloads folder:
```bash
# Update config.txt with your Downloads path
WATCH_DIRECTORY=~/Downloads
TARGET_DIRECTORY=~/Downloads/Organized

# Run the script
python Smart_File_Classification_System.py
```

## 📂 Supported Categories

The tool organizes files into the following categories:

| Category | Extensions |
|----------|-----------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.pptx`, `.txt`, `.xlsx`, etc. |
| **Pictures_n_GIFS** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, etc. |
| **Developer** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, etc. |
| **Video** | `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, etc. |
| **Other** | Files that don't fit into above categories |

## 🏗️ Project Structure

```
Smart_File_Classification/
├── README.md                              # This file
├── Smart_File_Classification_System.py    # Main script with file monitoring
├── config.txt                             # Configuration file (user-customizable)
├── Datatypes.xlsx                         # Reference file type mappings
├── requirements.txt                       # Python dependencies
└── .gitattributes                         # Git configuration
```

## 🔄 How It Works

1. **Loads Configuration**: Reads watch and target directories from `config.txt`
2. **Organizes Existing Files**: Scans and categorizes all files already in the watch directory
3. **Monitors for New Files**: Watches the directory for newly created or added files
4. **Identifies Extensions**: Extracts file extensions and matches them to categories
5. **Creates Folders**: Automatically creates category folders if needed
6. **Moves Files**: Transfers files to their corresponding category folders
7. **Logs Activity**: Prints organized file information to the console

## 🛠️ Future Enhancements

### GUI Interface
- Simple button-based integration with Windows File Explorer
- Ability to trigger organization on-demand from context menu

### Database Support
- Store file type mappings in a database (e.g., SQLite, JSON)
- Easily manage and extend supported file types without code changes
- Support for thousands of file extension categories

### Custom Categories
- User interface to define custom file type categories
- Save custom configurations per directory
- Support for multiple classification profiles

## 💡 Example Workflow

```
Downloads/
├── document.pdf          → Organized/Documents/
├── photo.jpg             → Organized/Pictures_n_GIFS/
├── script.py             → Organized/Developer/
├── video.mp4             → Organized/Video/
└── random_file.txt       → Organized/Other/
```

## 🤝 Contributing

Contributions are welcome! Feel free to fork this project and submit pull requests with improvements.

## 📝 Issues & Feedback

If you encounter any issues or have suggestions for improvement, please open an issue on GitHub.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Talal-Ali** - [GitHub Profile](https://github.com/Talal-Ali)

---

**Note**: This is an actively developed project. Expect updates and improvements as we implement the planned features including GUI integration, database support, and custom category definitions!
