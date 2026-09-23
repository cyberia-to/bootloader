import json
import os
import shutil
import tempfile
import unittest
from unittest import mock

import extract


class _OutDirTestCase(unittest.TestCase):
    """cmd_* functions write to the module-level OUT dir; point it at a
    scratch directory for the duration of each test."""

    def setUp(self):
        self._tmp = tempfile.mkdtemp()
        self._patch_out = mock.patch.object(extract, "OUT", self._tmp)
        self._patch_out.start()

    def tearDown(self):
        self._patch_out.stop()
        shutil.rmtree(self._tmp, ignore_errors=True)

    def read_json(self, name):
        with open(os.path.join(self._tmp, name)) as f:
            return json.load(f)


class CmdSupplyTests(_OutDirTestCase):
    def test_writes_the_paged_supply_list_verbatim(self):
        supply = [{"denom": "boot", "amount": "123"}, {"denom": "hydrogen", "amount": "7"}]
        with mock.patch("extract.paged", return_value=iter(supply)) as p:
            extract.cmd_supply()
        self.assertEqual(self.read_json("supply.json"), supply)
        self.assertEqual(p.call_args.args[0], "/cosmos/bank/v1beta1/supply")

    def test_empty_supply_still_writes_an_empty_list(self):
        with mock.patch("extract.paged", return_value=iter([])):
            extract.cmd_supply()
        self.assertEqual(self.read_json("supply.json"), [])


class CmdPoolsTests(_OutDirTestCase):
    def test_pool_price_and_reserves_come_from_the_balances_lookup(self):
        pool = {
            "id": "1",
            "reserve_account_address": "bostrom1reserve",
            "reserve_coin_denoms": ["boot", "hydrogen"],
            "pool_coin_denom": "pool1",
        }
        balances = {"balances": [{"denom": "boot", "amount": "100"}, {"denom": "hydrogen", "amount": "250"}]}
        with mock.patch("extract.paged", return_value=iter([pool])), mock.patch(
            "extract.get", return_value=balances
        ) as g:
            extract.cmd_pools()
        [written] = self.read_json("pools.json")
        self.assertEqual(written["reserves"], {"boot": "100", "hydrogen": "250"})
        self.assertEqual(written["price"], {"boot_in_hydrogen": 250 / 100})
        self.assertEqual(g.call_args.args[0], "/cosmos/bank/v1beta1/balances/bostrom1reserve")

    def test_a_reserve_denom_absent_from_balances_prices_as_none_not_a_crash(self):
        pool = {
            "id": "2",
            "reserve_account_address": "bostrom1empty",
            "reserve_coin_denoms": ["boot", "hydrogen"],
            "pool_coin_denom": "pool2",
        }
        with mock.patch("extract.paged", return_value=iter([pool])), mock.patch(
            "extract.get", return_value={"balances": []}
        ):
            extract.cmd_pools()
        [written] = self.read_json("pools.json")
        self.assertEqual(written["reserves"], {})
        self.assertIsNone(written["price"]["boot_in_hydrogen"])

    def test_multiple_pools_all_written_in_order(self):
        pools = [
            {"id": "1", "reserve_account_address": "a1", "reserve_coin_denoms": ["boot", "hydrogen"], "pool_coin_denom": "p1"},
            {"id": "2", "reserve_account_address": "a2", "reserve_coin_denoms": ["milliampere", "millivolt"], "pool_coin_denom": "p2"},
        ]
        with mock.patch("extract.paged", return_value=iter(pools)), mock.patch(
            "extract.get", return_value={"balances": []}
        ):
            extract.cmd_pools()
        written = self.read_json("pools.json")
        self.assertEqual([w["id"] for w in written], ["1", "2"])


if __name__ == "__main__":
    unittest.main()
