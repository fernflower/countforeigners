"""
This script processes CSU 2023 dataset from https://csu.gov.cz/produkty/cizinci-podle-statniho-obcanstvi-veku-a-pohlavi
"""

import csv

import pandas

OUTPUT = 'reduced.csv'
OUTPUT_KEYS = ['total_women', 'total_men', 'age_group']
FILENAME = './OD_CIZ01_2024062613561450.csv'

# For more details and legend see ./290038-24schema2023.json
RECORD_KEYS = ['idhod', 'hodnota', 'stapro_kod', 'pohlavi_cis', 'pohlavi_kod', 'stobcan_cis', 'stobcan_kod', 'vek_cis',
               'vek_kod', 'rok', 'vuzemi_cis', 'vuzemi_kod', 'kraj_cis', 'kraj_kod', 'vuzemi_txt', 'kraj_txt',
               'pohlavi_txt', 'stobcan_txt', 'vek_txt']

MALE = 'muž'
FEMALE = 'žena'


def load_data(filename=FILENAME):
    return pandas.read_csv(filename)


def main():
    # age_group: female/male total
    total_per_age_group = {}

    data = load_data()
    # filter Russian citizens grouped per age (undefined kraj_kod means sum of child values)
    russians = data[(data['stobcan_txt'] == 'Rusko') & (data['vek_txt'].str.len() > 0) & (data['kraj_kod'].isnull())]

    def sort_by_age(series):
        """
        Must return one Series
        """
        return series.apply(lambda x: int(str(x).lstrip('<').split(';')[0]) if str(x) != 'nan' else 100)

    # order by age groups
    sorted_data = russians.sort_values(by='vek_txt', key=sort_by_age)

    # As I'm not a true data scientist let's resort to good old barbaric iterate over / calculate sums per group
    # without any pandas magic elegancy (suggestions welcome!)
    for index, row in sorted_data.iterrows():
        age_group = row['vek_txt']

        if age_group not in total_per_age_group:
            total_per_age_group[age_group] = {FEMALE: 0, MALE: 0}

        if row['pohlavi_txt'] == FEMALE:
            total_per_age_group[age_group][FEMALE] += row['hodnota']
        elif row['pohlavi_txt'] == MALE:
            # Will be negating male sums to draw nice pyramid-like structure
            row['hodnota'] *= -1
            total_per_age_group[age_group][MALE] += row['hodnota']
        else:
            continue
            # There are also rows where gender is set to NaN - that is essentially sum of MALE + FEMALE so skip
            # those

    # Now to control: total should match value in initial data with undefined kraj, undefined gender and undefined age
    control_sum = data[(data['stobcan_txt'] == 'Rusko') & (data['pohlavi_txt'].isnull()) &
                       (data['kraj_kod'].isnull()) & (data['vek_txt'].isnull())]
    assert len(control_sum.index) == 1
    grand_total = sum([abs(val[MALE]) + val[FEMALE] for age, val in total_per_age_group.items()])
    assert control_sum.iloc[0]['hodnota'] == grand_total

    with open(OUTPUT, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_KEYS)
        writer.writeheader()
        for age_group in total_per_age_group:
            interval = age_group.lstrip('<').rstrip(')').split(';')
            writer.writerow({'total_men': total_per_age_group[age_group][MALE], 
                             'total_women': total_per_age_group[age_group][FEMALE],
                             'age_group': f'{interval[0]}-{interval[1].strip()}'})




if __name__ == '__main__':
    main()
