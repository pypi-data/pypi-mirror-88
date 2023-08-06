# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discord_interactions']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'discord-interactions',
    'version': '0.1.0',
    'description': 'Useful tools for using the Discord Interactions API',
    'long_description': "discord-interactions-python\n---\n\nTypes and helper functions for Discord Interactions webhooks.\n\n# Installation\n\n```\npip install discord-interactions\n```\n\nRequires Python 3.6+\n\n# Usage\n\nUse the `InteractionType` and `InteractionResponseType` enums to process and respond to webhooks.\n\nUse `verify_key` to check a request signature.\n\nUse `verify_key_decorator` to protect routes in a Flask app.\n\n```py\nimport os\n\nfrom flask import Flask, request, jsonify\n\nfrom discord_interactions import verify_key_decorator, InteractionType\n\nCLIENT_PUBLIC_KEY = os.getenv('CLIENT_PUBLIC_KEY')\n\napp = Flask(__name__)\n\n@app.route('/interactions', methods=['POST'])\n@verify_key_decorator(CLIENT_PUBLIC_KEY)\ndef interactions():\n  if request.json['type'] == InteractionType.APPLICATION_COMMAND:\n    return jsonify({\n        'type': InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,\n        'data': {\n            'content': 'Hello world'\n        }\n    })\n```\n\n# Exports\n\nThis module exports the following:\n\n### InteractionType\n\nAn enum of interaction types that can be POSTed to your webhook endpoint.\n\n### InteractionResponseType\n\nAn enum of response types you may provide in reply to Discord's webhook.\n\n### InteractionResponseFlags\n\nAn enum of flags you can set on your response data.\n\n### verify_key(raw_body: str, signature: str, timestamp: str, client_public_key: str) -> bool:\n\nVerify a signed payload POSTed to your webhook endpoint.\n\n### verify_key_decorator(client_public_key: str)\n\nFlask decorator that will verify request signatures and handle PING/PONG requests.\n",
    'author': 'Ian Webster',
    'author_email': 'ianw_pypi@ianww.com',
    'maintainer': 'Ian Webster',
    'maintainer_email': 'ianw_pypi@ianww.com',
    'url': 'https://github.com/discord/discord-interactions-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
