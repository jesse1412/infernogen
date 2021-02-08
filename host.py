from flask import Flask, send_file
from back_end import create_image
import io

app = Flask(__name__)

@app.route('/<wave>')
def get_image(wave):
    img = create_image(int(wave))
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    del img
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')
