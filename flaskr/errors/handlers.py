from flask import Blueprint, jsonify, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return jsonify({
        'error': 404,
        'message': 'Not Found',
        'success': False
    }), 404


@errors.app_errorhandler(400)
def error_400(error):
    return jsonify({
        'error': 400,
        'message': 'Bad Request',
        'success': False
    }), 400


@errors.app_errorhandler(405)
def error_405(error):
    return jsonify({
        'error': 405,
        'message': 'Method Not Allowed',
        'success': False
    }), 405


@errors.app_errorhandler(422)
def error_422(error):
    return jsonify({
        'error': 422,
        'message': 'Unprocessable',
        'success': False
    }), 422
