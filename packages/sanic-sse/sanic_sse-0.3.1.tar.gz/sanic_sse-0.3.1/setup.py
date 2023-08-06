# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sanic_sse']

package_data = \
{'': ['*']}

install_requires = \
['sanic']

setup_kwargs = {
    'name': 'sanic-sse',
    'version': '0.3.1',
    'description': 'Sanic Server-Sent Events extension',
    'long_description': '# Sanic Server-Sent Events extension\n\n![Publish](https://github.com/inn0kenty/sanic_sse/workflows/Publish/badge.svg)\n\nA Sanic extension for HTML5 [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) support, inspired by [flask-sse](https://github.com/singingwolfboy/flask-sse) and [aiohttp-sse](https://github.com/aio-libs/aiohttp-sse).\n\n## Install\n\nInstallation process as simple as:\n\n```bash\n$ pip install sanic_sse\n```\n\n## Example\n\nServer example:\n\n```python\nfrom http import HTTPStatus\nfrom sanic import Sanic\nfrom sanic.response import json, json_dumps\nfrom sanic.exceptions import abort\nfrom sanic_sse import Sse\n\n# This function is optional callback before sse request\n# You can use it for authorization purpose or something else\nasync def before_sse_request(request):\n    if request.headers.get("Auth", "") != "some_token":\n        abort(HTTPStatus.UNAUTHORIZED, "Bad auth token")\n\n\nsanic_app = Sanic()\n\n# The default sse url is /sse but you can set it via init argument url.\nSse(\n    sanic_app, url="/events", before_request_func=before_sse_request\n)  # or you can use init_app method\n\n\n@sanic_app.route("/send", methods=["POST"])\nasync def send_event(request):\n    # if channel_id is None than event will be send to all subscribers\n    channel_id = request.json.get("channel_id")\n\n    # optional arguments: event_id - str, event - str, retry - int\n    # data should always be str\n    try:\n        await request.app.sse_send(json_dumps(request.json), channel_id=channel_id)\n    except KeyError:\n        abort(HTTPStatus.NOT_FOUND, "channel not found")\n\n    return json({"status": "ok"})\n\n\nif __name__ == "__main__":\n    sanic_app.run(host="0.0.0.0", port=8000)\n```\n\nClient example (powered by [sseclient-py](https://github.com/mpetazzoni/sseclient) and [requests](https://github.com/requests/requests)):\n\n```python\nimport json\nimport pprint\nimport requests\nimport sseclient\n\nurl = "http://127.0.0.1:8000/events"\n# you may set channel_id parameter to receive special events\n# url = "http://127.0.0.1:8000/events?channel_id=foo"\n\nresponse = requests.get(url, stream=True)\nclient = sseclient.SSEClient(response)\nfor event in client.events():\n    print(event.id)\n    print(event.event)\n    print(event.retry)\n    pprint.pprint(json.loads(event.data))\n```\n\n## Requirements\n\n- [python](https://www.python.org/) 3.5+\n- [sanic](https://github.com/channelcat/sanic) 0.7.0+\n',
    'author': 'Innokenty Lebedev',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inn0kenty/sanic_sse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
