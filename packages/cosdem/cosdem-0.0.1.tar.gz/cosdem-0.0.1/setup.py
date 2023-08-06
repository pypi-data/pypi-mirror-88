from setuptools import setup, find_packages
import os

basepath = os.path.realpath(__file__)
basepath = os.path.dirname(basepath)
path = os.path.join(basepath, 'README.md')

with open(path, 'r') as file:
	README = file.read()

setup(	name='cosdem',
		version="0.0.1",
		description='Comparing Statistical Differences of Measurements',
		url='http://github.com/yigitsener/cosdem_project',
		author='Yiğit Şener',
		author_email='dataevreni@gmail.com',
		license='MIT',
		packages=find_packages(),
		install_requires=[
					'matplotlib==3.3.3',
					'numpy==1.19.4',
					'pandas==1.1.4',
					'scipy==1.5.4',
					'xlrd==1.2.0',
					'XlsxWriter==1.3.7',
				],
		classifiers = [
					"Programming Language :: Python",
					"Programming Language :: Python :: 3.6",
					"Programming Language :: Python :: 3.7",
					"Programming Language :: Python :: 3.8",
					"Intended Audience :: Science/Research",
					"License :: OSI Approved :: MIT License",
					"Operating System :: OS Independent",
					"Topic :: Scientific/Engineering :: Information Analysis",
					"Topic :: Scientific/Engineering :: Visualization",
				],
		keywords=[
			'Statistical Difference Tests', 't test', 'regression', 'correlation', 'mann wihtney u test',
			'Homogeneity Tests', 'Normality Test', 'Descriptive Statistics', 'bland altman plot', 'violin plot'
		  ],
		python_requires='>=3.6.*',
		long_description_content_type='text/markdown',
		long_description = README,
		documentation='http://github.com/yigitsener/cosdem_project',
		include_package_data=True,
		zip_safe=True
		)
