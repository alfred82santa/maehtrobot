from setuptools import setup
import os

setup(
    name='maehtrobot',
    url='https://github.com/alfred82santa/maehtrobot',
    author='alfred82santa',
    version='0.1.0',
    author_email='alfred82santa@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta'],
    packages=['maehtrobot'],
    include_package_data=False,
    install_requires=['dirty-loader', 'aiohttp'],
    description="Maehtro bot",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    test_suite="nose.collector",
    tests_require="nose",
    zip_safe=True,
)
