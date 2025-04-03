from unittest import TestSuite, TextTestRunner

from tests.domain.service.BinaryComparatorTest import BinaryComparatorTest
from tests.domain.service.FileNameComparatorTest import FileNameComparatorTest
from tests.domain.service.DuplicateRemoverTest import DuplicateRemoverTest
from tests.domain.service.EmptyFolderRemoverTest import EmptyFolderRemoverTest

def suite():
    suite = TestSuite()
    suite.addTest(BinaryComparatorTest)
    suite.addTest(FileNameComparatorTest)
    suite.addTest(DuplicateRemoverTest)
    suite.addTest(EmptyFolderRemoverTest)
    return suite

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())