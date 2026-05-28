Data Source Probe
Source name: World Bank World Development Indicators (WDI)
Access method: Direct bulk download — no API key, no login required
URL / endpoint: https://databank.worldbank.org/data/download/WDI_excel.zip
File committed to repo: data/Unemployment.xlsx
Download date: 2026-04-08 (recorded in workbook row 2: "Last Updated Date")
Licence: Creative Commons Attribution 4.0 International (CC BY 4.0)

One-row proof — India (IND), year 2015
  -      Indicator                                         WB Code     
- Unemployment  total (% of total labor force)       SL.UEM.TOTL.ZS7.629  
- GDP per capita growth (annual %)                   NY.GDP.PCAP.KD.ZG6.716 
- Inflation, consumer prices (annual %)              FP.CPI.TOTL.ZG4.907
- Industry, value added (% of GDP)                   NV.IND.TOTL.ZS27.347 
- Trade (% of GDP)                                   NE.TRD.GNFS.ZS41.923 
- Foreign direct investment, net inflows (% of GDP)  BX.KLT.DINV.WD.GD.ZS2.092 
- Labor force participation rate (% of total pop)    SL.TLF.ACTI.ZS55.422 %Urban 
- population (% of total population)                 SP.URB.TOTL.IN.ZS32.547 
- School enrollment, tertiary (% gross)              SE.TER.ENRR27.285 
- Urban Population growth (annual %)                 SP.POP.GROW1.193 

All ten values were read directly from data/Unemployment.xlsx at rows matching
Country Code = IND and column header 2015. No external call was made at
probe time; the file is committed to the repo.

Full coverage summary (years 2000–2023, all countries including aggregates)

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

World Bank aggregate and regional rows (WLD, HIC, SSA, etc.) are excluded during
panel construction using the fixed WB_AGGREGATES list in main.py, leaving
185 sovereign countries in the final cleaned panel.

Workbook structure

Header rows: 3 metadata rows before the data header

Row 1: Data Source | World Development Indicators
Row 2: Last Updated Date | 2026-04-08
Row 3: (blank)
Row 4: Country Name | Country Code | Indicator Name | Indicator Code | 2000 | 2001 | … | 2024


Year columns: integers 2000–2024 (code uses 2000–2023 only)
One indicator per sheet — each sheet has exactly one Indicator Code

How to re-download

Visit https://databank.worldbank.org/source/world-development-indicators
Select "Download" → "Excel" to get WDI_excel.zip
Extract and save the relevant workbook as data/Unemployment.xlsx in the repo root
No credentials required; the bulk download is publicly accessible

Notes

gdp_per_capita_growth used in modelling is derived in code as the
year-on-year pct_change() of GDP per capita growth values within each
country — it is not a separate sheet.
The FDI variable is sign-log transformed (np.sign(x) * np.log1p(abs(x)))
before modelling to handle heavy right skew and negative reversal values.
First observations per country are excluded from the hypothesis test (where
pct_change() returns NaN), and remaining growth values are winsorised at
the 5th / 95th percentile to remove currency-rebase artifacts.

Replace this file with a real probe once your source is live.
