import re
import pandas as pd


POSTCODE_REGEX = re.compile(
    r'\b((?:GIR\s?0AA|[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}))\b',
    flags=re.IGNORECASE)


def normalise_names(names: pd.Series) -> pd.Series:
    """
    Tidy a pandas Series of strings by removing leading/trailing whitespace,
    converting to lowercase, and replacing multiple spaces with a single space.
    """
    return names.str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)


def split_address(series: pd.Series) -> pd.DataFrame:
    s = (series
         .str.upper()
         .str.replace(r'\s+', ' ', regex=True)
         .str.strip())

    postcodes = s.str.extract(POSTCODE_REGEX, expand=False)

    # Keep postcode in canonical form: force single space before last 3 chars
    postcodes = (postcodes
                 .str.replace(r'\s+', '', regex=True)
                 .str.replace(r'(.+)(\w{3})$', r'\1 \2', regex=True))

    addresses = (s
                 .str.replace(POSTCODE_REGEX, '', regex=True)
                 .str.strip()
                 .str.replace(r'\s{2,}', ' ', regex=True))

    return pd.DataFrame({'address_no_postcode': addresses,
                         'postcode': postcodes})


def normalise_addresses(address: pd.Series) -> pd.Series:
    """
    Normalise a pandas Series of addresses by

    1. stripping leading/trailing whitespace
    2. removing all punctuation
    3. converting to lowercase
    4. collapsing runs of whitespace to a single space
    """

    # 1. Trim surrounding whitespace
    normalized = address.str.strip()

    # 2. Drop punctuation (anything that is not a word-char or whitespace)
    normalized = normalized.str.replace(r'[^\w\s]', '', regex=True)

    # 3. Lower-case everything
    normalized = normalized.str.lower()

    # 4. Replace multiple spaces (or tabs/newlines) with a single space
    normalized = normalized.str.replace(r'\s+', ' ', regex=True)

    return normalized

