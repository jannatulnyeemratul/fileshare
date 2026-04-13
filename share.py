from flask import Flask, render_template, send_from_directory, request, redirect,url_for
from pathlib import Path
import os

app = Flask(__name__, static_url_path='/')
if not Path('./downloads').exists():
    os.mkdir('downloads')
filenames = os.listdir('./downloads')
messages = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'message' in request.form:
            messages.append(request.form['message'])
        elif 'file' in request.files:
            for file in request.files.getlist('file'):
                if file.filename != '':
                    file.save(Path.cwd()/'downloads'/file.filename)
                    filenames.append(file.filename)

    return render_template('home.html', filenames = filenames, messages = messages)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(directory='./downloads', path=filename, as_attachment=True)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    global filenames
    current_dir = Path.cwd() / 'downloads'
    for file in filenames:
        os.unlink(current_dir/file)
    filenames = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)