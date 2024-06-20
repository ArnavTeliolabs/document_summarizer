from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from src.abstractive_summarizer import abstractive_summary
from src.pdf_handler import extract_text_from_pdf
from src.docx_handler import extract_text_from_docx
import os
import time
import tempfile

app = Flask(__name__, template_folder='.')

# Maximum word length for input text
MAX_WORD_LENGTH = 1000000

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    return render_template('summary.html', summary=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file and allowed_file(file.filename):
        # Save the uploaded file to a temporary directory
        file_path = os.path.join(tempfile.gettempdir(), secure_filename(file.filename))
        file.save(file_path)

        # Check the word length of the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            word_count = len(f.read().split())

        # Check if the word length exceeds the maximum
        if word_count > MAX_WORD_LENGTH:
            os.remove(file_path)
            return "Maximum word length exceeded (10000 words)"

        # Extract text from the PDF or DOCX file using its path
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_path)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(file_path)
        else:
            text = file.read().decode("utf-8")

        # Perform summarization on the extracted text
        summary = abstractive_summary(text)
        if not summary:
            return "File not supported"
        
        return render_template('summary.html', summary=summary)

    else:
        return "File type not supported"

if __name__ == '__main__':
    app.run(debug=True)
