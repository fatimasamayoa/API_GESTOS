from flask import jsonify
from Algorithm.translate import translate


def validation(content):
    if 'imageString' in content.keys():
        if content['imageString'] == '':
            return jsonify(result=''), 400
        palabra = translate(content['imageString'])
    if palabra == '':
        return jsonify(result='NOT_FOUND'), 404
    if palabra == 'NOT_HANDS':
        return jsonify(result=''), 400
    return jsonify(result=palabra), 200
