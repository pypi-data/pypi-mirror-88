from setuptools import setup, find_packages

setup(
  name='kittenai',
  version='0.1.2',
  keywords=('kittenai'),
  license='MIT',
  author='riven',
  url='https://gitee.com/KittenTech/pylib_kittenai',
  author_email='riven@kittenbot.cc',
  packages=find_packages(exclude=('tests')),
  install_requires=['requests'],
  description="AI for kittencode python ide",
  platform='any'
)

