from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='esales',
    version='0.0.6',
    description='This is a very simple eslaes module :)',
    long_description='there is no long description :)',
    long_description_content_type='text/markdown' ,
    url='',
    author='Rients Hoeksma',
    author_email='rientshoeksma@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='esales',
    packages=find_packages(),
    install_requires=['']
)


