from distutils.core import setup
from MyHelloWorldKugan.consts import version, homepage

setup(
    name='MyHelloWorldKugan',  # How you named your package folder (MyHelloWorldKugan)
    packages=['MyHelloWorldKugan'],  # Chose the same as "name"
    version=version,  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='MyHelloWorldKugan for easy hello world',  # Give a short description about your library
    author='Sathiyakugan',  # Type in your name
    author_email='bsathiyakugan@gmail.com',  # Type in your E-Mail
    url=homepage,  # Provide either the link to your github or to your website
    download_url='https://github.com/Sathiyakugan/MyHelloWorld/archive/0.1.tar.gz',  # I explain this later on
    keywords=['Hello', 'Hello World', 'World'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    project_urls={
        'Documentation': 'https://github.com/Sathiyakugan/MyHelloWorld',
        'Commercial License': '',
        'Bug Tracker': '',
        'Source Code': '',
        'Blog': '',
        'Donate': '',
    }
)
