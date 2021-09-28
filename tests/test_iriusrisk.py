import unittest
import pytest
from tests.config import setup, check


class TestIriusRisk(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.api_token, self.config, self.product_ref, self.api_instance = setup()

    def setUp(self):
        self.test_config = check(unittest.TestCase.id(self).rsplit(".")[-1], self.config)

    def test_residual_risk_over_risk_threshold(self):
        """Shows if the current risk of a product exceed a risk threshold"""
        try:
            riskThreshold = self.test_config["variables"]["RISK_THRESHOLD"]
        except KeyError:
            riskThreshold = 50
            print(f"Using default risk threshold: {riskThreshold}")

        risk_summary = self.api_instance.products_ref_risks_get(self.api_token, self.product_ref)
        if risk_summary.residual_risk > riskThreshold:
            pytest.fail(
                f"Product {self.product_ref} has risk {risk_summary.residual_risk} and is over the threshold {riskThreshold}")


    def test_required_controls_not_implemented(self):
        """Shows how many required controls are not implemented"""
        try:
            percentage = int(self.test_config["variables"]["PERCENTAGE"])
        except KeyError:
            percentage = 50
            print(f"Using default percentage: {percentage}")

        allControls = self.api_instance.products_ref_controls_get(self.api_token, self.product_ref)
        total = len(allControls)

        if total != 0:
            required = 0
            for control in allControls:
                state = control.state
                if state == "Required":
                    required += 1

            proportion = (required/total)*100
            if proportion >= percentage:
                pytest.fail(f"Above percentage: there are {proportion}% countermeasures marked as required over the maximum percentage required of {percentage}%")


    def test_standard_controls_not_implemented(self):
        """Shows how many required controls related to a standard are not implemented"""
        try:
            standardRef = self.test_config["variables"]["STANDARD_REF"]
        except KeyError:
            pytest.fail("No standard ref found in configuration variables")

        try:
            percentage = self.test_config["variables"]["PERCENTAGE"]
        except KeyError:
            percentage = 50
            print(f"Using default percentage: {percentage}")

        allControls = self.api_instance.products_ref_controls_get(self.api_token, self.product_ref)
        total = 0
        notImplemented = 0
        for control in allControls:
            standards = control.standards
            if standards is not None:
                standardNames = [std.name for std in standards]
                if standardRef in standardNames:
                    total += 1
                    if control.state != "Implemented":
                        notImplemented += 1

        if total != 0:
            proportion = (notImplemented / total) * 100
            if proportion >= percentage:
                pytest.fail(f"Above percentage: there are {proportion}% countermeasures that applies {standardRef} that are not implemented")


    def test_high_risk_controls_not_implemented(self):
        """Shows how many controls with high risk are not implemented"""
        try:
            percentage = self.test_config["variables"]["PERCENTAGE"]
        except KeyError:
            percentage = 50
            print(f"Using default percentage: {percentage}")

        try:
            high_risk_value = self.test_config["variables"]["HIGH_RISK_VALUE"]
        except KeyError:
            high_risk_value = 75
            print(f"Using default high_risk_value: {high_risk_value}")

        allControls = self.api_instance.products_ref_controls_get(self.api_token, self.product_ref)
        total = 0
        notImplementedWithHighPriority = 0
        for control in allControls:
            if control.risk >= high_risk_value:
                total += 1
                if control.state != "Implemented":
                    notImplementedWithHighPriority += 1

        if total != 0:
            proportion = (notImplementedWithHighPriority / total) * 100
            if proportion > percentage:
                pytest.fail(f"Above percentage: there are {proportion}% countermeasures with high risk that are not implemented")


