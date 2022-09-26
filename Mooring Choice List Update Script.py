# This script is used to update the SMCRI OIMS Choice Lists that are used to populate the selections that are available 
# in the Mooring Pre-deployment Form and the Mooring Rollover Forms in Survey123

# The workflow is that when technicians add the details for a new deployment location to the various info_sheet.csv 
# files hosted in ArcGIS Online at nrf-saeon,.maps.arcgis.com, this script can be run to automatically  update the choice sheets used in survey123 
# with the details of the new deployment.

import pandas as pd
import tempfile
import os
from arcgis.gis import GIS
gis = GIS("home") # for when running this script within ArcGIS Online
# gis = GIS(url='https://nrf-saeon.maps.arcgis.com/', username='XXXXXX', password='XXXXXX') # for when running this script from a stand alone python environment

### Download all the hosted csv files from user content folder into a temporary folder in ArcGIS online

tmpdir = tempfile.TemporaryDirectory() # Make a temporary directory to store the csv files before we convert them into pandas data frames
download_folder = tmpdir.name #Create a downloads folder

#create variables for the different csv files hosted in arcgis online that we wish to download
choice = gis.content.search('c4be3ae7d91c46df841ac6f42d18c36c', item_type="CSV")[0]
sites = gis.content.search('6ad63238a4f64e27aa9e053a65f2c61c', item_type="CSV")[0]
utr = gis.content.search('085d85d71046499ba3e4beaecf1d7cfc', item_type="CSV")[0]
gtp = gis.content.search('a7b2324589e94a25af5bbd97083cd21e', item_type="CSV")[0]
ct =  gis.content.search('e1fb2b369ec44f66b282339679cc3d2a', item_type="CSV")[0]
adcp = gis.content.search('e213f7cafb7147b696fff69154c681d4', item_type="CSV")[0]

# Download the data to the temp folder
sites.download(download_folder)
utr.download(download_folder)
gtp.download(download_folder)
ct.download(download_folder)
adcp.download(download_folder)

### Convert the CSV files into Data Frames

# Sentinel Sites and Satellite Sentinel Sites
sites_choice_df = pd.read_csv(download_folder + '/sites_info_sheet.csv')
sites_choice_df['ListName'] = 'Sites'


# UTR
utr_info_df = pd.read_csv(download_folder + '/utr_info_sheet.csv')
utr_service_choice_df = utr_info_df[['site_code','service_group']].drop_duplicates()
utr_service_choice_df['name'] = utr_service_choice_df['service_group'].replace(' ', '_',regex=True)
utr_service_choice_df.rename(columns = {'site_code':'sites1', 'service_group':'label'}, inplace = True)
utr_service_choice_df['ListName'] = 'utr_service'
utr_mooring_df = utr_info_df[['mooring_code','label', 'service_group']].drop_duplicates()
utr_mooring_df['service_group'].replace(' ', '_',regex=True, inplace=True)
utr_mooring_df.rename(columns = {'mooring_code':'name','service_group':'utr_group'}, inplace = True)
utr_mooring_df['ListName'] = 'utr_mooring'

# GTP
gtp_info_df = pd.read_csv(download_folder + '/gtp_info_sheet.csv')
gtp_service_choice_df = gtp_info_df[['site_code','service_group']].drop_duplicates()
gtp_service_choice_df['name'] = gtp_service_choice_df['service_group'].replace(' ', '_',regex=True)
gtp_service_choice_df.rename(columns = {'site_code':'sites1', 'service_group':'label'}, inplace = True)
gtp_service_choice_df['ListName'] = 'gtp_service'

gtp_mooring_df = gtp_info_df[['mooring_code','label', 'service_group']].drop_duplicates()
gtp_mooring_df['service_group'].replace(' ', '_',regex=True, inplace=True)
gtp_mooring_df.rename(columns = {'mooring_code':'name','service_group':'gtp_group'}, inplace = True)
gtp_mooring_df['ListName'] = 'gtp_mooring'

# ADCP
adcp_info_df = pd.read_csv(download_folder + '/adcp_info_sheet.csv')
adcp_mooring_df = adcp_info_df[['mooring_code', 'mooring_name','site_code']].drop_duplicates()
adcp_mooring_df['ListName']= 'adcp_mooring'
adcp_mooring_df.rename(columns = {'mooring_code':'name','mooring_name': 'label','site_code':'sites1'}, inplace = True)

# CT_choices
ct_info_df = pd.read_csv(download_folder + '/ct_info_sheet.csv')
ct_service_choice_df = ct_info_df[['site_code','service_group']].drop_duplicates()
ct_service_choice_df['name'] = ct_service_choice_df['service_group'].replace(' ', '_',regex=True)
ct_service_choice_df.rename(columns = {'site_code':'sites1', 'service_group':'label'}, inplace = True)
ct_service_choice_df['ListName'] = 'ct_service'

ct_mooring_df = ct_info_df[['mooring_code','mooring_name', 'service_group']].drop_duplicates()
ct_mooring_df['service_group'].replace(' ', '_',regex=True, inplace=True)
ct_mooring_df.rename(columns = {'mooring_code':'name','mooring_name':'label','service_group':'ct_group'}, inplace = True)
ct_mooring_df['ListName'] = 'ct_mooring'

ct_reach_df = ct_info_df[['Reach_Code','Reach_Name', 'mooring_code']].drop_duplicates()
ct_reach_df.rename(columns = {'Reach_Code':'name','Reach_Name':'label','mooring_code':'ct_river'}, inplace = True)
ct_reach_df['ListName'] = 'ct_reach'

#Create the final Choice list by concatenating all the data frames
choiceList_df = pd.concat([sites_choice_df,utr_service_choice_df,utr_mooring_df,gtp_service_choice_df,gtp_mooring_df, adcp_mooring_df,ct_service_choice_df,ct_mooring_df,ct_reach_df])

#export the choice list from a dataframe into the temp folder
choiceList_df.to_csv(download_folder + '/choice_list.csv', index=False)
choicelist_temp = download_folder + '/choice_list.csv'

### Update the choice_list.csv hosted in ArcGIS Online
choice.update(data=choicelist_temp)
