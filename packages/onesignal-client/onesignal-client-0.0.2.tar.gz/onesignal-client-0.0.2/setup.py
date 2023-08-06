import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='onesignal-client',
    version='0.0.2',
    url='https://github.com/radimsuckr/onesignal-client',
    description='OneSignal API wrapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Radim Sückr',
    author_email='contact@radimsuckr.cz',
    packages=['onesignal'],
    install_requires=['requests'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
