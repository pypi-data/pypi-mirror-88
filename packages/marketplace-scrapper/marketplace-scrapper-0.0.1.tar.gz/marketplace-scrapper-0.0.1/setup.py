import setuptools


with open('README.rst', 'r', encoding='utf-8') as f:
    description = f.read()

setuptools.setup(
    name='marketplace-scrapper',
    version='0.0.1',
    author='Muremwa',
    author_email='danmburu254@gmail.com',
    url='https://github.com/muremwa/VSmarketplace-scrapper',
    description='Extract details of a (visual studio, vscode, azure devops)'
                ' extension from https://marketplace.visualstudio.com',
    long_description=description,
    long_description_content_type='text/x-rst',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
