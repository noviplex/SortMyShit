from unittest import TestSuite, TextTestRunner

from tests.domain.service.CompareBinaryTest import BinaryComparatorTest
from tests.domain.service.CompareFileNameTest import FileNameComparatorTest
from tests.domain.service.RemoveDuplicateTest import RemoveDuplicateTest
from tests.domain.service.RemoveEmptyFolderTest import RemoveEmptyFolderTest
from tests.domain.service.ListDuplicateTest import ListDuplicateTest
from tests.domain.service.RemoveEmptyFileTest import RemoveEmptyFileTest


def suite():
    suite = TestSuite()
    suite.addTest(BinaryComparatorTest)
    suite.addTest(FileNameComparatorTest)
    suite.addTest(RemoveDuplicateTest)
    suite.addTest(RemoveEmptyFolderTest)
    suite.addTest(ListDuplicateTest)
    suite.addTest(RemoveEmptyFileTest)
    return suite


if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
