# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['huey_monitor',
 'huey_monitor.migrations',
 'huey_monitor_tests',
 'huey_monitor_tests.test_app',
 'huey_monitor_tests.test_app.management',
 'huey_monitor_tests.test_app.management.commands',
 'huey_monitor_tests.test_project',
 'huey_monitor_tests.test_project.settings',
 'huey_monitor_tests.tests']

package_data = \
{'': ['*'], 'huey_monitor': ['templates/admin/huey_monitor/taskmodel/*']}

install_requires = \
['bx_py_utils==0.0.4',
 'django-debug-toolbar',
 'django-redis',
 'django>=2.2.0,<2.3.0',
 'huey']

entry_points = \
{'console_scripts': ['publish = '
                     'huey_monitor_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'django-huey-monitor',
    'version': '0.0.1rc1',
    'description': 'Django based tool for monitoring huey task queue: https://github.com/coleifer/huey',
    'long_description': '# django-huey-monitor\n\nDjango based tool for monitoring huey task queue: https://github.com/coleifer/huey\n\n\nProject state: planing/pre-alpha ;)\n\n\n## developing\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/django-huey-monitor.git\n~$ cd django-huey-monitor\n~/django-huey-monitor$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry via pip\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\ntox-py36             Run pytest via tox with *python v3.6*\ntox-py37             Run pytest via tox with *python v3.7*\ntox-py38             Run pytest via tox with *python v3.8*\ntox-py39             Run pytest via tox with *python v3.9*\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nmakemessages         Make and compile locales message files\nstart-dev-server     Start Django dev. server with the test project\nclean                Remove created files from the test project (e.g.: SQlite, static files)\nbuild                Update/Build docker services\nup                   Start docker containers\ndown                 Stop all containers\nlogs                 Display and follow docker logs\n```\n\n\n## License\n\n[GPL](LICENSE). Patches welcome!\n',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
