from distutils.core import setup

setup(
	name='bci_lib',
	packages=['bci_lib', 'bci_lib/Stages', 'bci_lib/Stages/Classification', 'bci_lib/Stages/FeatureExtraction', 'bci_lib/Stages/LoadData', 'bci_lib/Stages/Preprocess'],
	version='0.0.9',
	license='MIT',
	description='A useful and easy to use tool for building bci pipelines.',
	author='Sahand Sadeghpour',
	author_email='sahand.2k.ss@gmail.com',
	url='https://github.com/SahandSadeghpour/bci_lib',
	download_url='https://github.com/SahandSadeghpour/bci_lib/archive/v0.0.9.tar.gz',
	keywords=['bci', 'pipelines', 'preprocessing', 'classification'],
	install_requires=[
		'mne~=0.20.4',
		'numpy~=1.18.4',
		'sklearn~=0.0',
		'scikit-learn~=0.23.2',
		'scipy~=1.4.1',
		'nptyping~=1.3.0',
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
	    'Topic :: Software Development :: Build Tools',
	    'License :: OSI Approved :: MIT License',
	    'Programming Language :: Python :: 3',
	    'Programming Language :: Python :: 3.4',
	    'Programming Language :: Python :: 3.5',
	    'Programming Language :: Python :: 3.6',
	],
)
