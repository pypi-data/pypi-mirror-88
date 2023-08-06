"""
Module handles Dicord functionality
"""

from junitparser import JUnitXml, TestSuite

class JunitHandler():

    @staticmethod
    def junitFactory(junit_creator):
        if (junit_creator == "phpstan"):
            return JunitPHPStanHandler()
        elif (junit_creator == "phpunit"):
            return JunitPHPUnitHandler()

    def setJunitReport(self, junit_report):
        self.junit_report = junit_report

    def parseReport(self):
        try:
            xml = JUnitXml.fromfile(self.junit_report)
        except FileNotFoundError:
            raise
        
        failures = 0
        tests = 0
        errors = 0

        if isinstance(xml, TestSuite):
            failures = xml.failures
            tests = xml.tests
            errors = xml.errors
        else:
            for suite in xml:
                failures = failures + suite.failures
                tests = tests + suite.tests
                errors = errors + suite.errors

        self.metrics = {'failures' : failures, 'tests' : tests, 'errors' : errors, 'issues' : failures + errors}

    def isSuccess(self):
        if (self.metrics['failures'] + self.metrics['errors'] > 0):
            return False
        return True

    def getIcon(self):
        if self.isSuccess():
            return ':green_heart:'
        else:
            return ':no_entry:'
        
class JunitPHPStanHandler(JunitHandler):
    def getCIMessage(self):
        return "Issues: {metrics[issues]}".format(metrics=self.metrics)

class JunitPHPUnitHandler(JunitHandler):
    def getCIMessage(self):
        return "Tests: {metrics[tests]}, failures {metrics[failures]}, errors {metrics[errors]}".format(metrics=self.metrics)