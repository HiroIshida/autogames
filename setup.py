from setuptools import setup, find_packages

__version__ = '0.0.1'

setup(
    name='autogames',
    version=__version__,
    packages=find_packages(),
    description="server and client programs for tictactoe",
    long_description=open('README.md').read(),
    url='https://github.com/HiroIshida/tictoctoe',
    author='Hiro Ishida & Naoya Yamaguchi',
    author_email='h-ishida@jsk.imi.i.u-tokyo.ac.jp & yamaguchi@jsk.imi.i.u-tokyo.ac.jp',
    license='MIT',
    install_requires=open('requirements.txt').readlines(),
    entry_points={'console_scripts':
                  ['autogames_server='
                   'autogames.server.server:main',
                   'autogames_client='
                   'autogames.client.python.client:main']},
)
