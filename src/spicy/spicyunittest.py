# coding: utf-8
import unittest

from fabric.colors import *
from django.test.utils import setup_test_environment


class SpicyTextTestResult(unittest.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = green('=' * 80)
    separator2 = green('-' * 80)

    def __init__(self, stream, descriptions, verbosity):
        super(SpicyTextTestResult, self).__init__()
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '{0}\n{1}\nShort desc: {2}\n'.format(
                self.separator2,
                yellow(test),
                green(doc_first_line))
        else:
            return '{0}\n{1}\nShort desc: {2}\n'.format(
                self.separator2,
                yellow(test),
                red('Unavailable (docstring not defined)'))

    def startTest(self, test):
        super(SpicyTextTestResult, self).startTest(test)
        if self.showAll:
            self.stream.write(self.getDescription(test))
            self.stream.write(yellow(" ... "))
            self.stream.flush()

    def addSuccess(self, test):
        super(SpicyTextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln(green("ok"))
        elif self.dots:
            self.stream.write(green('.'))
            self.stream.flush()

    def addError(self, test, err):
        super(SpicyTextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln(red("ERROR"))
        elif self.dots:
            self.stream.write(red('E'))
            self.stream.flush()

    def addFailure(self, test, err):
        super(SpicyTextTestResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln(red("FAIL"))
        elif self.dots:
            self.stream.write(red('F'))
            self.stream.flush()

    def addSkip(self, test, reason):
        super(SpicyTextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln(yellow("skipped {0!r}").format(blue(reason)))
        elif self.dots:
            self.stream.write(yellow("s"))
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(SpicyTextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln(red("expected failure"))
        elif self.dots:
            self.stream.write(red("x"))
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(SpicyTextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln(red("unexpected success"))
        elif self.dots:
            self.stream.write(red("u"))
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList(red('ERROR'), self.errors)
        self.printErrorList(red('FAIL'), self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)


class SpicyTextTestRunner(unittest.TextTestRunner):
    """Spicy wrapper over `unittest` text runner."""

    resultclass = SpicyTextTestResult

    def _makeResult(self):
        self.stream.writeln(green('~> Starting Spicy unittest wrapper'))
        return self.resultclass(self.stream, self.descriptions, self.verbosity)


setup_test_environment()
print '@@@'
unittest.main(testRunner=SpicyTextTestRunner)
