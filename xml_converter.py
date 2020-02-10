import sys
from lxml import etree
import codecs
import csv
import html2text as h2t

class Main():

    def __init__(self):
        self.header_files = ['testsuite', 'testcase_name', 'node_order', 'version', 'summary', 'preconditions', 'execution_type', 'status', 'step_number', 'actions', 'expectedresults']

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
            testcase[self.header_files[2]] = item.find(self.header_files[2]).text
            testcase[self.header_files[3]] = item.find(self.header_files[3]).text
            testcase[self.header_files[4]] = h2t.html2text(item.find(self.header_files[4]).text)
            testcase[self.header_files[5]] = h2t.html2text(item.find(self.header_files[5]).text).replace('\\-','')
            testcase[self.header_files[6]] = item.find(self.header_files[6]).text
            testcase[self.header_files[7]] = item.find(self.header_files[7]).text
            lst_steps = self.parseSteps(item.find('steps'))
            testcase[self.header_files[8]] = lst_steps[0][self.header_files[8]]
            testcase[self.header_files[9]] = lst_steps[0][self.header_files[9]]
            testcase[self.header_files[10]] = lst_steps[0][self.header_files[10]]
            testcases.append(testcase)
            for step in lst_steps[1:]:
                testcases.append(self.createTestCaseOnlySteps(step))
        return testcases
    def createTestCaseOnlySteps(self, step):
        steps_testcase = { key: '' for key in self.header_files[:8] }
        steps_testcase[self.header_files[8]] = step[self.header_files[8]]
        steps_testcase[self.header_files[9]] = step[self.header_files[9]]
        steps_testcase[self.header_files[10]] = step[self.header_files[10]]
        return steps_testcase 

    def parseSteps(self, element):
        steps = []
        for step in element.iter('step'):
            register = {}
            register[self.header_files[8]] = h2t.html2text(step.find(self.header_files[8]).text).strip()
            register[self.header_files[9]] = h2t.html2text(step.find(self.header_files[9]).text).strip()
            register[self.header_files[10]] =  h2t.html2text(step.find(self.header_files[10]).text).strip()
            steps.append(register)
        return steps


if __name__ == '__main__':
    m = Main()

    if (m.validationArgs(sys.argv)):
        xmlFilePath = m.extractArg('--xmlfile', sys.argv)
        csvFilePath = m.extractArg('--csvfile', sys.argv)
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