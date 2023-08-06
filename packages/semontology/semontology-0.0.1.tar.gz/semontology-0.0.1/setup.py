import setuptools
import semontology

setuptools.setup(
    name='semontology',
    version=semontology.__version__,
    author='Zharkov A.P.',
    author_email='antonzharckov@yandex.ru',
    description='semontology',
    long_description='semontology',
    long_description_content_type='',
    url='https://github.com/Zharkov/semontology',
    packages=setuptools.find_packages(),
    test_suite='tests',
    python_requires='>=3.8',
    platform=["any"]
)