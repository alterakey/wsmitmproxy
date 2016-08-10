import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = []

setup(
  name='wsproxy',
  version='0.0.1',
  description='Intercepting Proxy for WebSockets',
  long_description=README,
  classifiers=[
    "Programming Language :: Python",
  ],
  author='Takahiro Yoshimura',
  author_email='altakey@gmail.com',
  url='https://github.com/taky/wsmitmproxy',
  keywords='websocket html5 security pentest hacking',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires = requires,
  entry_points = {'console_scripts':['wsproxy = wsproxy.shell:shell']}
)
