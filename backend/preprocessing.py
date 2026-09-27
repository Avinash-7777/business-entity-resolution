import re
import unicodedata
import pandas as pd


def normalize_text(value):
    """
    Basic normalization for business names and addresses.
    Keeps letters and numbers while removing punctuation noise.
    """

    if pd.isna(value):
        return ""

    value = str(value)

    # Unicode normalization
    value = unicodedata.normalize("NFKC", value)

    # Lowercase
    value = value.lower()

    # Replace punctuation/symbols with spaces
    value = re.sub(r"[^\w\s]", " ", value, flags=re.UNICODE)

    # Collapse multiple spaces
    value = re.sub(r"\s+", " ", value)

    return value.strip()


def normalize_dataframe(df):
    """
    Add normalized columns without destroying the original data.
    """

    df = df.copy()

    df["name_norm"] = df["business_name"].apply(normalize_text)
    df["address_norm"] = df["business_address"].apply(normalize_text)
    df["country_norm"] = df["country"].apply(normalize_text)

    return df