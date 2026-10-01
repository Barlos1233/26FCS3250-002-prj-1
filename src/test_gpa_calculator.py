import unittest
from gpa_calculator import calculate_gpa

class GpaCalculatorTest(unittest.TestCase):

    def testNoEnrollments(self):
        self.assertEqual(0, calculate_gpa([]))

    def testSingleCourse(self):
        self.assertAlmostEqual(3.0, calculate_gpa([{'grade': 'B', 'credits': 3}]))

    def testCreditWeightedGpa(self):
        enrollments = [
            {'grade': 'B', 'credits': 4},
            {'grade': 'C-', 'credits': 4}
        ]
        self.assertAlmostEqual(2.35, calculate_gpa(enrollments))

    def testCreditsChangeTheWeight(self):
        enrollments = [
            {'grade': 'A', 'credits': 3},
            {'grade': 'F', 'credits': 1}
        ]
        self.assertAlmostEqual(3.0, calculate_gpa(enrollments))

    def testAPlusAndF(self):
        enrollments = [
            {'grade': 'A+', 'credits': 3},
            {'grade': 'F', 'credits': 3}
        ]
        self.assertAlmostEqual(2.15, calculate_gpa(enrollments))

    def testAPlusAloneExceedsFour(self):
        self.assertAlmostEqual(4.3, calculate_gpa([{'grade': 'A+', 'credits': 3}]))

    def testMissingGradeIsIgnored(self):
        enrollments = [
            {'grade': None, 'credits': 4},
            {'grade': 'A', 'credits': 4}
        ]
        self.assertAlmostEqual(4.0, calculate_gpa(enrollments))

    def testUnrecognizedGradeIsIgnored(self):
        enrollments = [
            {'grade': 'Z', 'credits': 4},
            {'grade': 'A', 'credits': 4}
        ]
        self.assertAlmostEqual(4.0, calculate_gpa(enrollments))

    def testNoGradedCredits(self):
        enrollments = [
            {'grade': None, 'credits': 4},
            {'grade': 'Z', 'credits': 3}
        ]
        self.assertEqual(0, calculate_gpa(enrollments))

if __name__ == '__main__':
    unittest.main()