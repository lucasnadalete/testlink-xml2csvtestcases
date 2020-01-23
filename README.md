# __Executing the command__

Pre-requirements: Python 2.7+

Exported file with Test Suites and Test Cases specified in Testlink Tool

Execute the command with the following parameters:

Linux:

    - xml2csvconverter --xmlfile=<path_jira_file.xml> --csvfile=<path_requirement_file.csv>

Windows:

    NOT SUPPORTED

# __Build project with PyInstaller__

## Creating venv and preparing environment
    python3.x -m venv venv/
    source venv/bin/activate
    pip install -r dependencies.txt (needs to be in the same VENV used in project folder)
    
## To execute Python file direct the project
    Linux: python xml_converter.py --xmlfile=<path_jira_file.xml> --csvfile=<path_requirement_file.csv>
    Windows: python.exe xml_converter.py --xmlfile=<path_jira_file.xml> --csvfile=<path_requirement_file.csv>

## Windows build command
##### See: http://sparkandshine.net/en/build-a-windows-executable-from-python-scripts-on-linux/
##### Execute:
    wine ~/.wine/drive_c/Python27/Scripts/pyinstaller.exe --onefile xml_converter.spec

## Linux build command
##### Execute:
    pyinstaller --onefile xml_converter.spec
