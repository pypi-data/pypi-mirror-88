from os import walk, path as osp
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

data_files = []
for dirname, dirnames, filenames in walk(f'{here}/boxes_classifier/data'):
    fileslist = []
    for filename in filenames:
        fullname = osp.join(dirname, filename)
        fileslist.append(fullname)
    data_files += fileslist
print(data_files)
setup(
    name="boxes_classifier",
    version="1.0.4",
    description="SF Core processing data library",
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    author='duongpd',  # Optional
    author_email="duongpd@bap.jp",
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        # 'License :: OSI Approved :: SF License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='sample, setuptools, development',  # Optional
    packages=find_packages(),  # Required
    entry_points={
        'console_scripts': [
            'sfedu_cli=SF_EDU.boxes_classifier_cli:main'
        ]
    },
    python_requires='>=3.6, <4',
    extras_require={  # Optional
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        '': data_files,
    },
    install_requires=[
        "opencv-python",
        "pillow",
        "tensorflow-cpu",
        "image_embeddings"
    ],
)