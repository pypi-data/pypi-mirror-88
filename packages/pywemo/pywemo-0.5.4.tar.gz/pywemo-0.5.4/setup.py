# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pywemo',
 'pywemo.ouimeaux_device',
 'pywemo.ouimeaux_device.api',
 'pywemo.ouimeaux_device.api.xsd']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.0', 'requests>=2.0', 'six>=1.10.0']

setup_kwargs = {
    'name': 'pywemo',
    'version': '0.5.4',
    'description': 'Lightweight Python module to discover and control WeMo devices',
    'long_description': 'pyWeMo |Build Badge| |PyPI Version Badge| |PyPI Downloads Badge|\n================================================================\nLightweight Python 2 and Python 3 module to discover and control WeMo devices.\n\nThis is a stripped down version of the Python API for WeMo devices, `ouimeaux <https://github.com/iancmcc/ouimeaux>`_, with simpler dependencies.\n\nDependencies\n------------\npyWeMo depends on Python packages: requests, ifaddr and six\n\nHow to use\n----------\n\n.. code-block:: python\n\n    >>> import pywemo\n    >>> devices = pywemo.discover_devices()\n    >>> print(devices)\n    [<WeMo Insight "AC Insight">]\n\n    >> devices[0].toggle()\n\nIf discovery doesn\'t work on your network\n-----------------------------------------\nOn some networks discovery doesn\'t work reliably, in that case if you can find the ip address of your Wemo device you can use the following code.\n\n.. code-block:: python\n\n    >>> import pywemo\n    >>> url = pywemo.setup_url_for_address("192.168.1.192", None)\n    >>> print(url)\n    http://192.168.1.192:49153/setup.xml\n    >>> device = pywemo.discovery.device_from_description(url, None)\n    >>> print(device)\n    <WeMo Maker "Hi Fi Systemline Sensor">\n\nPlease note that `discovery.device_from_description` call requires a `url` with an IP address, rather than a hostnames. This is needed for the subscription update logic to work properly. In addition recent versions of the WeMo firmware may not accept connections from hostnames, and will return a 500 error.\n\nThe `setup_url_for_address` function will lookup a hostname and provide a suitable `url` with an IP address.\n\nDevice Reset and Setup\n----------------------\npywemo includes the ability to reset and setup devices, without using the Belkin app or needing to create a Belkin account.\nThis can be particularly useful if the intended use is fully local control, such as using Home Assistant.\n\nReset can be performed with the `reset` method, which has 2 boolean input arguments, `data` and `wifi`.\nSetting `data=True` will reset data ("Clear Personalized Info" in the Wemo app), which resets the device name and clears the icon and rules.\nSetting `wifi=True` will clear wifi information ("Change Wi-Fi" in the Wemo app), which does not clear the rules, name, etc.\nSetting both to true is equivalent to a "Factory Restore" from the app.\nIt should also be noted that devices contain a hardware reset procedure as well, so using the software is for convenience or if physical access is not available.\n\nDevice setup is through the `setup` method.\nThe user must first connect to the devices locally broadcast access point, then discover the device there.\nOnce done, pass the desired SSID and password (AES encryption only) to the `setup` method to connect it to your wifi network.\n\nImportant Note for Device Setup - OpenSSL is Required!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nOpenSSL is used to encrypt the password by the pywemo library.\nIt must be installed and available on the path via calling `openssl` with a terminal (or command prompt, if on Windows).\nThis is not required if connecting the device to an open network, since that requires no password, although an open network certainly isn\'t recommended.\n\nFirmware Warning\n----------------\nStarting in May of 2020, Belkin started requiring users to create an account and login to the app (Android app version 1.25).\nIn addition to the account, most of the app functionality now requires a connection to the cloud (internet access), even for simple actions such as toggling a switch.\nAll of the commands that go through the cloud are encrypted and cannot be easily inspected.\nThis raises the possibility that Belkin could, in the future, update Wemo device firmware and make breaking API changes that can not longer be deciphered.\nIf this happens, pywemo may no longer function on that device.\nIt would be prudent to upgrade firmware cautiously and preferably only after confirming that breaking API changes have not been introduced.\n\nDeveloping\n----------\nSetup and builds are fully automated. You can run build pipeline locally by running.\n\n.. code-block::\n\n    # Setup, build, lint and test the code:\n\n    ./scripts/build.sh\n\nLicense\n-------\nThe code in pywemo/ouimeaux_device is written and copyright by Ian McCracken and released under the BSD license. The rest is released under the MIT license.\n\n.. |Build Badge| image:: https://travis-ci.org/pavoni/pywemo.svg?branch=master\n   :target: https://travis-ci.org/pavoni/pywemo\n   :alt: Status of latest Travis CI build\n.. |PyPI Version Badge| image:: https://pypip.in/v/pywemo/badge.png\n    :target: https://pypi.org/project/pywemo/\n    :alt: Latest PyPI version\n.. |PyPI Downloads Badge| image:: https://pypip.in/d/pywemo/badge.png\n    :target: https://pypi.org/project/pywemo/\n    :alt: Number of PyPI downloads\n',
    'author': 'Greg Dowling',
    'author_email': 'mail@gregdowling.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pavoni/pywemo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
