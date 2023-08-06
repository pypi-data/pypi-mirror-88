import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'PtPclass',         # How you named your package folder (MyLib)
  packages = ['PtPclass'],   # Chose the same as "name"
  version = '0.0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'package practice to learn python OOP by PtP',   # Give a short description about your library
  long_description=DESCRIPTION,
  long_description_content_type = "text/markdown",
  author = 'PtP',                   # Type in your name
  author_email = 't1hc0msupp0rt@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Portuphet/PtPclass',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Portuphet/PtPclass/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['pratice python', 'OOP', 'Portuphet'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)