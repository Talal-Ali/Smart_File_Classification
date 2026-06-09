# Smart File Classification

A Python-based file organization tool that automatically sorts and categorizes files based on their extensions. Perfect for organizing cluttered directories with ease.

## Overview

Smart File Classification is a lightweight utility designed to help you organize directories by automatically categorizing files into folders based on their file extensions. The system watches directories in real-time and features a user-friendly UI for configuration and dynamic category management, backed by a robust database for extensible file type support.

## 🎯 Key Features

- **Automatic File Categorization**: Organizes files into logical categories (Documents, Images, Videos, Audio, Developer, etc.)
- **File Extension-Based Classification**: Uses file extensions to determine the appropriate category
- **Real-Time Monitoring**: Watches directories and automatically sorts new files as they arrive
- **Batch Processing**: Organize all existing files in a directory with a single command
- **Safe Organization**: Creates category folders automatically if they don't exist
- **Database-Driven Architecture**: Manage file type mappings efficiently with database support
- **Dynamic Categories**: Create, modify, and manage custom file categories on-the-fly
- **Settings UI**: User-friendly interface for configuring directories and file type mappings
- **Configuration-Driven**: Simple config file for specifying watch and target directories
- **Extensible Architecture**: Foundation ready for advanced customization and integrations

## 📋 Scope & Roadmap

### ✅ Completed
- [x] File classification based on extension
- [x] Real-time file monitoring and organization
- [x] Batch processing of existing files
- [x] Configuration file support
- [x] Automatic folder creation
- [x] **Database Implementation** - Persistent storage for file type mappings
- [x] **UI for Settings** - User-friendly interface for configuration management
- [x] **Dynamic Categories** - Create and modify categories without code changes

### 🚀 Planned Features
- [ ] **GUI Interface**: Full-featured graphical interface with drag-and-drop support
- [ ] **Advanced Filtering**: Filter files by date, size, or custom criteria
- [ ] **Undo Functionality**: Ability to revert file movements
- [ ] **System Tray Integration**: Windows Explorer context menu integration
- [ ] **Logging & Analytics**: Track file organization history and statistics
- [ ] **Multi-Profile Support**: Save and switch between different organization profiles

## 📥 Installation

### Requirements
- Python 3.6+
- SQLite3 (or compatible database)

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

### Via Configuration File
Edit `config.txt` to specify your watch and target directories:

```
WATCH_DIRECTORY=C:/Users/YourName/Downloads
TARGET_DIRECTORY=C:/Users/YourName/Downloads/Organized_Files
```

- **WATCH_DIRECTORY**: The folder where new files appear (files here will be organized)
- **TARGET_DIRECTORY**: Where organized files will be sorted into category subfolders

### Via Settings UI
Launch the settings interface to:
- Configure watch and target directories
- View and manage file type mappings
- Create and modify custom categories
- Update database settings

## 🚀 Usage

### Run the Organizer
```bash
python Smart_File_Classification_System.py
```

The script will:
1. Load your configuration from the database or config file
2. Organize all existing files in the watch directory
3. Start monitoring for new files
4. Open the settings UI for real-time adjustments
5. Press `Ctrl+C` to stop

### Open Settings UI
```bash
python settings_ui.py
```

Manage all aspects of file organization through the graphical interface:
- Add/remove file extensions
- Create custom categories
- Configure directory paths
- Preview organization rules

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

The tool organizes files into the following categories (customizable via database):

| Category | Sample Extensions |
|----------|-----------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.pptx`, `.txt`, `.xlsx`, etc. |
| **Pictures_n_GIFS** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, etc. |
| **Developer** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, etc. |
| **Video** | `.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`, etc. |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, etc. |
| **Other** | Files that don't fit into above categories |

**Note**: Categories are now stored in the database and can be easily modified through the settings UI.

## 🏗️ Project Structure

```
Smart_File_Classification/
├── README.md                              # This file
├── Smart_File_Classification_System.py    # Main script with file monitoring
├── settings_ui.py                         # Settings UI for configuration management
├── database.py                            # Database management module
├── config.txt                             # Configuration file (user-customizable)
├── file_categories.db                     # SQLite database (auto-generated)
├── Datatypes.xlsx                         # Reference file type mappings
├── requirements.txt                       # Python dependencies
└── .gitattributes                         # Git configuration
```

## 🔄 How It Works

1. **Loads Configuration**: Reads watch and target directories from `config.txt` or database
2. **Database Initialization**: Sets up SQLite database for file type mappings and categories
3. **Organizes Existing Files**: Scans and categorizes all files already in the watch directory
4. **Monitors for New Files**: Watches the directory for newly created or added files
5. **Identifies Extensions**: Extracts file extensions and matches them to categories via database
6. **Creates Folders**: Automatically creates category folders if needed
7. **Moves Files**: Transfers files to their corresponding category folders
8. **Logs Activity**: Prints organized file information to the console
9. **Supports Dynamic Updates**: Changes to categories take effect immediately through the UI

## 🛠️ Database Features

### File Type Mappings
- Store unlimited file extensions and their corresponding categories
- Quickly query category associations
- Easily add or remove file types without code changes

### Dynamic Category Management
- Add new categories on-the-fly
- Modify existing category definitions
- Delete unused categories
- Track category usage statistics

### Benefits
- **Scalability**: Support for thousands of file extension categories
- **Flexibility**: No need to modify code to add new file types
- **Persistence**: All configurations saved between sessions
- **Performance**: Optimized queries for fast file lookups

## 💡 Example Workflow

```
Downloads/
├── document.pdf          → Organized/Documents/
├── photo.jpg             → Organized/Pictures_n_GIFS/
├── script.py             → Organized/Developer/
├── video.mp4             → Organized/Video/
├── song.mp3              → Organized/Audio/
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

**Note**: This is an actively developed project. The latest version includes database implementation, a settings UI for easy configuration, and dynamic category management. Expect continued improvements and new features!
