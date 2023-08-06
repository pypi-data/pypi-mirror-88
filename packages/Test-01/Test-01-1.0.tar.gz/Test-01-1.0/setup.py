from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 3 - Alpha',
  'Topic :: Scientific/Engineering :: Artificial Intelligence',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3',
]
 
setup(
  name='Test-01',
  packages=['Test'],
  version='1.0',
  
  description='Speed up your model making process. This will help you in selecting best features, best Models (SVM,SVR Random Fotest e.t.c and also in Data Preprocessing',
  download_url='https://github.com/SSudhashu/Test/archive/v01.0.tar.gz',
  url='https://github.com/SSudhashu/Test',  
  author='Sudhanshu Pandey',
  author_email='sudhanshu.dpandey@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['Machine Learning','Model','Regression','Classification','Automation','Data Preprocessing','Preprocessing','Feature Selection','Model Selection','SVM'], 

  install_requires=['pandas','numpy'] 
)