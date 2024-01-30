# Easy PDF Merger

Easy PDF Merger is a simple web application built with Streamlit that allows users to merge multiple PDF files into a single PDF file. This tool is user-friendly and requires no prior experience with PDF merging software.

https://mergepdf-easy.streamlit.app/

## Features

- **Upload Multiple PDFs**: Users can select and upload multiple PDF files.
- **Reorder PDFs**: Users can adjust the order of the PDF files before merging.
- **Merge & Download**: With a single click, merge the uploaded PDFs and download the merged PDF.

## Installation

To run this application on your local machine, you'll need Python3.x installed. If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/) and follow the installation instructions.

1. Clone this repository or download the source code:

```bash
git clone https://github.com/hwonheo/mergePDF-webui.git
cd mergePDF-webui
```

## Install the required Python packages

```bash
pip install -r requirements.txt
```

## How to Run

After installing the required packages, run the application using Streamlit:

```bash
streamlit run app.py
```

The application will start, and your web browser should automatically open a new tab with the app running.

## How to Use

1. Upload PDFs: Click the 'Select PDF files' button in the sidebar to upload your PDF files.
2. Adjust Order: The uploaded files will be displayed in the main area. Select a file and use the 'Up' and 'Down' buttons to adjust the order.
3. Merge PDFs: Click the 'Merge PDFs' button to merge the files into a single PDF.
4. Download: Click the 'Download Merged PDF' button to save the merged PDF to your device.

## License

This project is open source and available under the MIT License.
