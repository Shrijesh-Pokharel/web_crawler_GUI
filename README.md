# Web Crawler GUI

This project is a graphical user interface (GUI) for a web crawler, developed by [Shrijesh Pokharel](https://shrijesh.com.np/). It enables users to input a URL and retrieve the HTML and XML content of the specified website. The application provides options to view, edit, or copy the extracted content.

## Features

- **URL Input**: Enter the desired website URL to initiate the crawling process.
- **Content Extraction**: Retrieve and display the HTML and XML content of the specified URL.
- **Edit and Copy Functionality**: View the extracted content with options to edit or copy it for further use.

## Requirements

- Python 3.10 or higher
- Required Python libraries:
  - `requests`
  - `beautifulsoup4`
  - `tkinter`

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Shrijesh-Pokharel/web_crawler_GUI.git
   ```



2. **Navigate to the Project Directory**:

   ```bash
   cd web_crawler_GUI
   ```



3. **Install the Required Libraries**:

   ```bash
   pip install requests beautifulsoup4
   ```



   Note: `tkinter` is included with standard Python installations. If it's not available, install it using your system's package manager.

## Usage

1. **Run the Application**:

   ```bash
   python web_crawler_GUI.py
   ```



2. **Using the GUI**:

   - Enter the URL of the website you wish to crawl in the input field.
   - Click the "Crawl" button to retrieve the content.
   - The extracted HTML and XML content will be displayed in the text area.
   - You can edit the content directly within the application.
   - Use the "Copy" button to copy the content to your clipboard for use in other applications.

