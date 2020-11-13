import unittest
import pytest
from tests.config import setup, check


class TestIriusRisk(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.api_token, self.config, self.product_ref, self.api_instance = setup()

    def setUp(self):
      self.test_config = check(unittest.TestCase.id(self).rsplit(".")[-1], self.config)
      print(self.test_config)

    def test_template(self):
        # TODO: Do test
        pass
        # Failures are marked with pytest.fail("message")
        # Skipped tests are marked with pytest.skip("message")

    def test_product_risk_is_very_high(self):
        riskThreshold = self.test_config["variables"]["RISK_THRESHOLD"]
        if not riskThreshold:
            pytest.skip("No risk threshold")

        risk_summary = self.api_instance.products_ref_risks_get(self.api_token, self.product_ref)
        if risk_summary.residual_risk > riskThreshold:
            pytest.fail(
                f"Product {self.product_ref} has risk {risk_summary.residual_risk} and is over the threshold {riskThreshold}")
