# addressmatch

A small command-line tool for cleaning and deduplicating restaurant names and addresses.

---

## Installation

```bash
pip install -e .   # from the project root
```

---

## Quick start

```bash
# 1. Clean raw CSV data → normalised files
addressmatch clean <input_csv> <output_dir>

# 2. Deduplicate one postcode-outcode bucket
addressmatch dedupe <input_dir> <output_dir> <OUTCODE> \
                 [--name-threshold 0.1] [--address-threshold 0.1]
```

Example:

```bash
addressmatch clean   data/input/restaurants.csv  data/normalised
addressmatch dedupe  data/normalised            data/output      N1
```

---

## Command reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `clean` | `<input_csv>` – path to raw CSV with `name,address` columns  <br>`<output_dir>` – directory to write cleaned CSVs | • Adds deterministic `id` column  <br>• Normalises `name` and `address`  <br>• Splits `postcode` / `outcode` and expands common abbreviations |
| `dedupe` | `<input_dir>` – directory produced by **clean**  <br>`<output_dir>` – where to write deduped CSV  <br>`<OUTCODE>` – postcode outcode (e.g. `N1`)  <br>`--name-threshold` *(float)* – cosine-similarity cut-off for names  <br>`--address-threshold` *(float)* – cosine-similarity cut-off for addresses | • Builds similarity graph and groups duplicates  <br>• Emits CSV `<OUTCODE>.csv` with new `group_id` column |

---

## Output structure

```
output_dir/
└── N1.csv   # deduped records with `group_id`
```

Each `group_id` denotes one cluster of duplicate rows (same restaurant).

---

## License

MIT
