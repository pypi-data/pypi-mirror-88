from distutils.core import setup
	
setup(
  packages = ['MAQTextSDK','MAQTextSDK.models'],  
  name = 'MAQTextSDK',         
  version = '1.0',      
  license='MIT', 
  description = 'NLP based text processing SDK',
  long_description="""**Text Analytics SDK**\n
  *MAQTextSDK* is a python package for natural language processing.\n
  This SDK can be used for extracting sentiment value from textual data.\n
  For usage related concerns please check https://github.com/maqsoftware/MAQTextAnalyticsSDK or contact support@maqsoftware.com\n
  """,
  author = 'MAQ',                  
  author_email = 'support@maqsoftware.com',    
  url = 'https://github.com/maqsoftware/MAQTextAnalyticsSDK',   
  download_url = 'https://github.com/maqsoftware/MAQTextAnalyticsSDK/archive/1.0.tar.gz',  
  keywords = ['NLP', 'Text', 'Sentiment'], 
  install_requires=[          
    'msrest'
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
