## About
A script to query the official CSU [foreigners-in-the-Czech-Republic-by-end-of-2023 dataset](https://csu.gov.cz/produkty/cizinci-podle-statniho-obcanstvi-veku-a-pohlavi)
to fetch statistics about legally residing Russian citizens in the Czech Republic (visas over 12 months, residence permits of all kinds, no refugees).

## How to run it

1. `poetry install`
2. `poetry shell`
3. `python run.py`

This will generate a `reduced.csv` file with the totals per gender and age group.

## Data for year 2023

```
total_women,total_men,age_group
457,480,0-5
693,745,5-10
740,746,10-15
658,747,15-20
3382,2883,20-25
3611,2193,25-30
2609,1703,30-35
2160,1498,35-40
1540,1092,40-45
1331,927,45-50
1374,1072,50-55
1128,1117,55-60
1041,1035,60-65
776,662,65-70
533,398,70-75
389,241,75-80
239,116,80-85
334,129,85-N
```

![Legally residing Russian citizens by 31.12.2023](https://github.com/fernflower/countforeigners/blob/main/legally_residing_russians_31_12_2023.png)

[Data sheet](https://docs.google.com/spreadsheets/d/1-WxXXsSXVjLFv2PblPjA6fnSu9HOX_4ERtD-vqjOJys/)
