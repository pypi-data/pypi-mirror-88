from setuptools import setup

with open('readme.md', 'r') as f :
    readme_content = f.read()

setup(
    name='petit_interfacer',
    version='0.1.1',
    description='Convert your function prototypes to work faster',
    packages=['petit_interfacer'],
    url='https://github.com/Plawn/petit_interfacer',
    license='apache-2.0',
    author='Plawn',
    author_email='plawn.yay@gmail.com',
    long_description=readme_content,
    long_description_content_type="text/markdown",
    python_requires='>=3.8',
    install_requires=[],
)
