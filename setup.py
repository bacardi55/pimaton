from setuptools import setup

setup(name='pimaton',
      version='0.0.3',
      description='A photobooth application for raspberry pi',
      url='https://github.com/bacardi55/pimaton',
      download_url='https://github.com/bacardi55/pimaton/archive/v0.0.3.tar.gz',
      author='bacardi55',
      author_email='bac@rdi55.pl',
      license='GPLv3',
      packages=['pimaton'],
      install_requires=[
          'picamera', 'six', 'pyyaml', 'pillow', 'pycups'
      ],
      keywords = 'photobooth raspberrypi picamera',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7'
      ],
      entry_points = {
          'console_scripts': ['pimaton=pimaton:main']
      },
      include_package_data=True,
      zip_safe=False)
