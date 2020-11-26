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
        try:
            riskThreshold = self.test_config["variables"]["RISK_THRESHOLD"]
        except KeyError:
            print("Using default risk threshold: 50")
            riskThreshold = 50

        risk_summary = self.api_instance.products_ref_risks_get(self.api_token, self.product_ref)
        if risk_summary.residual_risk > riskThreshold:
            pytest.fail(
                f"Product {self.product_ref} has risk {risk_summary.residual_risk} and is over the threshold {riskThreshold}")

