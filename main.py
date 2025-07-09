from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/')
def form():
    # Serve the form.html content
    try:
        with open("form.html", "r", encoding="utf-8") as f:
            return render_template_string(f.read())
    except FileNotFoundError:
        return "form.html not found", 404

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name'].upper()
    year = request.form['year']

    # Load certificate background
    try:
        image = Image.open("certificate_template.png")
    except FileNotFoundError:
        return "Template image not found", 404

    draw = ImageDraw.Draw(image)

    # Load fonts or fallback
    try:
        font_name = ImageFont.truetype("LibreBaskerville-Regular.ttf", 94)
        font_year = ImageFont.truetype("OpenSans_Condensed-LightItalic.ttf", 35)
    except:
        font_name = ImageFont.load_default()
        font_year = ImageFont.load_default()

    # Draw the name and academic year
    draw.text((image.width // 2, 1120), name, fill="black", font=font_name, anchor="mm")
    sentence = f"for successfully completing the academic year {year} at Global English School"
    draw.text((image.width // 2, 1235), sentence, fill="black", font=font_year, anchor="mm")

    # Save image to a PDF in memory
    buffer = BytesIO()
    image.save(buffer, format="PDF")
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{name}_certificate.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    # Use port=10000 only for Render or other cloud hosts
    app.run(host="0.0.0.0", port=10000)
