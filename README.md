<img src="banner.gif" width="100%" alt="Ducktcha Demo Banner">


# Ducktcha

Simple animated GIF captcha for Python. Copy the `ducktcha` folder into your project and use it.

## Install

```bash
pip install -r ducktcha/requirements.txt
```

## Usage

`ducktcha/app.py` already has a working Flask app with two routes:

- `GET /api/captcha/new` → returns the captcha gif + a token in the `X-Captcha-Token` header
- `POST /api/captcha/verify` → send `{"token": "...", "code": "..."}`, get back `{"valid": true/false}`

Just import that `app` into your own project instead of rebuilding it:

```python
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ducktcha'))

from ducktcha.app import app

# add your own routes here if needed
# app.route('/')...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

That's it, the captcha routes are already live.

## Using the engine directly (no Flask)

If you're not using Flask, or want more control:

```python
import uuid
from captcha import CaptchaGenerator
from store import MemoryStore

engine = CaptchaGenerator()
db = MemoryStore()

# generate
token = str(uuid.uuid4())
code, img_bytes = engine.create_image()
db.save(token, code)
# send img_bytes (gif) and token to the user

# verify
is_correct = db.validate(token, user_code)
```

