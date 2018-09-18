from setuptools import setup, find_packages

setup(name='disagree',
      version='0.1.3',
      author='Oliver Price',
      author_email='op.oliverprice@gmail.com',
      url='https://github.com/o-P-o/annotations',
      packages=['disagree', 'disagree.test'],
      include_package_data=True,
      scripts=['bin/plot_utils.py'],
      licence='LICENCE',
      description='Visual and statistical assessment of annotator agreements',
      long_description=open('README.md').read(),
      install_requires=[
        'scipy >= 1.1.0',
        'tqdm >= 4.26.0',
        'pandas >= 0.23.0',
        'matplotlib >= 2.2.3']
     )
