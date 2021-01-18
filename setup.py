from setuptools import setup

setup(name='RWAPIMicroservicePython',
      version='0.1.0',
      description='Integration library for the RW API microservice',
      author='Vizzuality',
      author_email='info@vizzuality.com',
      license='MIT',
      packages=['RWAPIMicroservicePython'],
      install_requires=[
        'flask',
        'requests'
      ],
      extras_require={
        'dev': [
            'pytest==5.2.2',
            'pytest-cov==2.8.1',
            'pytest-mock==1.11.1',
            'codecov==2.0.15',
            'requests_mock==1.7.0',
        ]
      },
      zip_safe=False)
