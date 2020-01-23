import sys
from lxml import etree
import codecs
import csv
import html2text as h2t

class Main():

    def __init__(self):
        self.header_files = ['testsuite', 'testcase_name', 'node_order', 'version', 'summary', 'preconditions', 'execution_type', 'status', 'steps', ]

    def writeCsvFile(self, path_file, content):
        header_fields = self.header_files
        with open(path_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Header row
            writer.writerow(header_fields)
            # Content rows
            for row_dict in content:
                writer.writerow([ row_dict[field] for field in header_fields ])

    def validationArgs(self, args):
        argsCount = 0
        for arg in args:
            if arg.__contains__('--xmlfile') or arg.__contains__('--csvfile'):
                argsCount += 1

        return argsCount == 2

    def extractArg(self, field, args):
        for arg in args:
            if arg.__contains__(field):
                indexSeparator = arg.index('=')
                return arg[indexSeparator + 1:]

    def readTestlinkXmlFile(self, file):
        root = etree.parse(file)
        testcases = []
        for item in root.iter("testcase"):
            testcase = {}
            testcase['testsuite'] = item.getparent().attrib['name']
            testcase['testcase_name'] = item.attrib['name']
            testcase['node_order'] = item.find('node_order').text
            testcase['version'] = item.find('version').text
            testcase['summary'] = h2t.html2text(item.find('summary').text)
            testcase['preconditions'] = h2t.html2text(item.find('preconditions').text).replace('\\-','')
            testcase['execution_type'] = item.find('execution_type').text
            testcase['status'] = item.find('status').text
            testcase['steps'] = self.parseSteps(item.find('steps')).replace('\n', '').replace('#|#', ']\n')
            testcases.append(testcase)
        return testcases

    def parseSteps(self, element):
        steps = ''
        for step in element.iter('step'):
            steps += h2t.html2text(step.find('step_number').text).strip() + ' - Ação do Usuário ['
            steps += h2t.html2text(step.find('actions').text).strip() + '] - Resultado Esperado ['
            steps += h2t.html2text(step.find('expectedresults').text).strip() + '#|#'
        return steps


if __name__ == '__main__':
    m = Main()

    if (m.validationArgs(sys.argv)):
        xmlFilePath = m.extractArg('--xmlfile', sys.argv)
        csvFilePath = m.extractArg('--csvfile', sys.argv)
    # xmlFilePath = 'gestrat-deep.xml'
    # csvFilePath = 'output.csv'
        testlinkTestSuite = m.readTestlinkXmlFile(xmlFilePath)
        m.writeCsvFile(csvFilePath, testlinkTestSuite)
    else:
        print('''
                Pre-requirements: Python 2.7+
                Execute the command with the following parameters:

                    - Linux: python xml_converter.py --xmlfile=<path_jira_file.xml> --csvfile=<path_requirement_file.xml>
                    - Windows: python.exe xml_converter.py --xmlfile=<path_jira_file.xml> --csvfile=<path_requirement_file.xml>

                The Testlink Test Suite with Test Case file must be exported in XML format directly of Testlink Tool.
                ''')