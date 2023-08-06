import setuptools

with open("README.txt", "r",encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='jhsp',
    version="0.0.14",
    author='Junhe Zhao',
    author_email="zhaozong111@gmail.com",
    description="A package only used by Junhe Zhao",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://pypi.org',
    packages = setuptools.find_packages(),
    install_requires=['pandas==1.1.3',
                        'numpy==1.18.5',
                        'tensorflow==2.3.1',
                        'matplotlib==3.3.2',
                        'scikit_learn==0.23.2',
                      ],

)