import setuptools

setuptools.setup(
    name='test-packaging-rss',
    version='0.0.7',
    url='https://github.com/baobabtr33/test-packaging-rss',
    license='',
    author='Kim Jung Hwan',
    install_requires    =  ['feedparser'],
    packages=setuptools.find_packages(),
    author_email='author@example.com',
    description='test packaging',
    setup_requires=['wheel']
)

