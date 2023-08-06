from setuptools import setup

setup(name='ks_ci',
      version='1.3.1',
      description='KS CI Bundle',
      long_description='CI scripts used in dev environment of the www.sarmacja.org community',
      author='Maciej Poleszczyk',
      author_email='mpoleszczyk@wp.pl',
      packages=['ks_ci'],
      license='MIT',
      url='https://github.com/poleszcz/ks-ci-bundle',
      python_requires='>=3',
      scripts=['bin/ks_ci_helper.py']
     )