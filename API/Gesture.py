from Command.middle import validation
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/api/gesture', methods=['POST'])
def ejemplo5():
    if request.method == 'POST':
        content = request.get_json(force=True)
        return validation(content)


if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True,
            port=8089)
