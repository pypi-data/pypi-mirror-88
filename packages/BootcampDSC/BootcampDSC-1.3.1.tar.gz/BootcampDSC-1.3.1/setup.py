from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(name = 'BootcampDSC',
        version = '1.3.1',
        description = 'Data Literate Bootcamp DSC UMM',
        long_description = long_description,
        long_description_content_type = 'text/markdown', 
        # packages = ['BootcampDSC'],
        author = 'shandytp',
        author_email = 'shandytsalasa@gmail.com',
        packages = find_packages(),
        zip_safe = False)
