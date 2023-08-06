from distutils.core import setup

setup(
    name='my_printer',
    packages= ['my_printer'],
    version='0.1',
    license='unlicense',
    description='Test Pip Package',
    author='Mohammad Abid',
    author_email='mohammad.abid.p95@gmail.com',
    url='https://github.com/Mohammad95abid/Printer.git',
    download_url = 'https://github.com/Mohammad95abid/Printer/archive/0.1.tar.gz',    # I explain this later on
    keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
            'numpy',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],


)