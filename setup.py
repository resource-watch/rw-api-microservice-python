from setuptools import setup

setup(name='RWAPIMicroservicePython',
      version='3.0.0-rc.2',
      long_description='Python integration library for the RW API microservices',
      description='Python integration library for the RW API microservices',
      long_description_content_type='text',
      author='Vizzuality',
      author_email='info@vizzuality.com',
      url='https://vizzuality.com',
      license='MIT',
      packages=['RWAPIMicroservicePython'],
      install_requires=[
        'boto3==1.28.16',
        'Flask<=2.3.2',
        'requests<=2.31',
      ],
      extras_require={
        'dev': [
            'codecov==2.1.13',
            'Flask==2.3.2',
            'moto[logs]==4.1.4',
            'pytest==7.4.0',
            'pytest-cov==4.1.0',
            'pytest-mock==3.11.1',
            'requests_mock==1.11.0',
        ]
      },
      zip_safe=False)
