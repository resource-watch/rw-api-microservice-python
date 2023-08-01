from setuptools import setup

setup(name='RWAPIMicroservicePython',
      version='2.0.0',
      description='Python integration library for the RW API microservices',
      author='Vizzuality',
      author_email='info@vizzuality.com',
      url='https://vizzuality.com',
      license='MIT',
      packages=['RWAPIMicroservicePython'],
      install_requires=[
        'Flask<=2.2.2',
        'requests<2.29',
      ],
      extras_require={
        'dev': [
            'boto3==1.28.16',
            'codecov==2.1.13',
            'Flask==2.2.2',
            'moto[logs]==4.1.4',
            'pytest==7.4.0',
            'pytest-cov==4.1.0',
            'pytest-mock==3.11.1',
            'requests_mock==1.11.0',
        ]
      },
      zip_safe=False)
