import pandas as pd
import requests
import streamlit as st
from PIL import Image

#THIS IS TO RETURN THE LUNA PRICE ON KW SALES

def return_luna_settlement(x):
    parse_list = []
    for value in list(x.values()):
        if 'denom' in value[0]:
                parse_list.append(value[0].get('amount'))

    return (max(parse_list) / 10**6)

#aesthetics
st.set_page_config(layout="wide")
faction_wars = Image.open("faction_wars.png")
st.image(faction_wars)
st.markdown("# COUNCIL - OPAL DUST PURCHASE TRACKING - STARTING 2/22/22")
st.text('Sorry for delays, takes about 1 minute to populate all the data')

#start data
re_dust_sales = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/e922f679-017a-4f37-a902-157ed9d68278/data/latest')
opal_token_id = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/06fc1811-4539-4d54-aa30-92aa2b3a8b34/data/latest')

re_merge_df = re_dust_sales.merge(opal_token_id['TOKEN_ID'], how='inner', on='TOKEN_ID')
re_merge_df['BLOCK_TIMESTAMP'] = pd.to_datetime(re_merge_df['BLOCK_TIMESTAMP'])
re_since_start = re_merge_df[re_merge_df['BLOCK_TIMESTAMP'] >= '2022-02-22'] #this marks the beginning of the wars

re_owner_list = []
for token_id in re_since_start['TOKEN_ID']:
    re_owner_list.append({'TOKEN_ID':token_id,
        'address':requests.get(f'https://fcd.terra.dev/wasm/contracts/terra1p70x7jkqhf37qa7qm4v23g4u4g8ka4ktxudxa7/store?query_msg=%7B%22owner_of%22:%7B%22token_id%22:%22{token_id}%22%7D%7D').json().get('result').get('owner')})

re_owner_id_df = pd.DataFrame(re_owner_list)
re_count_df = re_owner_id_df.groupby('address').count().reset_index()

re_faction_list = []
for address in re_count_df['address']:
    try:
        re_faction_list.append(requests.get(f'https://stations.levana.finance/api/factions?wallet={address}').json().get('wallet').get('faction'))
    except:
        re_faction_list.append('none')

re_address_faction = pd.concat([re_count_df, pd.DataFrame(re_faction_list)], axis = 1).rename(columns={0:'faction'})

st.title('RANDOMEARTH SALES')
st.dataframe(re_since_start)


kw_dust_sales = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/555a8db1-8640-416e-9c5b-1c4c7a6eca77/data/latest')
kw_dust_sales.rename(columns={'EVENT_ATTRIBUTES':'LUNA_PRICE'}, inplace=True)
kw_dust_sales['LUNA_PRICE'] = kw_dust_sales['LUNA_PRICE'].apply(lambda x: return_luna_settlement(x))

kw_merge_df = kw_dust_sales.merge(opal_token_id['TOKEN_ID'], how='inner', on='TOKEN_ID')
kw_merge_df['BLOCK_TIMESTAMP'] = pd.to_datetime(kw_merge_df['BLOCK_TIMESTAMP'])
kw_since_start = kw_merge_df[kw_merge_df['BLOCK_TIMESTAMP'] >= '2022-02-22'] #this marks the beginning of the wars
kw_since_start = kw_since_start.groupby('TX_ID').max().reset_index()

kw_owner_list = []
for token_id in kw_since_start['TOKEN_ID']:
    kw_owner_list.append({'TOKEN_ID':token_id,
        'address':requests.get(f'https://fcd.terra.dev/wasm/contracts/terra1p70x7jkqhf37qa7qm4v23g4u4g8ka4ktxudxa7/store?query_msg=%7B%22owner_of%22:%7B%22token_id%22:%22{token_id}%22%7D%7D').json().get('result').get('owner')})

kw_owner_id_df = pd.DataFrame(kw_owner_list)
kw_count_df = kw_owner_id_df.groupby('address').count().reset_index()

kw_faction_list = []
for address in kw_count_df['address']:
    try:
        kw_faction_list.append(requests.get(f'https://stations.levana.finance/api/factions?wallet={address}').json().get('wallet').get('faction'))
    except:
        kw_faction_list.append('none')

kw_address_faction = pd.concat([kw_count_df, pd.DataFrame(kw_faction_list)], axis = 1).rename(columns={0:'faction'})

st.title('KNOWHERE SALES')
st.dataframe(kw_since_start)


la_dust_sales = pd.read_json('https://api.flipsidecrypto.com/api/v2/queries/26121f5b-8ea0-4f03-a9c2-937254196fdc/data/latest')

la_merge_df = la_dust_sales.merge(opal_token_id['TOKEN_ID'], how='inner', on='TOKEN_ID')
la_merge_df['BLOCK_TIMESTAMP'] = pd.to_datetime(la_merge_df['BLOCK_TIMESTAMP'])
la_since_start = la_merge_df[la_merge_df['BLOCK_TIMESTAMP'] >= '2022-02-22']
la_since_start['TOKEN_ID'] = pd.to_numeric(la_since_start['TOKEN_ID'], downcast='integer')

la_owner_list = []
for token_id in la_since_start['TOKEN_ID']:
    la_owner_list.append({'TOKEN_ID':token_id,
        'address':requests.get(f'https://fcd.terra.dev/wasm/contracts/terra1p70x7jkqhf37qa7qm4v23g4u4g8ka4ktxudxa7/store?query_msg=%7B%22owner_of%22:%7B%22token_id%22:%22{token_id}%22%7D%7D').json().get('result').get('owner')})

la_owner_id_df = pd.DataFrame(la_owner_list)
la_count_df = la_owner_id_df.groupby('address').count().reset_index()

la_faction_list = []
for address in la_count_df['address']:
    try:
        la_faction_list.append(requests.get(f'https://stations.levana.finance/api/factions?wallet={address}').json().get('wallet').get('faction'))
    except:
        la_faction_list.append('none')

la_address_faction = pd.concat([la_count_df, pd.DataFrame(la_faction_list)], axis = 1).rename(columns={0:'faction'})

st.title('LUART SALES')
st.dataframe(la_since_start)


total_df = pd.concat([la_address_faction, re_address_faction, kw_address_faction]).groupby(['address', 'faction']).sum().reset_index()
total_df.rename(columns = {'TOKEN_ID':'Count of NFTs purchased'}, inplace=True)

st.title('ALL PURCHASES PER ADDRESS')
st.dataframe(total_df)
st.markdown(f"### There have been a total of {len(total_df)} unique addresses that have purchased Dust with Opal since the start of the Faction Wars")
st.markdown(f"### There have been a total of {sum(total_df['Count of NFTs purchased'])} NFTs purchased")

    