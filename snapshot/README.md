---
title: bostrom final snapshot
tags: cyber, bootloader
crystal-type: source
crystal-domain: cyber
---
# bostrom final snapshot

the bootloader chain halted at height 25120712 (2026-08-05 08:55 UTC) and is being laid to rest. this directory holds the extraction scripts that produced the final public snapshot — anyone with an archive node can reproduce every file.

## datasets

| file | contents | source |
|------|----------|--------|
| cyberlinks_indexed.csv | particle_from, particle_to, neuron, height, timestamp, tx_hash | cyberindex postgres (heights ≤ 23465699) |
| graph_export.json | the complete graph from final state (2,949,732 links) | `cyber export` at halt height |
| balances.csv | address, denom, amount — BOOT, H, A, V, TOCYB, PUSSY (ibc), LP + factory denoms | LCD denom_owners |
| supply.json | total supply per denom | LCD |
| denom_traces.json | ibc denom hash → base denom mapping | LCD |
| pools.json | all liquidity pools: reserves + implied prices at halt | LCD + reserve accounts |
| passports.jsonl | nickname, owner, avatar/extension (addresses, resolvers) — 47,837 moon passports | cw721 `bostrom1xut80d0…zhxel` |
| delegations.csv | delegator, validator, shares, boot | LCD staking |
| validators.json | validator set with metadata | LCD staking |
| pubkeys.csv | address → public key (for future claims) | LCD auth |
| manifest.json | sha256 + size of every file, halt height, method | this repo |

## reproduce

```bash
# next to a bostrom archive node with LCD on :1317
python3 extract.py supply && python3 extract.py pools && python3 extract.py balances
python3 extract.py staking && python3 extract.py pubkeys
PASSPORT=bostrom1xut80d09q0tgtch8p0z4k5f88d3uvt8cvtzm5h3tu3tsy4jk9xlsfzhxel python3 extract.py passport
python3 extract.py manifest
```

the full graph comes from state export on the stopped node:

```bash
docker stop bostrom_arch && docker run --rm -v /path/to/.cyber:/root/.cyber <image> cyber export > state_export.json
```

## why

[[bostrom]] taught the [[collective focus theorem]] everything it knows: 3.1M particles, 2.9M cyberlinks, ~70K neurons, 47,837 passports. the knowledge moves to [[soft3]]; the chain rests. published on IPFS so the record outlives every server.
