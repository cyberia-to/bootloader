import unittest

from extract import delegation_row, passport_record


class PassportRecordTests(unittest.TestCase):
    def test_builds_record_from_nickname_and_nft_info(self):
        info = {"access": {"owner": "bostrom1owner"},
                "info": {"extension": {"trait": "x"}, "token_uri": "ipfs://abc"}}
        rec = passport_record("42", info)
        self.assertEqual(rec, {
            "nickname": "42",
            "owner": "bostrom1owner",
            "extension": {"trait": "x"},
            "token_uri": "ipfs://abc",
        })

    def test_missing_extension_and_token_uri_become_none(self):
        info = {"access": {"owner": "bostrom1owner"}, "info": {}}
        rec = passport_record("7", info)
        self.assertIsNone(rec["extension"])
        self.assertIsNone(rec["token_uri"])


class DelegationRowTests(unittest.TestCase):
    def test_row_shape_matches_csv_header_order(self):
        d = {"delegation": {"delegator_address": "bostrom1del", "shares": "1000.0"},
             "balance": {"amount": "999"}}
        self.assertEqual(
            delegation_row(d, "bostromvaloper1val"),
            ["bostrom1del", "bostromvaloper1val", "1000.0", "999"],
        )

    def test_validator_address_comes_from_the_argument_not_the_delegation(self):
        d = {"delegation": {"delegator_address": "bostrom1del", "shares": "1"},
             "balance": {"amount": "1"}}
        row = delegation_row(d, "bostromvaloper1other")
        self.assertEqual(row[1], "bostromvaloper1other")


if __name__ == "__main__":
    unittest.main()
