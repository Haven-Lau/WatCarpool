from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print request.form.get('first')
        print request.form.get('second')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8000)
    