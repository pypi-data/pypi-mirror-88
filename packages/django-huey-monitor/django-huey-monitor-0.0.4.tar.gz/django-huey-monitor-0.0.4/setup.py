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
{'': ['*'],
 'huey_monitor': ['locale/de/LC_MESSAGES/*',
                  'locale/en/LC_MESSAGES/*',
                  'templates/admin/huey_monitor/taskmodel/*']}

install_requires = \
['bx_py_utils', 'django', 'huey']

entry_points = \
{'console_scripts': ['publish = '
                     'huey_monitor_tests.test_project.publish:publish']}

setup_kwargs = {
    'name': 'django-huey-monitor',
    'version': '0.0.4',
    'description': 'Django based tool for monitoring huey task queue: https://github.com/coleifer/huey',
    'long_description': '# django-huey-monitor\n\nDjango based tool for monitoring [huey task queue](https://github.com/coleifer/huey)\n\nCurrent implementation will just store all Huey task signals into the database\nand display them in the Django admin.\n\n\n## Quickstart\n\n```bash\npip install django-huey-monitor\n```\n\n```python\nINSTALLED_APPS = [\n    #...\n    \'huey_monitor\',\n    #...\n]\n```\n\n\n# Screenshots\n\n### 2020-12-16-v002-change-list.png\n\n![2020-12-16-v002-change-list.png](https://raw.githubusercontent.com/boxine/django-huey-monitor/gh-pages/2020-12-16-v002-change-list.png)\n\n### 2020-12-16-v002-task-details1.png\n\n![2020-12-16-v002-task-details1.png](https://raw.githubusercontent.com/boxine/django-huey-monitor/gh-pages/2020-12-16-v002-task-details1.png)\n\n### 2020-12-16-v002-task-details2.png\n\n![2020-12-16-v002-task-details2.png](https://raw.githubusercontent.com/boxine/django-huey-monitor/gh-pages/2020-12-16-v002-task-details2.png)\n\n\n\n## developing\n\n* install docker\n* clone the project\n* start the container\n\nTo start developing e.g.:\n\n```bash\n~$ git clone https://github.com/boxine/django-huey-monitor.git\n~$ cd django-huey-monitor\n~/django-huey-monitor$ make\nhelp                 List all commands\ninstall-poetry       install or update poetry via pip\ninstall              install via poetry\nupdate               Update the dependencies as according to the pyproject.toml file\nlint                 Run code formatters and linter\nfix-code-style       Fix code formatting\ntox-listenvs         List all tox test environments\ntox                  Run pytest via tox with all environments\npytest               Run pytest\npytest-ci            Run pytest with CI settings\npublish              Release new version to PyPi\nmakemessages         Make and compile locales message files\nclean                Remove created files from the test project (e.g.: SQlite, static files)\nbuild                Update/Build docker services\nup                   Start docker containers\ndown                 Stop all containers\nshell_django         go into a interactive bash shell in Django container\nshell_huey           go into a interactive bash shell in Huey worker container\nlogs                 Display and follow docker logs\nreload_django        Reload the Django dev server\nreload_huey          Reload the Huey worker\nrestart              Restart the containers\nfire_test_tasks      Call "fire_test_tasks" manage command to create some Huey Tasks\n\n~/django-huey-monitor$ make install-poetry\n~/django-huey-monitor$ make install\n~/django-huey-monitor$ make up\n```\n\n\nIt\'s also possible to run the test setup with SQLite and Huey immediate setup\nwithout docker:\n\n```bash\n~$ git clone https://github.com/boxine/django-huey-monitor.git\n~$ cd django-huey-monitor\n~/django-huey-monitor$ ./manage.sh run_testserver\n```\n\n\n## License\n\n[GPL](LICENSE). Patches welcome!\n\n\n## Links\n\n* https://pypi.org/project/django-huey-monitor/\n',
    'author': 'JensDiemer',
    'author_email': 'git@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/boxine/django-huey-monitor/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
