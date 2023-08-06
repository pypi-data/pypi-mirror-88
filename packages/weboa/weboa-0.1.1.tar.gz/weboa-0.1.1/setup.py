from setuptools import setup, find_packages
from os.path import join, dirname

__PACKAGE__='weboa'
__DESCRIPTION__='weboa is a cli tool to create templates for websites and preprocessors'
__VERSION__="0.1.1"

setup(
    name=__PACKAGE__,
    version=__VERSION__,
    packages=['weboa'],
    description=__DESCRIPTION__,
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author="lonagi",
    install_requires=["pillow"],
    author_email='lonagi22@gmail.com',
    url="https://github.com/lonagi/weboa",
    entry_points = {
              'console_scripts': [
                  'weboa = weboa.run:runcli',
              ],
          },
)