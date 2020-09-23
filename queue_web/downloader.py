import tkinter as tk
from tkinter import filedialog
from flask import Flask, send_file, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = r'C:\Users\BZMBN4\Desktop'


@app.route('/download')
def download():
    return send_file(file_path, as_attachment=True)
    # return send_from_directory(r"C:\Users\BZMBN4\Desktop", filename="ParaView-5.8.1-Windows-Python3.7-msvc2015-64bit.zip", as_attachment=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename()
    print(file_path)
    root.destroy()
    app.run(debug=True, host='0.0.0.0', port='8888', use_reloader=False)


