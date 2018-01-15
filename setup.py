from setuptools import setup

setup(name='pimaton',
      version='0.1',
      description='A photobooth app for raspberry pi',
      url='https://git.bacardi55.org/bacardi55/pimaton',
      author='bacardi55',
      author_email='bac@rdi55.pl',
      license='GPLv3',
      packages=['pimaton'],
      install_requires=[
          'picamera', 'six', 'pyyaml', 'pillow', 'pycups'
      ],
      zip_safe=False)
