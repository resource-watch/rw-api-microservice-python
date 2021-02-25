from setuptools import setup

setup(name='RWAPIMicroservicePython',
      version='0.2.0',
      description='Python integration library for the RW API microservices',
      author='Vizzuality',
      author_email='info@vizzuality.com',
      url='https://vizzuality.com',
      license='MIT',
      packages=['RWAPIMicroservicePython'],
      install_requires=[
        'flask',
        'requests'
      ],
      extras_require={
        'dev': [
            'Flask==1.1.1',
            'pytest==5.2.2',
            'pytest-cov==2.8.1',
            'pytest-mock==1.11.1',
            'codecov==2.0.15',
            'requests_mock==1.7.0',
        ]
      },
      zip_safe=False)
