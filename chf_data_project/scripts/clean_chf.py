from pathlib import Path

import pandas as pd

# the repository folder is the parent of scripts/, so the script works from any folder
repo = Path(__file__).resolve().parent.parent

raw = pd.read_csv(repo / "raw" / "Data_CHF_Zhao_2020_ATE.csv")

# irrelevant: the id is only a row number
tests = raw.drop(columns="id")

# improper format: the units are in the column names, so they are moved to metadata.yaml
tests.columns = [name.split(" [")[0] for name in tests.columns]

# duplicated: it is not known if these are copies or real repeats, so they are kept and flagged
tests["repeated_row"] = tests.duplicated().astype(int)

# incorrect: mass flux = 0 is pool boiling, which does not belong in a flow boiling table
tests = tests[tests["mass_flux"] > 0].reset_index(drop=True)

# keep the target as the last column
tests["chf_exp"] = tests.pop("chf_exp")

(repo / "processed").mkdir(exist_ok=True)
tests.to_csv(repo / "processed" / "chf_clean.csv", index=False)
print("saved", tests.shape, "to processed/chf_clean.csv")
