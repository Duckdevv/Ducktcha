import uuid
from captcha import CaptchaGenerator
from flask import Flask, jsonify, request, send_file
from store import MemoryStore

app = Flask(__name__)

engine = CaptchaGenerator()
db = MemoryStore()


@app.route('/api/captcha/new', methods=['GET'])
def get_captcha():
  token = str(uuid.uuid4())
  code, img_bytes = engine.create_image()

  db.save(token, code)

  res = send_file(img_bytes, mimetype='image/gif')
  res.headers['X-Captcha-Token'] = token
  return res


@app.route('/api/captcha/verify', methods=['POST'])
def check_captcha():
  payload = request.get_json() or {}
  token = payload.get('token')
  user_code = payload.get('code', '')

  if not token:
    return jsonify({'valid': False, 'error': 'Token missing'}), 400

  is_correct = db.validate(token, user_code)

  if is_correct:
    return jsonify({'valid': True})

  return jsonify({'valid': False, 'error': 'Invalid code'}), 400


if __name__ == '__main__':
  app.run(port=5000, debug=True)
