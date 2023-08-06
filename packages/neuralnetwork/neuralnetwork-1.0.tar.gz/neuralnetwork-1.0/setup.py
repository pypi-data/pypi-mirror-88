from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'neuralnetwork',         # How you named your package folder (MyLib)
  packages = ['neuralnetwork'],   # Chose the same as "name"
  version = 'v1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Artificial Neural Network',   # Give a short description about your library
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'Stephen OShea',                   # Type in your name
  author_email = 'stephenlmoshea@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/stephenlmoshea/python-neuralnetwork',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/stephenlmoshea/python-neuralnetwork/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['NEURAL NETWORK', 'BACKPROPAGATION', 'GRADIENT DESCENT', 'SIGMOID', 'HYPERBOLIC TANGENT'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
