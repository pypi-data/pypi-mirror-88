from setuptools import setup
setup(
        name = 'restlogger',
        version = '0.1.3',
        packages = ['restlogger'],
        entry_points = {
            'console_scripts': [
                'restlogger = restlogger.__main__:main'
                ]
            })

