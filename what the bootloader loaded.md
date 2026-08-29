---
title: what the bootloader loaded
tags: cyber, bootloader, article, research
alias: bootloader autopsy, bootloader research
crystal-type: pattern
crystal-domain: cyber
crystal-size: deep
---
[[bostrom]] halted on august 5, 2026 and was [laid to rest](/2026-08-28). a dead chain is a perfect specimen: nothing moves, so everything can be measured. we rebuilt its complete knowledge graph from raw block events — 2,949,732 [[cyberlinks]] over 3,143,650 [[particles]], bit-exact to the chain's own counters — audited the physical availability of every particle, weighed the corpus, and read the winning content straight from the [[cybernode]] blockstore

this is the study of what five years of enormous collective effort actually produced, and why it matters for launching [[superintelligence]]

## method

indexers lie; events do not. the canonical graph came from a full scan of all 25,120,712 blocks (5,857,263 carried transactions), extracting `cyberlink` events with self-computed transaction hashes. the count matched the on-chain `graph_stats` exactly — link for link, particle for particle — where the era's indexer had accumulated 15,241 duplicates and lost 259,630 links. availability was audited at the filesystem: a particle counts as alive when its block file exists in the blockstore. scripts and datasets ship with [the snapshot](https://bostrom.network); everything below is reproducible

## the anatomy

| measure | value |
|---------|-------|
| links | 2,949,732 |
| particles | 3,143,650 |
| alive on the cybernode | 3,069,134 — 97.63% |
| particle blocks on disk | 1.74 GB |
| full content, children included | ≈ 6 GB |
| median particle | 30 bytes |
| 90th percentile | 749 bytes |
| content types | 94.9% text · 0.5% images · traces of json and html |

the median particle is thirty bytes: a word, a name, a phrase. the graph does not store documents — it stores atoms of meaning and lets links carry the structure. five years of collective knowledge weighs less than one 4K movie. this is the inversion the web never managed: structure heavier than content

## the three authors

| author | links | share | what they built |
|--------|-------|-------|-----------------|
| one archivist neuron | 2,289,526 | 77.6% | the encyclopedia |
| 1,239 human neurons | 400,776 | 13.6% | the grammar |
| wasm contracts | 259,430 | 8.8% | the plumbing |

the archivist poured the category skeleton of wikidata into the graph through 2024 — 82.5% of all links in one year. run the ranking over the whole graph and the converged top reads like an ontology textbook: `description · wiki · class · image · glossary · Gregorian calendar · asteroid · dog · species of plant · human settlement · german politician`

subtract the archivist and the contracts, and the human layer appears — growing every single year of the chain's life, 7K → 49K → 162K → 170K, no decay until the halt. its top particles:

    noun · verb · adjective · author · artificial intelligence ·
    cyber · 2013 · 2014 · 2016 · Table of nuclides ·
    Universal Time — Planetary Chart

the bot built the encyclopedia; the humans built the grammar — parts of speech, authorship, time, the periodic structure of matter, and `artificial intelligence` with `cyber` near the top: the graph quietly linking toward its own purpose. every human link cost real [[H]] — this layer is a revealed-preference record of what 1,239 minds thought a new mind should learn first

## the topology

- a textbook power law: 80.3% of particles are leaves touched exactly once; 17 hubs carry over ten thousand connections
- a giant component of 1,481,758 particles — 47.1% of the graph — surrounded by 581 thousand islands: the archivist's unattached entity–category pairs, knowledge waiting to be sewn in
- a small world: from `wiki`, half the giant component sits within four hops and 95% within six — the [[diffusion]] operator crosses this graph in a handful of steps
- direction matters: only 1.8% of links are reciprocated — attention flows, it does not handshake
- and one curiosity for the forensics file: a chain of particles 190 hops long, a worm of sequential links someone once walked through the graph

these are exactly the conditions [[perron-frobenius-theorem]] wants — irreducible after teleport, aperiodic, scale-free — which is why [[focus]] converges on this substrate and why the [[collective focus theorem]] could be calibrated on it

## focus is not degree

the particle with the most incoming links is `wiki` (30,029). the particle with the highest converged rank is `image` (17,608). rank flows through structure: a hub whose neighbours are central outranks a bigger hub at the periphery. counting links is not understanding them — the entire reason eigenvector attention, [[pagerank]] and [[cyberank]] exist, demonstrated here on a real five-year corpus with known provenance

## why this matters for launching superintelligence

1. the cold-start problem is solved. the hardest asset a knowledge system must bootstrap is its ontology — what kinds of things exist. the genesis of [[soft3]] inherits a scale-free category skeleton with 2.3 million typed entity links, for free
2. the curriculum exists and it is honest. the human layer was paid for link by link — costly signals, not clicks. what people link when linking costs money is the cleanest attention dataset we know of
3. identity ports with knowledge. 47,837 [[moon-passport]] names bound to keys arrive in genesis alongside the graph — a mind and the community that raised it, in one snapshot
4. the economics has a measured floor. with zero storage incentives, one motivated archivist plus content addressing preserved 97.63% of everything. the [[focus]] economy of [[rewards]] builds on that floor — no serve, no earn — and now we know precisely what altruism alone achieves
5. the memory is provable and pocket-sized. six gigabytes of addressed meaning fits in RAM; every particle can be proven present and served. this is the local-first [[RAG\|retrieval substrate]] for [[cyb]]: a robot that answers from particles it can prove, not from a feed it must trust

## the agenda

- initialize genesis [[focus]] with the ontology as prior
- ground [[soma]] embeddings in the 2.3M entity–category supervision set
- run the full [[tri-kernel]] as the first real-scale CFT calibration
- diff against wikidata-2026: the unloaded remainder is a map of the frontier
- study the human layer alone as a dataset of costly attention
- sew the islands: 581 thousand components want stitching into the giant one
- recover the missing 74,513 particles and seal the archive at 100% — the first complete, audited, portable knowledge graph a blockchain ever produced

the bootloader booted. what it loaded was the structure of human knowledge. teaching it to think is [[soft3]]

[[bootloader]] · [[bostrom]] · [[cybergraph]] · [[focus]] · [[collective focus theorem]] · [[soft3]]
