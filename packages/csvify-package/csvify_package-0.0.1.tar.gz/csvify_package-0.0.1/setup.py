from distutils.core import setup
setup(
  name = 'csvify_package',         
  packages = ['csvify_package'],
  version = '0.0.1',       
  license='MIT',        
  description = 'Small package that can import and export any file or python object, as CSV',   
  author = 'Philip Peters',                   
  author_email = '',      
  url = 'https://github.com/PhilipPeters/csvify_package',   
  download_url = 'https://github.com/PhilipPeters/csvify_package/archive/0.1.tar.gz',    
  keywords = ['csv', 'data', 'quick'],   
  install_requires=[           
          'pickle',
          'base64',
          'pandas',
          'csv'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
