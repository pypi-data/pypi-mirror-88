# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['password_generator']
install_requires = \
['Flask-RESTful', 'marshmallow', 'webargs']

setup_kwargs = {
    'name': 'random-password-generator',
    'version': '2.1.2',
    'description': 'Simple and custom random password generator for python',
    'long_description': '# Random password Generator\n[![PyPI version](https://img.shields.io/badge/PYPI-V%202.1.0-blue.svg)](https://pypi.org/project/random-password-generator)\n[![Build Status](https://travis-ci.org/suryasr007/random-password-generator.svg?branch=master)](https://travis-ci.org/suryasr007/random-password-generator)\n[![Updates](https://pyup.io/repos/github/suryasr007/random-password-generator/shield.svg)](https://pyup.io/repos/github/suryasr007/random-password-generator/)\n\n##### A simple and custom random password generator.\n * Generate a simple password of default length 6-16.\n * Generate a password with custom properties.\n * Generate a password from given characters.\n * Generate Non Duplicate Password.\n * Available at https://random-pg.herokuapp.com/\n\n## API (GET Request)\n * Base_url: https://random-pg.herokuapp.com\n * Generate simple password ```/api/generate```\n   * Optional Attributes can be provided as params  \n     eg: \n     ```\n      /api/generate?minlen=16  \n      /api/generate?minlen=16&minlchars=5\n     ```\n * Generate a custom password from givin characters\n   * Mandatory attributes can be provided as params  \n     eg: \n     ```\n      /api/shuffle?password=sdjbfbfB&maxlen=14\n     ```\n * Generate a non duplicate password.  \n   * Mandatory Attribute \'maxlen\'  \n     eg:\n     ``` \n      /nonduplicate?maxlen=14\n     ```\n\n\n## Usage\n * Install the package.\n * Import the package.\n * Create an instance\n * Modify the default properties. (Optional)\n * Generate the password (Default length of password 6-16 unless specified via properties).\n\n``` bash\n  pip install random-password-generator\n```\n\n``` python\n  from password_generator import PasswordGenerator\n\n  pwo = PasswordGenerator()\n  pwo.generate()\n```\n\n\n## Configuration\n\n| property   |                          Description                 | Default |\n| ---------- |------------------------------------------------------| ------- |\n| minlen     |   Minimum length of the password                     | 6 |\n| maxlen     |   Maximum length of the password                     | 16 |\n| minuchars  |   Minimum upper case characters required in password | 1 |\n| minlchars  |   Minimum lower case characters required in password | 1 |\n| minnumbers |   Minimum numbers required in password               | 1 |\n| minschars  |   Minimum special characters in the password         | 1 |\n\n## Update V2.1.0\nApplication uses [secrets](https://docs.python.org/3/library/secrets.html) module instaed of `random` module **whenever** possible.\n\n\n## Update V2.0.1\nApplication is available at following link: https://random-pg.herokuapp.com/\n\n\n## Update V1.1.0\nFrom version 1.1.0, Characters can be excluded from the required password by setting the properties on PasswordGenerator object\n\nexample:\n``` python\n  pwo = PasswordGenerator()\n\n  pwo.excludeuchars = "ABCDEFTUVWXY" # (Optional)\n  pwo.excludelchars = "abcdefghijkl" # (Optional)\n  pwo.excludenumbers = "012345" # (Optional)\n  pwo.excludeschars = "!$%^" # (Optional)\n```\n\n\n## Generate a custom password\n``` python\n  pwo = PasswordGenerator()\n\n  # All properties are optional\n  pwo.minlen = 30 # (Optional)\n  pwo.maxlen = 30 # (Optional)\n  pwo.minuchars = 2 # (Optional)\n  pwo.minlchars = 3 # (Optional)\n  pwo.minnumbers = 1 # (Optional)\n  pwo.minschars = 1 # (Optional)\n\n  pwo.generate()\n```\n\n## Generate a password from given characters\n``` python\n  pwo = PasswordGenerator()\n\n  # It takes two arguments\n  # required characters and length of required password\n  pwo.shuffle_password(\'sdafasdf#@&^#&234u8\', 20)\n```\n\n## Generate Non Duplicate Password\n``` python\n  pwo = PasswordGenerator()\n\n  # length of required password\n  pwo.non_duplicate_password(20)\n```\n\n## Contributions\nContributions are welcomed via PR.\n\n## License\n * [MIT](LICENSE)\n',
    'author': 'Surya Teja',
    'author_email': '94suryateja@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/suryasr007/random-password-generator',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
