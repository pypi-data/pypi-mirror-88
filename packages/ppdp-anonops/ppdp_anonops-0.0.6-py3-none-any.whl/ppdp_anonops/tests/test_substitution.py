from unittest import TestCase
import os
from ppdp_anonops import Substitution
from pm4py.objects.log.importer.xes import factory as xes_importer


class TestSubstitution(TestCase):
    def getTestXesLog(self):
        xesPath = os.path.join(os.path.dirname(__file__), 'resources', 'running_exampleWithCaseAttributes.xes')
        return xes_importer.apply(xesPath)

    def test_01_substituteResourcesEvent(self):
        log = self.getTestXesLog()

        s = Substitution()

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertGreater(frequency["Sean"], 0)
        self.assertGreater(frequency["Sara"], 0)

        log = s.SubstituteEventAttributeValue(log, "org:resource", ["Sean", "Sara"], [])

        frequency = {"Sean": 0, "Sara": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if event["org:resource"] in frequency.keys():
                    frequency[event["org:resource"]] += 1

        self.assertEqual(frequency["Sean"], 0)
        self.assertEqual(frequency["Sara"], 0)

    def test_02_substituteAttributeWithRandomCase(self):
        log = self.getTestXesLog()

        s = Substitution()

        frequency = {"52062": 0, "52064": 0}
        for case_index, case in enumerate(log):
            if case.attributes["Zip"] in frequency.keys():
                frequency[case.attributes["Zip"]] += 1

        self.assertGreater(frequency["52062"], 0)
        self.assertGreater(frequency["52064"], 0)

        log = s.SubstituteCaseAttributeValue(log, "Zip", ["52062", "52064"], [])

        frequency = {"52062": 0, "52064": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if case.attributes["Zip"] in frequency.keys():
                    frequency[case.attributes["Zip"]] += 1

        self.assertEqual(frequency["52062"], 0)
        self.assertEqual(frequency["52064"], 0)

    def test_03_substituteAttributeWithDataCase(self):
        log = self.getTestXesLog()

        s = Substitution()

        frequency = {"52062": 0, "52064": 0}
        for case_index, case in enumerate(log):
            if case.attributes["Zip"] in frequency.keys():
                frequency[case.attributes["Zip"]] += 1

        self.assertGreater(frequency["52062"], 0)
        self.assertGreater(frequency["52064"], 0)

        log = s.SubstituteCaseAttributeValue(log, "Zip", ["52062", "52064"], ["Test", "PLZ"])

        frequencyAfter = {"52062": 0, "52064": 0, "Test": 0, "PLZ": 0}
        for case_index, case in enumerate(log):
            for event_index, event in enumerate(case):
                if case.attributes["Zip"] in frequencyAfter.keys():
                    frequencyAfter[case.attributes["Zip"]] += 1

        self.assertEqual(frequencyAfter["52062"], 0)
        self.assertEqual(frequencyAfter["52064"], 0)

        # Check together, as real randomness could only choose one of the two alternatives
        self.assertGreater(frequencyAfter["Test"] + frequencyAfter["PLZ"], 0)
