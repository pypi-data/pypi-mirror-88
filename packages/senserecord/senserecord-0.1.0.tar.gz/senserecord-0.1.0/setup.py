# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['senserecord',
 'senserecord.cli',
 'senserecord.core',
 'senserecord.gui',
 'senserecord.http']

package_data = \
{'': ['*'], 'senserecord.http': ['static/*']}

install_requires = \
['PyQt5>=5.15.1,<6.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'QtAwesome>=1.0.1,<2.0.0',
 'aiofiles>=0.6.0,<0.7.0',
 'brainflow>=3.7.1,<4.0.0',
 'fastapi>=0.61.2,<0.62.0',
 'pyshortcuts>=1.7.1,<2.0.0',
 'typer[all]>=0.3.2,<0.4.0',
 'uvicorn>=0.12.2,<0.13.0']

entry_points = \
{'console_scripts': ['senserecord = senserecord.main:console',
                     'senserecord-gui = senserecord.main:gui',
                     'senserecord-http = senserecord.main:http']}

setup_kwargs = {
    'name': 'senserecord',
    'version': '0.1.0',
    'description': 'A cross-platform application for saving data streams from biosensor hardware.',
    'long_description': '# Sense Record\n\nA cross-platform application for saving data streams from biosensor hardware using the [BrainFlow Python API](https://brainflow.readthedocs.io/en/stable/UserAPI.html#python-api-reference).\n\nSense Record is designed for a research lab setting, where the user (experimenter, study staff) needs to ensure that the raw file stream is being saved and that the file is saved along with information about the experimental session/task/run/participant.\n\nSense Record saves biosensor recordings using file naming conventions compliant with the [Brain Imaging Data Structure (BIDS)](https://bids-specification.readthedocs.io/en/stable/). The user is prompted to enter the subject/participant, session, task, and run information before starting any recording. This data is then used by Sense Record to generate the output file name and sub directory names, along with BIDS-spec metadata files that it saves with each recording.\n\n## Installation\n\nInvoke `pip` as appropriate in your environment to do:\n\n```bash\npip install senserecord\n```\n\n## Usage\n\nSense Record provides three types of interfaces for recording biosensor data with BrainFlow: a GUI desktop app, a command-line interface, and a REST web services API.\n\nTo launch the GUI desktop app:  \n`senserecord-gui`\n\nTo launch the CLI console app:  \n`senserecord`\n\nTo launch the local http server and web app with REST API:  \n`senserecord-http`\n\nLearn more about each of these interfaces in the sections below.\n\n### GUI Desktop Application\n\nThe GUI provides controls for starting and stopping recordings. It prompts you for run information (BIDS fields) at the start of each recording run.\n\n![Screenshot](screenshot.png)\n\n1. Launch the GUI by running the command: `senserecord-gui`\n2. In the menu bar, select **File > Load configuration file** and load your `.yml` file. Use the example configuration files in [`/examples`](examples) to create your config file.\n3. Press the "Start Recording" button. A dialog will appear, prompting you to enter information (BIDS fields) about your recording.\n4. Record until your task/run is finished.\n5. Press the "Stop Recording" button.\n6. Find your recording\'s raw data file in `[bidsroot]/sourcedata/sub-[subject]/ses-[session]/[data_type]/*.csv`\n\n### CLI Application\n\nSense Record comes with an interactive command-line interface.\n\nType `senserecord` with no arguments and it shows you help text.\n\nType `senserecord start` with no arguments and you are prompted for input, like this:\n\n```bash\nEnter your board name: SYNTHETIC_BOARD\nEnter the path to the root directory of your project: ./\nSubject name/ID: 001\nSession name: testSession\nTask name: myExperiment\nRun number: 001\nData type. Choices: eeg, ecg,: eeg\nNow recording from SYNTHETIC_BOARD\nStop the recording? [y/N]: n\nStop the recording? [y/N]: y\nStopped recording from SYNTHETIC_BOARD\n```\n\nThis example run created a test directory `sourcedata/sub-001/ses-testSession/eeg` with a data file inside named `sub-001_ses-testSession_task-myExperiment_run-001_eeg.csv`.\n\nYou can also bypass the prompts with command-line arguments, like this example:\n\n```bash\n:$ senserecord start --board-name SYNTHETIC_BOARD --serial-port /dev/ttyUSB0 --bidsroot /home/myuser/my_experiment_dir --sub 001 --ses mySession --task myTask --run 001 --data-type eeg\n```\n\nType `senserecord start --help` to see available options.\n\n### REST Web Services API\n\nYou can control recordings over http using the built-in REST web services API. Start the REST server with:\n\n```bash\nsenserecord-http\n```\n\nThis will launch the server process and try to open the http endpoint in your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000). Visit that URL and you get interactive HTML documentation that allows you to start and stop recordings from your browser. You can also use it to build URLs like the one used in the example below.\n\n### Example usage of the REST API\n\nRecordings can be started with a GET request, with parameters in the query string of the URL.\n\nVisit this example URL and it will start recording from `SYNTHETIC_BOARD`:\n\n```\nhttp://127.0.0.1:8000/start/SYNTHETIC_BOARD?bidsroot=%2Fhome%2Flink%2FDownloads&serial_port=%2Fdev%2FttyUSB0&sub=001&ses=default&task=default&run=001&data_type=eeg&modality=eeg\n```\n\nIt returns a simple JSON response that looks something like this:\n\n```json\n{\n  "status": "ok",\n  "result": {\n    "board": {\n      "name": "SYNTHETIC_BOARD",\n      "is_ready": false,\n      "is_recording": true\n    }\n  },\n  "details": []\n```\n\nDon\'t forget to stop the recording! You can do that by visiting this URL:\n\n```\nhttp://127.0.0.1:8000/stop/SYNTHETIC_BOARD\n```\n\nWhen the recording stops, the API returns this JSON response smth like:\n\n```json\n{\n  "status": "ok",\n  "result": {\n    "board": {\n      "name": "SYNTHETIC_BOARD",\n      "is_ready": true,\n      "is_recording": false\n    }\n  },\n  "details": []\n}\n```\n\n## License\n\nGPL-3.0-or-later\n\n## Contact\n\nLink Swanson (link@swanson.link)\n',
    'author': 'Link Swanson',
    'author_email': 'link@swanson.link',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
