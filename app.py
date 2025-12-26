from flask import Flask, request, send_file
import fitz  # PyMuPDF
import os
import uuid
import subprocess
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_file(file):
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    return path

@app.route('/merge', methods=['POST'])
def merge_pdf():
    files = request.files.getlist('files')
    output = fitz.open()
    for f in files:
        path = save_file(f)
        doc = fitz.open(path)
        output.insert_pdf(doc)
    out_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_merged.pdf")
    output.save(out_path)
    return send_file(out_path, as_attachment=True)

@app.route('/split', methods=['POST'])
def split_pdf():
    file = request.files['file']
    path = save_file(file)
    doc = fitz.open(path)
    output = fitz.open()
    for page in doc:
        output.insert_pdf(doc, from_page=page.number, to_page=page.number)
    out_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_split.pdf")
    output.save(out_path)
    return send_file(out_path, as_attachment=True)

@app.route('/compress', methods=['POST'])
def compress_pdf():
    file = request.files['file']
    path = save_file(file)
    doc = fitz.open(path)
    for page in doc:
        page.set_rotation(0)
    out_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_compressed.pdf")
    doc.save(out_path, deflate=True)
    return send_file(out_path, as_attachment=True)

@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    file = request.files['file']
    path = save_file(file)
    subprocess.run([
        "libreoffice",
        "--headless",
        "--convert-to",
        "docx",
        path,
        "--outdir",
        UPLOAD_FOLDER
    ])
    docx_path = path.replace(".pdf", ".docx")
    return send_file(docx_path, as_attachment=True)

@app.route('/jpg-to-pdf', methods=['POST'])
def jpg_to_pdf():
    file = request.files['file']
    path = save_file(file)
    image = Image.open(path).convert("RGB")
    out_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
    image.save(out_path)
    return send_file(out_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
