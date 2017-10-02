try:
	from setuptools import setup
except:
	from distutils.core import setup


setup(name='task', version='1.0.0', author='na',
      author_email='na@na',
      url="na",
      packages=['task', 'task.api', 'tast.data_interface', 'tast.model'],
      install_requires=['pandas', 'numpy'],
      description='na',
      license='--',  classifiers=['na'],
      )

