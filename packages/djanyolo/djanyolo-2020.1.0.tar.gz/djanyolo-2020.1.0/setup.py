import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.txt')).read()

version = '2020.1.0'

install_requires = [
    "asgiref==3.2.5",
    "autocorrect==0.4.4",
    "Django>=2.0.7",
    "opencv-python==4.2.0.32",
    "pytz==2019.3",
    "sqlparse==0.3.1"
]

setup(name='djanyolo',
      version=version,
      description="Manage content for YOLO model.",
      long_description=README + '\n\n' + NEWS,
      classifiers=[
      ],
      keywords='yolo, djanyolo, django',
      author='RoboMx Team',
      author_email='ask@robomx.tech',
      url='https://robomx.com',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'}, include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points={
          'console_scripts':
              ['djanyolo=djanyolo:main']
      }
      )
