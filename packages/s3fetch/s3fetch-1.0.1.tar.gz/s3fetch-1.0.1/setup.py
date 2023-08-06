# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['s3fetch']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.15.18,<2.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['s3fetch = s3fetch:cmd']}

setup_kwargs = {
    'name': 's3fetch',
    'version': '1.0.1',
    'description': 'Simple S3 download tool.',
    'long_description': "# S3Fetch\n\nEasy to use, multi-threaded S3 download tool.\n\nSource: [https://github.com/rxvt/s3fetch](https://github.com/rxvt/s3fetch)\n\nFeatures:\n\n- Simple to use.\n- Multi-threaded, allowing you to download multiple objects concurrently (defaults to amount of cores available).\n- Quickly download a subset of objects under a prefix without listing all objects.\n- Filter list of objects using regular expressions.\n- Uses standard Boto3 AWS SDK and standard AWS credential locations.\n- Dry run mode if you just want to see what would be downloaded.\n\n## Installation\n\n### Requirements\n\n- Python 3.9\n\nS3Fetch is available on PyPi and be installed via one of the following methods Prior to running it ensure you have AWS credentials configured in one of the [standard locations](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-where).\n\n### pipx (recommended)\n\nEnsure you have [pipx](https://pypi.org/project/pipx/) installed, then:\n\n`pipx install s3fetch`\n\n\n### pip\n\n`pip3 install s3fetch`\n\n\n## Usage:\n\n```\nUsage: s3fetch [OPTIONS] S3_URI\n\n  Easily download objects from an S3 bucket.\n\n  Example: s3fetch s3://my-test-bucket/birthday-photos/2020-01-01\n\n  The above will download all S3 objects located under the `birthday-\n  photos/2020-01-01` prefix.\n\n  You can download all objects in a bucket by using `s3fetch s3://my-test-\n  bucket/`\n\nOptions:\n  --region TEXT        Bucket region. Defaults to 'us-east-1'.\n  -d, --debug          Enable debug output.\n  --download-dir TEXT  Download directory. Defaults to current directory.\n  --regex TEXT         Filter list of available objects by regex.\n  --threads INTEGER    Number of threads to use. Defaults to core count.\n  --dry-run            Don't download objects.\n  --delimiter TEXT     Specify the directory delimiter. Defaults to '/'\n  -q, --quiet          Don't print to stdout.\n  --help               Show this message and exit.\n```\n\n## Examples:\n\n### Full example\n\nDownload using 4 threads, into `~/Downloads/tmp`, only downloading objects that end in `.dmg`.\n\n```\n$ s3fetch s3://my-test-bucket --download-dir ~/Downloads/tmp/ --threads 4  --regex '\\.dmg$'\ntest-1.dmg...done\ntest-2.dmg...done\ntest-3.dmg...done\ntest-4.dmg...done\ntest-5.dmg...done\n```\n\n### Download all objects from a bucket\n\n```\ns3fetch s3://my-test-bucket/\n```\n\n### Download objects with a specific prefix \n\nDownload all objects that strt with `birthday-photos/2020-01-01`.\n```\ns3fetch s3://my-test-bucket/birthday-photos/2020-01-01\n```\n\n### Download objects to a specific directory\n\nDownload objects to the `~/Downloads` directory.\n```\ns3fetch s3://my-test-bucket/  --download-dir ~/Downloads\n```\n\n### Download multiple objects concurrently\n\nDownload 4 objects concurrently.\n```\ns3fetch s3://my-test-bucket/ --threads 4\n```\n\n### Filter objects using regular expressions\n\nDownload objects ending in `.dmg`.\n```\ns3fetch s3://my-test-bucket/ --regex '\\.dmg$'\n```\n\n",
    'author': 'Shane Anderson',
    'author_email': 'shane@reactivate.cx',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rxvt/s3fetch',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
