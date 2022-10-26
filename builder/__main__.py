from config import config
from helpers import csv_to_df, round_float
import os
import pandas as pd


# import data
gov_df = csv_to_df(config['gov_source_url'])
pulse_df = csv_to_df(config['pulse_source_url'])
dap_df = csv_to_df(config['dap_source_url'])
additional_data = pd.read_csv(config['additional_data_path'])
additional_data['source_manually_added'] = 'TRUE'

# create new snapshot directory and save snapshot of data, if necessary
todays_snapshot_path = config['todays_snapshot_path']
if os.path.exists(todays_snapshot_path) == False:
    os.makedirs(todays_snapshot_path)
    gov_df.to_csv(todays_snapshot_path + '/gov.csv', index=False)
    pulse_df.to_csv(todays_snapshot_path + '/pulse.csv', index=False)
    dap_df.to_csv(todays_snapshot_path + '/dap.csv', index=False)

# normalize columns
gov_df = gov_df.rename(columns={'Domain Name': 'target_url', 'Domain Type': 'branch', 'Agency': 'agency', 'Organization': 'bureau'})
gov_df['target_url'] = gov_df['target_url'].str.lower()
gov_df['base_domain'] = gov_df['target_url']
gov_df['source_list_federal_domains'] = 'TRUE'
# strip out 'Federal - ' leading string from domain type column for .gov data
gov_df['branch'] = gov_df['branch'].map(lambda x: x.lstrip('Federal - '))

pulse_df = pulse_df.rename(columns= {'Domain': 'target_url', 'Base Domain': 'base_domain', 'Agency': 'agency'})
pulse_df['source_list_pulse'] = 'TRUE'

dap_df = dap_df.rename(columns={'domain': 'target_url'})
dap_df['source_list_dap'] = 'TRUE'
dap_df['base_domain_pulse'] = dap_df['target_url'].map(lambda x: '.'.join(x.split('.')[-2:]))

# combine all URLs into one column
url_series = pd.concat([gov_df['target_url'], pulse_df['target_url'], dap_df['target_url'], additional_data['target_url']])
url_df = pd.DataFrame(url_series)

# remove duplicates
url_df = url_df.drop_duplicates('target_url')

# remove URLs with ignore-listed strings
ignore_df = pd.read_csv(config['ignore_list_path'])
ignore_series = ignore_df['URL begins with:']

for string in ignore_series:
    url_df = url_df[~url_df['target_url'].str.startswith(string)]

# merge data back in
url_df = url_df.merge(gov_df, on='target_url', how='left')
url_df = url_df.merge(pulse_df, on='target_url', how='left')
url_df = url_df.merge(dap_df, on='target_url', how='left')
url_df = url_df.merge(additional_data, on='target_url', how='left')
url_df = url_df.fillna('')

# populate base domain and agency columns
url_df['agency'] = ''
url_df['base_domain'] = ''

for tuple in url_df.iterrows():
    row = tuple[1]
    if row['base_domain_pulse'] != '':
        row['base_domain'] = row['base_domain_pulse']
    else:
        if row['base_domain_x'] != '':
            row['base_domain'] = row['base_domain_x']
        else:
            row['base_domain'] = row['base_domain_y']
    if row['agency_x'] == '':
        row['agency'] = row['agency_y']
    else:
        row['agency'] = row['agency_x']

# format source columns
url_df['source_list_federal_domains'] = url_df['source_list_federal_domains'].map(lambda x: 'FALSE' if x == '' else x)
url_df['source_list_pulse'] = url_df['source_list_pulse'].map(lambda x: 'FALSE' if x == '' else x)
url_df['source_list_dap'] = url_df['source_list_dap'].map(lambda x: 'FALSE' if x == '' else x)
url_df['source_manually_added'] = url_df['source_manually_added'].map(lambda x: 'FALSE' if x == '' else x)

# get relevant subset
url_df = url_df[['target_url', 'base_domain', 'branch', 'agency', 'bureau', 'source_list_federal_domains', 'source_list_pulse', 'source_list_dap', 'source_manually_added']]

# set branch column's value to 'Executive' if empty
url_df[['branch']] = url_df[['branch']].replace('', 'Executive')

# get lookup table of agencies mapped to base domain
agency_df = gov_df[['base_domain', 'agency']]
agency_df = agency_df.drop_duplicates()

# merge in agencies
url_df = url_df.merge(agency_df, on='base_domain', how='left')
url_df = url_df.fillna('')
url_df['agency'] = ''

for tuple in url_df.iterrows():
    row = tuple[1]
    if row['agency_x'] == '':
        row['agency'] = row['agency_y']
    else:
        row['agency'] = row['agency_x']

# get lookup table of bureaus mapped to base domain
bureau_df = gov_df[['base_domain', 'bureau']]
bureau_df = bureau_df.drop_duplicates()

# merge in bureaus
url_df = url_df.merge(bureau_df, on='base_domain', how='left')
url_df = url_df.fillna('')
url_df['bureau'] = ''

for tuple in url_df.iterrows():
    row = tuple[1]
    if row['bureau_x'] == '':
        row['bureau'] = row['bureau_y']
    else:
        row['bureau'] = row['bureau_x']

# load agency and bureau reference data
omb_df = csv_to_df(config['omb_source_url'])
agency_codes = omb_df[['Agency Name', 'Agency Code']]
agency_codes = agency_codes.rename(columns={'Agency Name': 'agency', 'Agency Code': 'agency_code'}).drop_duplicates()
bureau_codes = omb_df[['Bureau Name', 'Bureau Code']]
bureau_codes = bureau_codes.rename(columns={'Bureau Name': 'bureau', 'Bureau Code': 'bureau_code'}).drop_duplicates()

# add agency and bureau codes
url_df = url_df.merge(agency_codes, on='agency', how='left')
url_df = url_df.merge(bureau_codes, on='bureau', how='left')
url_df = url_df.drop_duplicates()
url_df = url_df.fillna('')

# format agency and bureau codes
url_df['agency_code'] = url_df['agency_code'].map(lambda x: round_float(x))
url_df['bureau_code'] = url_df['bureau_code'].map(lambda x: round_float(x))

# reorder columns, sort, and remove all non-.gov urls
url_df = url_df[['target_url', 'base_domain', 'branch', 'agency', 'agency_code', 'bureau', 'bureau_code', 'source_list_federal_domains', 'source_list_pulse', 'source_list_dap', 'source_manually_added']]
url_df = url_df.sort_values(by=['base_domain', 'target_url'])
url_df = url_df.drop_duplicates('target_url')
url_df = url_df[url_df.target_url.str.contains('.gov')]

# write list to csv
url_df.to_csv(config['target_url_list_path'], index=False)