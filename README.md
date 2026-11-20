# Sunflower Storm Research Professor Package

## Updated five-stage canopy dataset

[Download the cleaned canopy dataset ZIP](https://github.com/usman-sarwar-rajput/sunflower-storm-evidence/raw/refs/heads/main/Sunflower_Canopy_Cleaned_Dataset.zip). Extract it inside this repository to access `datasets/canopy_hailstorm_2016/README.md`, the data and the validator. The archive includes the full cleaned canopy and weather series, the four-date subset, source workbook, five-stage Excel/CSV tables, results, field documentation and integrity hashes.

The [documented 2016 canopy release](Sunflower_Canopy_Cleaned_Dataset.zip) includes 192 source-checked observations, a five-stage table with plot identifiers, an Excel workbook, source attribution, validation code and checksums. **No storm-day canopy values are available; these data do not measure head movement or establish prediction.**

Start with **papers/Sunflower_Storm_Evidence_Paper.docx**. This is a historical case study and evidence review, with reproducible results and a protocol for a future storm-warning experiment.

## Main finding

Green canopy cover declined from 82.53% to 50.09% after documented hail on 19 August 2016. The difference was −32.44 percentage points, and all 48 paired plots declined. The canopy interval brackets one shared storm. It does not record head direction or storm anticipation. The three-day comparison preserves the lack of canopy data during the storm day and the three following days. The first post-hail reading was on day four.

Two independent baselines quantify what can be measured: 384 projected stem-angle observations from six young plants, and 514 paired head-inclination estimates from a USDA methods study. Neither provides repeated head angles linked to local storm onset. No advance-warning model or storm p-value is reported.

## Files

| Folder | Contents |
|---|---|
| papers | Editable research paper with methods, statistical results, phase comparisons, figures, conclusion, and research recommendations |
| inputs | Seven original source files, including downloaded workbooks and USDA CSVs and methods |
| cleaned | Plant or plot observations and daily weather; separate populations retained |
| results | Three- and five-period daily/summary tables, paired hail results, comparisons across all consecutive sampling intervals, weather joins, angle method agreement, and validation |
| figures | Four figures, including local rainfall and canopy chronology |
| code | Offline analysis script |
| protocol | Analysis rules, key field definitions, and blank field data collection headers |

## Run it

Use Python 3.12. From the extracted package directory:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe code\analyse.py
```

The initial dependency installation may require internet access. The analysis itself runs offline. Do not edit the bundled input files: the script checks their SHA-256 hashes. It rebuilds the cleaned tables, results, and figures. The Word paper documents the validated release and is not rewritten by the analysis script.

## Attribution

- USDA ARS, Colorado Sunflower Water Use, Physiology and Productivity Data Set, [version 2](https://doi.org/10.15482/USDA.ADC/28586066.v2), U.S. Public Domain.
- DeValk et al., [head inclination study](https://doi.org/10.1002/agj2.21708), [USDA dataset](https://doi.org/10.15482/USDA.ADC/27119340.v1), CC0. The original workbook is preserved under a shorter filename.
- Brooks, Atamian and Harmer, [PLOS Biology article](https://doi.org/10.1371/journal.pbio.3002344), [S13 Data](https://doi.org/10.1371/journal.pbio.3002344.s025); retain original author attribution.

The original studies collected the measurements. This package adds source checks, cleaned tables, event alignment, calculations, figures, and a research interpretation. It does not apply a new blanket license to the input files.

## Cleaned data at a glance

| File | What it contains | Source |
|---|---|---|
| [juvenile_stem_angles.csv](cleaned/juvenile_stem_angles.csv) | Projected stem angles for young plants | Brooks et al., S13 Data |
| [head_inclination_method_comparison.csv](cleaned/head_inclination_method_comparison.csv) | Paired measurements from two inclination methods | DeValk et al., USDA |
| [canopy_plot_observations.csv](cleaned/canopy_plot_observations.csv) | Plot-level green canopy cover | USDA Colorado field trial |
| [station_daily_weather.csv](cleaned/station_daily_weather.csv) | Daily station weather for environmental comparison | USDA Colorado field trial |

See the [field dictionary](protocol/DATA_DICTIONARY.csv), [analysis protocol](protocol/ANALYSIS_PROTOCOL.md), [source checksums](SOURCE_MANIFEST.json), and [validation results](results/validation_and_findings.json). Each table represents a separate source population or measurement method. Only the Colorado canopy observations were matched to the documented hail event.

## Reuse

The Colorado field-trial files are marked U.S. public domain by USDA. The DeValk dataset is CC0. The Brooks et al. workbook and cleaned stem-angle series are attributed to the original authors under the PLOS Creative Commons Attribution terms. The project renamed the source workbook and derived a tidy CSV. Cite the original sources when reusing the measurements. No additional license is asserted for third-party material.
