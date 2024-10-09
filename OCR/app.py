from flask import Flask, render_template, request, redirect, url_for
import pytesseract
from PIL import Image
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Assure-toi que le chemin de Tesseract est correctement configuré
# Pour Windows, spécifie le chemin du fichier exécutif de Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Enregistrer l'image dans le dossier uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Effectuer l'OCR sur l'image
        text = pytesseract.image_to_string(Image.open(filepath))
        
        # Retourner le texte extrait à la page web
        return f"<h1>Texte extrait :</h1><p>{text}</p>"

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=55000)
