from distutils.core import setup
setup(
  name = 'apollo_ad',
  packages = ['apollo_ad'], 
  version = '0.0.2',
  license='MIT',
  description = 'Auto Differentiation Tools',
  author = 'Connor Capitolo, Haoxin Li, Kexin Huang, Chen Zhang',
  author_email = 'cosamhkx@gmail.com', 
  url = 'https://github.com/West-Coast-Quaranteam/cs107-FinalProject',
  keywords = ['Auto-diff'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pytest',
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