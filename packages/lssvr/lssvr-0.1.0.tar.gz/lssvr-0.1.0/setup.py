# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lssvr']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.2,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'lssvr',
    'version': '0.1.0',
    'description': '',
    'long_description': "# lssvr\n\n`lssvr` is a Python module implementing the [Least Squares Support Vector Regression][1] using the scikit-learn as base.\n\n## instalation\nthe `lssvr` package is available in [PyPI](https://pypi.org/project/lssvr/). to install, simply type the following command:\n```\npip install lssvr\n```\nor using [Poetry](python-poetry.org/):\n```\npoetry add lssvr\n```\n\n## basic usage\n\nExample:\n\n```Python\nimport numpy as np\nfrom lssvr import LSSVR\n\nfrom sklearn.datasets import load_boston\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.metrics import mean_squared_error\n\n\nboston = load_boston()\n\nX_train, X_test, y_train, y_test = train_test_split(boston.data, boston.target, test_size=0.2)\n\nmodel = LSSVR(kernel='rbf', gamma=0.01)\nmodel.fit(X_train, y_train)\ny_hat = model.predict(X_test)\nprint('MSE', mean_squared_error(y_test, y_hat))\nprint('R2 Score',model.score(X_test, y_test))\n```\n\n\n## contributing\n\nthis project is open for contributions. here are some of the ways for you to contribute:\n\n - bug reports/fix\n - features requests\n - use-case demonstrations\n\nto make a contribution, just fork this repository, push the changes in your fork, open up an issue, and make a pull request!\n\n\n[1]: https://doi.org/10.1016/S0925-2312(01)00644-0",
    'author': 'José Alberth',
    'author_email': 'jalberth14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zealberth/lssvr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
