import pandas as pd
import re
import os
from collections import defaultdict

TEST_DIR = "data/dataset/test"
OUTPUT = "output/candidate_pairs.tsv"

S1_FILE = f"{TEST_DIR}/test_source1.tsv"
S2_FILE = f"{TEST_DIR}/test_source2.tsv"
S3_FILE = f"{TEST_DIR}/test_source3.tsv"

MAX_POSTINGS = 100

os.makedirs("output", exist_ok=True)


def norm(x):
    if pd.isna(x):
        return ""
    x = str(x).lower()
    x = re.sub(r"[^\w\s]", " ", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x


def tokens(x):
    return [t for t in x.split() if len(t) >= 3]


def build_index(df):
    indexes = {
        "exact": defaultdict(list),
        "prefix6": defaultdict(list),
        "token": defaultdict(list),
    }

    for i, row in enumerate(df.itertuples(index=False)):

        country = norm(row.country)
        name = norm(row.business_name)

        if not country:
            continue

        base = country + "|" + name

        if name:
            indexes["exact"][base].append(i)

            if len(name) >= 6:
                indexes["prefix6"][
                    country + "|" + name[:6]
                ].append(i)

            for tok in set(tokens(name)):
                indexes["token"][
                    country + "|" + tok
                ].append(i)

    return indexes


def generate(source_file, source_name, s1):

    print()
    print("=" * 60)
    print(f"PROCESSING {source_name}")
    print("=" * 60)

    df = pd.read_csv(
        source_file,
        sep="\t",
        dtype=str,
        keep_default_na=False
    )

    print(f"{source_name} rows: {len(df):,}")

    print("Building index...")
    indexes = build_index(df)
    print("Index ready.")

    rows = []

    for n, row in enumerate(s1.itertuples(index=False), 1):

        country = norm(row.country)
        name = norm(row.business_name)

        candidate_ids = set()

        # Exact normalized name
        if name:
            key = country + "|" + name
            for idx in indexes["exact"].get(key, [])[:MAX_POSTINGS]:
                candidate_ids.add(idx)

        # Name prefix
        if len(name) >= 6:
            key = country + "|" + name[:6]
            for idx in indexes["prefix6"].get(key, [])[:MAX_POSTINGS]:
                candidate_ids.add(idx)

        # Name tokens
        toks = sorted(
            set(tokens(name)),
            key=len,
            reverse=True
        )[:2]

        for tok in toks:
            key = country + "|" + tok

            for idx in indexes["token"].get(
                key, []
            )[:MAX_POSTINGS]:

                candidate_ids.add(idx)

        sid = row.entity_id

        for idx in candidate_ids:
            rows.append(
                (
                    source_name,
                    sid,
                    df.iloc[idx]["entity_id"]
                )
            )

        if n % 10000 == 0:
            print(
                f"{n:,}/{len(s1):,} | "
                f"candidates: {len(rows):,}"
            )

            if len(rows) >= 1_000_000:
                out = pd.DataFrame(
                    rows,
                    columns=[
                        "source",
                        "source1_entity_id",
                        "matched_entity_id"
                    ]
                )

                out.to_csv(
                    OUTPUT,
                    sep="\t",
                    index=False,
                    mode="a",
                    header=not os.path.exists(OUTPUT)
                )

                rows = []

    if rows:
        out = pd.DataFrame(
            rows,
            columns=[
                "source",
                "source1_entity_id",
                "matched_entity_id"
            ]
        )

        out.to_csv(
            OUTPUT,
            sep="\t",
            index=False,
            mode="a",
            header=not os.path.exists(OUTPUT)
        )


print("Loading Source 1...")

s1 = pd.read_csv(
    S1_FILE,
    sep="\t",
    dtype=str,
    keep_default_na=False
)

print(f"S1 rows: {len(s1):,}")

# IMPORTANT: start a completely fresh candidate file
if os.path.exists(OUTPUT):
    os.remove(OUTPUT)

generate(S2_FILE, "S2", s1)
generate(S3_FILE, "S3", s1)

print()
print("=" * 60)
print("CANDIDATE GENERATION COMPLETE")
print("=" * 60)
print(OUTPUT)