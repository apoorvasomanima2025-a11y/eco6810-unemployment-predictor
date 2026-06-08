Data Source Probe
Source name: World Bank World Development Indicators (WDI)
Access method: Direct bulk download — no API key, no login required
URL / endpoint: https://databank.worldbank.org/data/download/WDI_excel.zip
File committed to repo: data/Unemployment.xlsx
Download date: 2026-04-08 (recorded in workbook row 2: "Last Updated Date")
Licence: Creative Commons Attribution 4.0 International (CC BY 4.0)

One-row proof — India (IND), year 2015
All values read directly from data/Unemployment.xlsx at Country Code = IND, column 2015. No external call made at probe time.

  -      Indicator                                         WB Code     
- Unemployment  total (% of total labor force)       SL.UEM.TOTL.ZS
- GDP per capita growth (annual %)                   NY.GDP.PCAP.KD.ZG 
- Inflation, consumer prices (annual %)              FP.CPI.TOTL.ZG
- Industry, value added (% of GDP)                   NV.IND.TOTL.ZS
- Trade (% of GDP)                                   NE.TRD.GNFS.ZS
- Foreign direct investment, net inflows (% of GDP)  BX.KLT.DINV.WD.GD.ZS
- Labor force participation rate (% of total pop)    SL.TLF.ACTI.ZS
- population (% of total population)                 SP.URB.TOTL.IN.ZS
- School enrollment, tertiary (% gross)              SE.TER.ENRR
- Urban Population growth (annual %)                 SP.POP.GROW

All ten values were read directly from data/Unemployment.xlsx at rows matching
Country Code = IND and column header 2015. No external call was made at
probe time; the file is committed to the repo.

Full coverage — years 2000–2023, all 217 rows (incl. World Bank aggregates)

- Indicator                                   WB Code               obs  Countries
- Unemployment, total (% of total labor force) SL.UEM.TOTL.ZS        4484  217
- GDP per capita growth (annual %)             NY.GDP.PCAP.KD.ZG     4967  217 
- Inflation, consumer prices (annual %)        FP.CPI.TOTL.ZG        4345  217
- Industry value added (% of GDP)              NV.IND.TOTL.ZS        4686  217
- Trade (% of GDP)                             NE.TRD.GNFS.ZS        4252  217
- Foreign direct investment,(% of GDP)         BX.KLT.DINV.WD.GD.ZS  4634  217
- Labor force participation rate(% total pop)  SL.TLF.ACTI.ZS        4484  217
- Urban population (% of total  population)    SP.URB.TOTL.IN.ZS     5208  217
- School enrollment, tertiary (% gross)        SE.TER.ENRR           3087  217
- Urban Population growth (annual %)           SP.POP.GROW           5207  217

World Bank aggregate and regional rows (WLD, HIC, SSA, etc.) are excluded during panel construction using the fixed WB_AGGREGATES list in main.py, leaving 185 sovereign countries in the final cleaned panel.

Workbook structure
Header rows: 3 metadata rows before the data header

Row 1: Data Source | World Development Indicators
Row 2: Last Updated Date | 2026-04-08
Row 3: (blank)
Row 4 (index 3): Country Name | Country Code | Indicator Name | Indicator Code | 2000 | … | 2024


Year columns: integers 2000–2024 (code uses 2000–2023 only; header=3 in parse_sheet())
One indicator per sheet

How to re-download

Visit https://databank.worldbank.org/source/world-development-indicators
Select Download → Excel to get WDI_excel.zip
Extract and save as data/Unemployment.xlsx in the repo root
No credentials required

Transformations applied in main.py

fdi_inflows → sign-log transformed: np.sign(x) * np.log1p(abs(x)) before modelling, to handle heavy right skew and negative FDI reversal values.
gdp_per_capita_growth → read directly from sheet NY.GDP.PCAP.KD.ZG. This is a pre-computed annual % growth rate from the World Bank. No pct_change() is used, which eliminates the first-observation artifact (distorted median of −31.28%) present in earlier versions of the code.
Growth is winsorised at the 5th/95th percentile before the hypothesis test to remove any remaining currency-rebase outliers.
