from setuptools import setup, find_packages


setup(
    name='clock-bot',

    use_scm_version=True,

    description='A clock bot',

    url='https://github.com/alvarogzp/clock-bot',

    author='Alvaro Gutierrez Perez',
    author_email='alvarogzp@gmail.com',

    license='AGPL-3.0',

    packages=find_packages(),

    setup_requires=[
        'setuptools_scm'
    ],

    install_requires=[
        'telegram-bot',
        'pytz'
    ],

    python_requires='>=3',
)
