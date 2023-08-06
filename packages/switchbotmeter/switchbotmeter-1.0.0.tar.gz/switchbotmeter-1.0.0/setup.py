# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['switchbotmeter']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'switchbotmeter',
    'version': '1.0.0',
    'description': 'AsyncIO-compatible SwitchBot Meter library',
    'long_description': ".. image:: ./docs/switchbot.png\n\n**Python Swithbot Meter API**\n\nComprehensible [SwitchBot Meter](https://www.switch-bot.com/products/switchbot-meter) API.\nRead your SwitchBot Meter status in real time via BLE. \n\n|pypi| |release| |downloads| |python_versions| |pypi_versions| |coverage| |actions|\n\n.. |pypi| image:: https://img.shields.io/pypi/l/switchbotmeter\n.. |release| image:: https://img.shields.io/librariesio/release/pypi/switchbotmeter\n.. |downloads| image:: https://img.shields.io/pypi/dm/switchbotmeter\n.. |python_versions| image:: https://img.shields.io/pypi/pyversions/switchbotmeter\n.. |pypi_versions| image:: https://img.shields.io/pypi/v/switchbotmeter\n.. |coverage| image:: https://codecov.io/gh/XayOn/switchbotmeter/branch/develop/graph/badge.svg\n    :target: https://codecov.io/gh/XayOn/switchbotmeter\n.. |actions| image:: https://github.com/XayOn/switchbotmeter/workflows/CI%20commit/badge.svg\n    :target: https://github.com/XayOn/switchbotmeter/actions\n\nInstallation\n------------\n\nThis library is available on `Pypi <https://pypi.org/project/switchbotmeter/>`_, you can install it directly with pip::\n\n        pip install switchbotmeter\n\nThis library acts as a BLE client, so you need a\nBLE-capable device (a bluetooth dongle or integrated)\n\nUsage\n-----\n\nThis library exports a DeviceScanner object that will\ndected any SwitchBot Meter devices nearby. \nNote that you need to have permissions to access your\nbluetooth device, the scope of wich will not be covered by\nthis readme :\n\n.. code:: python\n\n    from switchbotmeter import DevScanner\n\n    for current_devices in DevScanner(): \n        for device in current_devices:\n            print(device)\n            print(f'{device.mac} -> {device.temp}')\n\n\n.. code:: bash\n\n    <T temp: 19.8 humidity: 73> (c6:97:89:d6:c8:09)\n    c6:97:89:d6:c8:09 -> 19.8\n    ...\n    <T temp: 20.4 humidity: 71> (c6:97:89:d6:c8:09)\n    c6:97:89:d6:c8:09 -> 20.4\n",
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
