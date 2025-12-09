# Persian Phonebook App

A simple yet powerful phonebook application built with Python and Tkinter, specifically designed to handle Persian text correctly. This application allows you to manage your contacts with a user-friendly interface that supports Persian language.

## Features

- **Contact Management**: Add, edit, delete, and search contacts
- **Database Storage**: Uses SQLite for reliable data storage
- **Backup & Restore**: Backup your contacts to JSON and restore them when needed
- **VCF Import**: Import contacts from VCF files with intelligent Persian text decoding
- **Customizable Fonts**: Change font family and size to better display Persian text
- **Search Functionality**: Filter contacts by name or phone number
- **Persian UI**: Full Persian language interface

## Screenshots

*Add screenshots here when available*

## Installation

1. Make sure you have Python installed (3.6 or higher)
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/persian-phonebook.git
   cd persian-phonebook
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python phonebook.py
   ```

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)
- sqlite3 (usually comes with Python)

## Usage

1. **Adding Contacts**: Click the "➕ Add Contact" button to add a new contact
2. **Editing Contacts**: Select a contact from the list and click "✏️ Edit Contact"
3. **Deleting Contacts**: Select a contact and click "❌ Delete Contact"
4. **Searching**: Use the search box to filter contacts by name or phone number
5. **Backup**: Click "💾 Backup" to save your contacts to a JSON file
6. **Restore**: Click "🔄 Restore Backup" to load contacts from a backup file
7. **Import VCF**: Click "📥 Import VCF" to import contacts from a VCF file
8. **Font Settings**: Click "⚙️ Font Settings" to customize the font family and size

## VCF Import Features

The application includes advanced VCF import functionality with intelligent Persian text decoding:

- Supports multiple VCF formats
- Handles QUOTED-PRINTABLE and BASE64 encoding
- Detects and decodes Persian characters in various encoding formats
- Extracts names from FN, N, and ORG fields
- Handles multi-line entries in VCF files
- Automatically skips duplicate contacts

## Database Structure

The application uses an SQLite database with a single table:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
```

## Settings

The application saves font settings in a JSON file (`phonebook_settings.json`) in the same directory as the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Python and Tkinter communities for providing excellent documentation and tools
- Special thanks to those who contributed to Persian language support in Python applications
# Persian Phonebook Application

A comprehensive phonebook application built with Python and Tkinter, specifically designed to handle Persian text correctly. This application provides a user-friendly interface for managing contacts with full support for Persian language.

## Features

- **Contact Management**: Add, edit, delete, and search contacts
- **Database Storage**: Uses SQLite for reliable data storage
- **Backup & Restore**: Backup your contacts to JSON and restore them when needed
- **VCF Import**: Import contacts from VCF files with intelligent Persian text decoding
- **Customizable Fonts**: Change font family and size to better display Persian text
- **Search Functionality**: Filter contacts by name or phone number
- **Persian UI**: Full Persian language interface

## Installation

1. Make sure you have Python installed (3.6 or higher)
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/persian-phonebook.git
   cd persian-phonebook
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python phonebook.py
   ```

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)
- sqlite3 (usually comes with Python)

## Usage

1. **Adding Contacts**: Click the "➕ Add Contact" button to add a new contact
2. **Editing Contacts**: Select a contact from the list and click "✏️ Edit Contact"
3. **Deleting Contacts**: Select a contact and click "❌ Delete Contact"
4. **Searching**: Use the search box to filter contacts by name or phone number
5. **Backup**: Click "💾 Backup" to save your contacts to a JSON file
6. **Restore**: Click "🔄 Restore Backup" to load contacts from a backup file
7. **Import VCF**: Click "📥 Import VCF" to import contacts from a VCF file
8. **Font Settings**: Click "⚙️ Font Settings" to customize the font family and size

## VCF Import Features

The application includes advanced VCF import functionality with intelligent Persian text decoding:

- Supports multiple VCF formats
- Handles QUOTED-PRINTABLE and BASE64 encoding
- Detects and decodes Persian characters in various encoding formats
- Extracts names from FN, N, and ORG fields
- Handles multi-line entries in VCF files
- Automatically skips duplicate contacts

## Database Structure

The application uses an SQLite database with a single table:

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL
);
```

## Settings

The application saves font settings in a JSON file (`phonebook_settings.json`) in the same directory as the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details."# PyContacts" 
"# PyContacts" 
