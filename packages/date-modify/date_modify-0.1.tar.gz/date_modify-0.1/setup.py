from distutils.core import setup

setup(
    name='date_modify',
    packages=['date_modify'],
    version='0.1',
    license='MIT',
    description='PHP date_modify() equivalent',
    author='emulienfou',
    author_email='emulienfou@gmail.com',
    url='https://github.com/emulienfou',
    download_url='https://github.com/emulienfou/date_modify/archive/v0.1.tar.gz',
    keywords=['php', 'date_modify', 'DateTime::modify', 'DateTime', 'modify'],
    install_requires=['python-dateutil', 'six'],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8'
    ]
)
