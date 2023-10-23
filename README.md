# Tesseract Text Extractor

Tesseract Text Extractor is a tool for extracting text from images and documents. It utilizes the power of Tesseract OCR, an open-source Optical Character Recognition engine, to perform text recognition and extraction.

## Q&A

### A. How accurate exactly does this extract images? And will it work with different inputs?

**Since it is given to have the same documentation format, yes it will definitely work with inputs. Whatsoever, inputs with accent letters will have to manually be checked as it is inaccurate when it comes to ISO detection.**

### B. How will you implement this in a website?

**Same as usual... but actually, I am having problem with flask compatibility so I will have to deal with that and maybe I will still use flask for the database. Regardless, it is still being planned.**

### C. What library is used on this?

**The library used on this is pytesseract—a popular OCR for image-to-text tool. Lastly, we used pdf-to-image module for the OCR tool to use on (it can be anything, there are a lot of library that can do this).**


## Features

- Extract text from images, scanned documents, and PDF files.
- Support for multiple languages.
- High accuracy and performance, thanks to the Tesseract OCR engine.
- Simple and easy-to-use command-line interface.

## Installation

1. **Install Tesseract OCR**: Before using this tool, make sure you have Tesseract OCR installed. You can download it from [the official Tesseract GitHub repository](https://github.com/tesseract-ocr/tesseract).

2. **Clone the Repository**:

```
 git clone https://github.com/yourusername/tesseract-text-extractor.git
 Install Dependencies:
 
 pip install -r requirements.txt
```
   
## Usage

   ```
    Basic Usage:
    
    To extract text from an image, simply run:
    
    python extract_text.py image.png
    Options:
    
    -l, --lang: Specify the language (default is English).
    -o, --output: Specify the output file (default is stdout).
    Example
    python extract_text.py image.png -l eng -o extracted_text.txt
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
Tesseract OCR - https://github.com/tesseract-ocr/tesseract
Feel free to customize this README according to your project's specific details and needs. You can also add more sections, such as "Contributing," "Credits," or "Support," depending on your project's requirements.

You can create a new repository on GitHub, add this content to the `README.md` file, and customize it to fit your project. Don't forget to replace `yourusername` with your GitHub username in the repository URL.
