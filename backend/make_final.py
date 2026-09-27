import csv
import os

CANDIDATE = "output/candidate_pairs.tsv"
S1_FILE = "data/dataset/test/test_source1.tsv"
OUTPUT = "output/matching_results.tsv"

MAX_MATCHES = 10

matches = {}

print("Reading S2 candidates...")

with open(CANDIDATE, "r", encoding="utf-8", buffering=1024 * 1024) as f:

    reader = csv.DictReader(f, delimiter="\t")

    count = 0

    for row in reader:

        sid = row["source1_entity_id"]
        mid = row["matched_entity_id"]

        if sid not in matches:
            matches[sid] = []

        if len(matches[sid]) < MAX_MATCHES:
            if mid not in matches[sid]:
                matches[sid].append(mid)

        count += 1

        if count % 5_000_000 == 0:
            print(
                f"Processed {count:,} candidates | "
                f"S1 with matches: {len(matches):,}"
            )

print()
print("Writing matching_results.tsv...")

with open(S1_FILE, "r", encoding="utf-8", buffering=1024 * 1024) as f, \
     open(OUTPUT, "w", encoding="utf-8", newline="") as out:

    reader = csv.DictReader(f, delimiter="\t")
    writer = csv.writer(out, delimiter="\t")

    writer.writerow([
        "source1_entity_id",
        "matched_entity_ids"
    ])

    total = 0
    nonempty = 0

    for row in reader:

        sid = row["entity_id"]
        ids = matches.get(sid, [])

        if ids:
            nonempty += 1

        writer.writerow([
            sid,
            ",".join(ids)
        ])

        total += 1

print()
print("DONE")
print(f"S1 rows: {total:,}")
print(f"S1 with matches: {nonempty:,}")
print(f"Output: {OUTPUT}")