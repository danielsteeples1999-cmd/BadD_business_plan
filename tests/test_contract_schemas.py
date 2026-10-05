import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"


def load_schema(filename: str) -> dict:
    return json.loads((CONTRACTS / filename).read_text(encoding="utf-8"))


def valid_market_result() -> dict:
    return {
        "experimentId": "MARKET-001",
        "status": "PROVEN",
        "evidence": [
            {
                "claim": "Example measured result",
                "level": "VERIFIED",
                "source": "Example source",
                "date": "2026-10-06",
                "geography": "Example geography",
            }
        ],
        "findings": ["Example finding"],
        "unknowns": [],
        "assumptions": [],
        "nextAction": "Collect another measurement",
    }


def valid_pricing_scenario() -> dict:
    return {
        "currency": "USD",
        "scenarios": [
            {
                "name": "Example plan",
                "price": 9.99,
                "billing": "monthly",
                "includedValue": ["Example feature"],
                "confidence": "INFERRED",
            }
        ],
        "assumptions": ["Example assumption"],
    }


class ContractSchemaTests(unittest.TestCase):
    def validator(self, filename: str) -> Draft202012Validator:
        return Draft202012Validator(load_schema(filename))

    def assert_validation_error(self, validator, instance: dict, keyword: str) -> None:
        errors = [error for error in validator.iter_errors(instance) if error.validator == keyword]
        self.assertTrue(errors, f"Expected a JSON Schema {keyword!r} validation error")

    def test_both_contracts_are_valid_draft_2020_12_schemas(self) -> None:
        for filename in ("market-result.schema.json", "pricing-model.schema.json"):
            with self.subTest(filename=filename):
                Draft202012Validator.check_schema(load_schema(filename))

    def test_market_result_accepts_a_valid_instance(self) -> None:
        self.assertTrue(self.validator("market-result.schema.json").is_valid(valid_market_result()))

    def test_market_result_rejects_a_missing_required_field(self) -> None:
        instance = valid_market_result()
        del instance["nextAction"]
        self.assert_validation_error(self.validator("market-result.schema.json"), instance, "required")

    def test_market_result_rejects_an_unsupported_evidence_level(self) -> None:
        instance = valid_market_result()
        instance["evidence"][0]["level"] = "CONFIRMED"
        self.assert_validation_error(self.validator("market-result.schema.json"), instance, "enum")

    def test_pricing_model_accepts_a_valid_instance(self) -> None:
        self.assertTrue(self.validator("pricing-model.schema.json").is_valid(valid_pricing_scenario()))

    def test_pricing_model_rejects_a_negative_price(self) -> None:
        instance = valid_pricing_scenario()
        instance["scenarios"][0]["price"] = -0.01
        self.assert_validation_error(self.validator("pricing-model.schema.json"), instance, "minimum")

    def test_pricing_model_rejects_an_unsupported_billing_period(self) -> None:
        instance = valid_pricing_scenario()
        instance["scenarios"][0]["billing"] = "weekly"
        self.assert_validation_error(self.validator("pricing-model.schema.json"), instance, "enum")


if __name__ == "__main__":
    unittest.main()
