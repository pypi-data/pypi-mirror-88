'''
# @Time    : 2020/12/11 18:17 PM
# @Author  : Jude
# @File    : setup.py
# @E-main:wangyifan7836@gmail.com
'''



from setuptools import setup, find_packages



setup(
    name = "pythoption",
    version = "1.0.1",
    keywords = ("pip", "python3","option",'derivative','finance'),
    description = "A Python library for options supporting black_scholes,binomial_tree and monte_carlo",
    long_description = "A simple and elegant option library.",
    license = "MIT Licence",

    url = "https://github.com/www5226448/pythoption",
    author = "Jude",
    author_email = "wangyifan7836@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['numpy==1.18.1',
                        'scipy==1.4.1']
)
