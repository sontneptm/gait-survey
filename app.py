from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', subject="hi")

if __name__ == '__main__':
    app.run('192.168.0.45', port = 5001, debug=True)