from flask import Flask, request, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def form():
    return render_template_string(open("form.html").read())

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name'].upper()
    year = request.form['year']

    image = Image.open("certificate_template.png")
    draw = ImageDraw.Draw(image)

    try:
        font_name = ImageFont.truetype("LibreBaskerville-Regular.ttf", 90)
        font_year = ImageFont.truetype("OpenSans_Condensed-LightItalic.ttf", 28)
    except:
        font_name = ImageFont.load_default()
        font_year = ImageFont.load_default()

    draw.text((image.width//2, 1120), name, fill="black", font=font_name, anchor="mm")
    sentence = f"for successfully completing the academic year {year} at Global English School"
    draw.text((image.width//2, 1235), sentence, fill="black", font=font_year, anchor="mm")

    buffer = BytesIO()
    image.save(buffer, format="PDF")
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name=f"{name}_certificate.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
