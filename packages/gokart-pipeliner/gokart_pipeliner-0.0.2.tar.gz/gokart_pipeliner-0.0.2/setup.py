# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gokart_pipeliner']

package_data = \
{'': ['*']}

install_requires = \
['gokart']

setup_kwargs = {
    'name': 'gokart-pipeliner',
    'version': '0.0.2',
    'description': 'gokart pipeline',
    'long_description': "# gokart-pipeliner\ngokart pipeline project\n\n\n# Usage\n\nPlease show [SampleTask.py](https://github.com/vaaaaanquish/gokart-pipeliner/blob/main/examples/SampleTasks.py) or [Eaxmple.ipynb](https://github.com/vaaaaanquish/gokart-pipeliner/blob/main/examples/Example.ipynb)\n\n```python\nfrom gokart_pipeliner import GokartPipeliner\nfrom ExampleTasks import *\n\n# make pipeline\npreprocess = [TaskA, {'task_b': TaskB, 'task_c': TaskC}, TaskD]\nmodeling = preprocess + [TaskE, {'task_f': TaskF}, TaskF]\npredict = [{'model': modeling, 'task_a': TaskA}, TaskG]\n\n# instantiation (setting static params)\nparams = {'TaskA': {'param1':0.1, 'param2': 'sample'}, 'TaskD': {'param1': 'foo'}}\nconfig_path_list = ['./conf/param.ini']\ngp = GokartPipeliner(\n    params=params,\n    config_path_list=config_path_list)\n\n# run (setting dynamic params)\nrunning_params = {'TaskB': {'param1':'bar'}}\ngp.run(predict, params=running_params)\n```\n\ntask example\n```python\nclass Task(gokart.TaskOnKart):\n    foo = gokart.TaskInstanceParameter()\n\n    def run(self):\n        x = self.load('foo')\n        self.dump(x)\n```\n\n# Develop\n\n```\npip install poetry\npip install poetry-dynamic-versioning\n\n# poetry install\npoetry build\n# poetry lock\n```\n",
    'author': 'vaaaaanquish',
    'author_email': '6syun9@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vaaaaanquish/gokart-pipeliner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
