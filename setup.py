from setuptools import setup, find_packages

import project_info

setup(
    name=project_info.name,

    use_scm_version=True,

    description=project_info.description,

    url=project_info.source_url,

    author=project_info.author_name,
    author_email=project_info.author_email,

    license=project_info.license_name,

    packages=find_packages(),

    setup_requires=[
        'setuptools_scm'
    ],

    install_requires=[
        'telegram-bot',
        'pytz',
        'babel',
    ],

    python_requires='>=3',
)
