# CHF data project

Data collection exercise (Homework 1, item 4) for ME 405/505, Machine Learning for Engineers.

## Problem

Predict the critical heat flux (CHF) of flow boiling from the test conditions. CHF is the heat flux at which the boiling crisis starts and the wall temperature rises sharply. One row of the table is one CHF experiment. The inputs are the source, the test section geometry and the operating conditions. The target is the measured CHF (`chf_exp`).

## Data source

X. Zhao, *Data for: On the prediction of critical heat flux using a physics-informed machine learning-aided framework*, Mendeley Data, version 1 (2020), [doi:10.17632/5p5h37tyv7.1](https://doi.org/10.17632/5p5h37tyv7.1). License: CC BY 4.0.

The data are a compilation of 1865 experiments from 10 literature sources (tube, annulus and plate test sections), described in Table 1 of X. Zhao et al., Applied Thermal Engineering 164 (2020) 114540, [doi:10.1016/j.applthermaleng.2019.114540](https://doi.org/10.1016/j.applthermaleng.2019.114540). The original file is not changed.

## Folder structure

```
raw/         Data_CHF_Zhao_2020_ATE.csv   original file, unchanged
processed/   chf_clean.csv                cleaned table, made by the script
scripts/     clean_chf.py                 raw -> processed
metadata.yaml                             source, units, column meanings, checks, what is not known
README.md                                 this file
```

## Columns of the processed file

| column | unit | meaning |
|---|---|---|
| author | - | source experiment of the row (10 values) |
| geometry | - | tube, annulus or plate |
| pressure | MPa | pressure |
| mass_flux | kg/m2-s | mass flux |
| x_e_out | - | outlet equilibrium quality, negative means subcooled |
| D_e | mm | equivalent (hydraulic) diameter of the channel |
| D_h | mm | heated diameter of the channel |
| length | mm | heated length (assumed L_h) |
| repeated_row | - | 1 if the row repeats an earlier row in every column, 0 otherwise |
| chf_exp | MW/m2 | experimental critical heat flux (target) |

## What the script does

`scripts/clean_chf.py` reads the raw file and

- drops the `id` column, which is only a row number,
- removes the units from the column names (they are in `metadata.yaml`),
- adds the flag `repeated_row` for the 49 rows that repeat an earlier row,
- drops the one test with `mass_flux = 0`, which is pool boiling and not flow boiling,
- moves the target `chf_exp` to the last column.

To rebuild `processed/chf_clean.csv`, run `python scripts/clean_chf.py` (needs pandas). The script finds the folders from its own location, so it can be started from any folder.

## Known issues and open questions

- The working fluid is not stated in the data. It is assumed to be water, based on the references of the paper.
- Measurement uncertainties are not reported for most tests. The paper estimates 5 to 20 %.
- The repeated rows are kept and flagged, because it is not known if they are copies or real repeated runs. Keep them in the same split when training models.
- A few values are outside the ranges of Table 1 of the paper (24 tests with outlet quality above 0.2, 3 Peskov tests at 10 MPa, 1 Thompson test at -0.87, 3 Kossolapov tests with mass flux between 310 and 340). They are kept.
- One source (Thompson) has 1202 of the 1865 tests, so a model can learn the source instead of the physics. Split by source when building models.
