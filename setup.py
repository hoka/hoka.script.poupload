from setuptools import setup, find_packages

version = '2.13.19.1'

setup(name='hoka.script.poupload',
      version=version,
      description='Upload po files to a po server',
      long_description=open("README.rst").read(),
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "Intended Audience :: Other Audience",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        ],
      keywords='adapter po upload script hoka',
      author='Kai Hoppert',
      author_email='kai.hoppert@online.de',
      url='http://eggserver.tcis.de/hoka.script.poupload',
      license='GPL version 2',
      packages=find_packages(),
      namespace_packages=['hoka'],
      include_package_data=True,
      install_requires=[
        'setuptools',
        'Zope2',
        'z3c.autoinclude',
      ],
      extras_require={'test': [
        'collective.testcaselayer',
      ]},
      entry_points={
          'console_scripts': 'poupload=hoka.script.poupload:main',},
      platforms='Any',
      zip_safe=False,
)