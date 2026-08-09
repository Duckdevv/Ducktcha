![Ducktcha Demo](banner.gif)

#Ducktcha

​simple animated gif captcha for python. just copy ducktcha folder into your project and use it.
​install requirements first:
pip install -r ducktcha/requirements.txt
​how it works:
ducktcha/app.py has a working flask app with 2 routes. GET /api/captcha/new returns the captcha gif with token in X-Captcha-Token header, and POST /api/captcha/verify takes token and code then returns if valid or not.
​
you can just import app into your project like this:
​
import sys
```import os
​sys.path.append(os.path.join(os.path.dirname(file), 'ducktcha'))
​from ducktcha.app import app
​if name == 'main':
   app.run(host='0.0.0.0', port=5000, debug=True)```

​if you dont use flask or want direct control use the engine directly:

```​import uuid
from captcha import CaptchaGenerator
from store import MemoryStore
​engine = CaptchaGenerator()
db = MemoryStore()
​token = str(uuid.uuid4())
code, img_bytes = engine.create_image()
db.save(token, code)
​is_correct = db.validate(token, user_code)```
