from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ConnectionValidation',
    version='0.4.7',
    description='Validad con un Dongle',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Wilbert Sanchez',
    author_email='wilbertenriquechable522@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Validador',
    packages=find_packages(),
    install_requires=['']
)