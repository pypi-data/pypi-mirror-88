# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recap']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0', 'yacs>=0.1.8,<0.2.0']

setup_kwargs = {
    'name': 'recap',
    'version': '0.1.3',
    'description': 'Reproducible configurations for any project',
    'long_description': '# recap\n\n![build](https://github.com/georgw777/recap/workflows/build/badge.svg)\n\n_recap_ is a tool for providing _REproducible Configurations for Any Project_.\n\nResearch should be reproducible.\nEspecially in deep learning, it is important to keep track of hyperparameters and configurations used in experiments.\nThis package aims at making that easier.\n\n## Installing\n\nJust install like any Python package:\n\n```bash\npip install recap\n```\n\n## Overview\n\nRecap provides two top-level concepts that would be imported as follows:\n\n```python\nfrom recap import URI, CfgNode as CN\n```\n\nThe `CfgNode` is a subclass of [yacs](https://github.com/rbgirshick/yacs)\' `CfgNode`.\nIt provides some additional features for parsing configurations that are inherited between files which is not possible with yacs.\n\nRecap\'s `URI` class provides a mechanism for handling logical paths within your project more conveniently with an interface that is fully compatible with `pathlib.Path`.\n\n## YAML configurations\n\nConfigurations are defined [just like in yacs](https://github.com/rbgirshick/yacs#usage), except that you need to import the `CfgNode` class from the recap package instead of yacs.\nConsider the following YAML configuration that sets default values for all configuration options we will use in our project. We shall name it `_base.yaml` because our experiments will build on these values.\n\n```yaml\nSYSTEM:\n  NUM_GPUS: 4\n  NUM_WORKERS: 2\nTRAIN:\n  LEARNING_RATE: 0.001\n  BATCH_SIZE: 32\n  SOME_OTHER_HYPERPARAMETER: 10\n```\n\nThe equivalent configuration can be obtained programatically like so:\n\n```python\nfrom recap import CfgNode as CN\n\ncfg = CN()\ncfg.SYSTEM = CN()\ncfg.SYSTEM.NUM_GPUS = 4\ncfg.SYSTEM.NUM_WORKERS = 2\ncfg.TRAIN = CN()\ncfg.TRAIN.LEARNING_RATE = 1e-3\ncfg.TRAIN.BATCH_SIZE = 32\ncfg.TRAIN.SOME_OTHER_HYPERPARAMETER = 10\n\nprint(cfg)\n```\n\n### Inheriting configurations\n\nRecap provides functionality for inheriting configuration options from other configuration files by setting the top-level `_BASE_` key.\nSo, we could create a configuration file `experiment_1.yaml` for an experiment where we try a different learning rate and batch size:\n\n```yaml\n_BASE_: _base.yaml\n\nTRAIN:\n  LEARNING_RATE: 1e-2\n  BATCH_SIZE: 64\n```\n\nIn our code, when we want to load the experiment configuration, we would use the `recap.CfgNode.load_yaml_with_base()` function:\n\n```python\nfrom recap import CfgNode as CN\n\ncfg = CN.load_yaml_with_base("experiment_1.yaml")\n\nprint(cfg)\n\n# Will output:\n"""\nSYSTEM:\n  NUM_GPUS: 4\n  NUM_WORKERS: 2\nTRAIN:\n  LEARNING_RATE: 0.01\n  BATCH_SIZE: 64\n  SOME_OTHER_HYPERPARAMETER: 10\n"""\n```\n\nNote that the `_BASE_` keys can be arbitrarily nested; however, circular references are prohibited.\n\n## Logical URIs and the path manager\n\nRecap includes a path manager for conveniently specifying paths to logical entities.\nThe path strings are set up like a URI where the scheme (i.e. `http` in the path string `http://google.com`) refers to a logical entity.\nEach such entity needs to be set up as a `PathTranslator` that can translate the logical URI path to a physical path on the file system.\n\nFor example, we could set up a path translator for the `data` scheme to refer to the the path of a dataset on our file system located at `/path/to/dataset`. Then the recap URI `data://train/abc.txt` would be translated to `/path/to/dataset/train/abc.txt`.\n\nThe simplest way of setting that up is using the `register_translator` function (although more complex setups are possible with the `recap.path_manager.PathTranslator` class, allowing you to download files from the internet, for example):\n\n```python\nfrom recap.path_manager import register_translator\nfrom pathlib import Path\n\nregister_translator("data", Path("/path/to/dataset"))\n```\n\nThen, we can use the `recap.URI` class just like any `pathlib.Path` object:\n\n```python\nfrom recap import URI\n\nmy_uri = URI("data://train/abc.txt")\n# Here, str(my_uri) == "/path/to/dataset/train/abc.txt"\n\nwith my_uri.open("r") as f:\n    print(f.read())\n```\n\n### Logical URIs in inherited configurations\n\nThe `recap.URI` interface is fully compatible with the nested configurations.\nThis means that you can use recap `URI`s within the `_BASE_` field for inheriting configurations.\n\nFor example, you could register a path translator for the `config` scheme and then include `_BASE_: config://_base.yaml` in your configuration files.\n',
    'author': 'Georg Wölflein',
    'author_email': 'georgw7777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/georgw777/recap',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
