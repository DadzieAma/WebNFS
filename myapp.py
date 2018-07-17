from flask import Flask, render_template, request
from nfs import *


app = Flask( __name__ )

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/server')
def server():
    return render_template('server.html')

@app.route('/client')
def client():
    return render_template('client.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/selectip')
def selectip():
    ip=request.args.get('ip')
    file=request.args.get('file')
    set_server(ip,file)
    return render_template('susserver.html',ip=ip,file=file)

@app.route('/setClient')
def setClient():
    ip=request.args.get('ip')
    file=request.args.get('file')
    folder=request.args.get('folder')
    set_client(ip,file,folder)
    return render_template('susclient.html',ip=ip,file=file,folder=folder)

@app.route('/clientfolder', methods=['POST'])
def clientfolder():
    folder=request.args.get('folder')
    openfolder(str(folder))
    return render_template('index.html')

@app.route('/serverfolder', methods=['POST'])
def serverfolder():
    file=request.args.get('file')
    openfolder(str(file))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
