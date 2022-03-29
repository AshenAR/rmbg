
from flask import Flask, render_template,request,send_file
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "ashen"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp','jfif'])


@app.route('/')
def hello():
    return render_template('index.html')



@app.route('/success',methods= ["POST","GET"])
def success():
    if (request.files):
        file = request.files['file']
        print(file)
        basepath = os.path.dirname(__file__)
        filenames = secure_filename(file.filename)
        file.save(os.path.join("static", filenames))

        # img_path = os.path.join(app.config['UPLOAD_FOLDER'] , filename)
        img = file.filename
        print(img)
        from main import runner

        print(os.path.join("static", filenames))
        
       
        name= runner(os.path.join(basepath,"static", filenames))
        os.remove(os.path.join("static", filenames))

    return render_template("result.html")


@app.route('/download', methods=['GET', 'POST'])
def download():
    basepath = os.path.dirname(__file__)


    uploads = os.path.join("static","test.png")
    print(uploads)
    return send_file(uploads,as_attachment=True)




if __name__ == '__main__':
   app.run(debug = True)