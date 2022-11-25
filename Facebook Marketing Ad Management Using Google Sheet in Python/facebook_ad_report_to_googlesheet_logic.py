import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials
from facebook_business.adobjects.business import Business
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.user import User
from datetime import datetime, time
import time
import os


# connecting to google sheet API using .json credentials
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credential = ServiceAccountCredentials.from_json_keyfile_name(
    "credential.json", scope)
client = gspread.authorize(credential)


# Facebook App access token, app secret and app id
access_token = '<access_token>'
app_secret = '<app_secret>'
app_id = '<app_id>'


# Get multiple Business Account ID - You can just use only one business Id depending on you use case
business_id_one = "<business_id_one>"
business_id_two = "<business_id_two>"
business_id_three = "<business_id_three>"
business_id_four = "<business_id_four>"

# Geting all Ad Account ID under selected business ID as stated above
ad_account_id_one = '<ad_account_id_one>'
ad_account_id_two = '<ad_account_id_two>'
ad_account_id_three = '<ad_account_id_three>'

FacebookAdsApi.init(app_id, app_secret, access_token)

# Opening Google Sheet workbook to select sheet 1
facebook_automation_sheet = client.open("<Google_Sheet_Name>").sheet1
# getting the values in list of dictionaries
facebook_automation_data = facebook_automation_sheet.get_all_records()

# getting the header of the sheet
header_list = facebook_automation_sheet.row_values(1)

# Getting Business Manager Name Column From Sheet
business_manager_name_index = header_list.index("Business Manager Name")
business_manager_name_value = facebook_automation_sheet.col_values(
    business_manager_name_index + 1)

# Getting Business Manager ID Column From Sheet
business_manager_id_index = header_list.index("Business Manager ID")
business_manager_id_value = facebook_automation_sheet.col_values(
    business_manager_id_index + 1)

# Getting Ads Account Name Column From Sheet
ads_account_name_index = header_list.index("Ads Account Name")
ads_account_name_value = facebook_automation_sheet.col_values(
    ads_account_name_index + 1)

# Getting Ads Account Name Column From Sheet
ads_account_id_index = header_list.index("Ads Account ID")
ads_account_id_value = facebook_automation_sheet.col_values(
    ads_account_id_index + 1)

# Getting Campaign Name Column From Sheet
campaign_name_index = header_list.index("Campaign Name")
campaign_name_value = facebook_automation_sheet.col_values(
    campaign_name_index + 1)

# Getting Campaign ID Column From Sheet
campaign_id_index = header_list.index("Campaign ID")
campaign_id_value = facebook_automation_sheet.col_values(campaign_id_index + 1)

# Getting Ad sets Name Column From Sheet
adsets_name_index = header_list.index("Ad sets Name")
adsets_name_value = facebook_automation_sheet.col_values(adsets_name_index + 1)

# Getting Ad sets ID Column From Sheet
adsets_id_index = header_list.index("Ad sets ID")
adsets_id_value = facebook_automation_sheet.col_values(adsets_id_index + 1)

# Getting This Period Date Start Column From Sheet
date_start_index = header_list.index("This Period Date Start")
date_start_value = facebook_automation_sheet.col_values(date_start_index + 1)

# Getting This Period Date Stop Column From Sheet
date_stop_index = header_list.index("This Period Date Stop")
date_stop_value = facebook_automation_sheet.col_values(date_stop_index + 1)

# Getting Time of Program Running Column From Sheet
program_running_index = header_list.index("Time of Program Running")
program_running_value = facebook_automation_sheet.col_values(
    program_running_index + 1)

# Getting Last Period Purchase Running Column From Sheet
last_period_purchase_index = header_list.index("Last Period Purchase")
last_period_purchase_value = facebook_automation_sheet.col_values(
    last_period_purchase_index + 1)

# Getting Last Period Spend Column From Sheet
last_period_spend_index = header_list.index("Last Period Spend")
last_period_spend_value = facebook_automation_sheet.col_values(
    last_period_spend_index + 1)

# Getting This Period Impression Column From Sheet
this_period_impressions_index = header_list.index("This Period Impressions")
this_period_impressions_value = facebook_automation_sheet.col_values(
    this_period_impressions_index + 1)

# Getting Landing Page View Column From Sheet
this_period_landing_index = header_list.index("This Period Landing")
this_period_landing_value = facebook_automation_sheet.col_values(
    this_period_landing_index + 1)

# Getting This Period Purchase Column From Sheet
this_period_purchase_index = header_list.index("This Period Purchase")
this_period_purchase_value = facebook_automation_sheet.col_values(
    this_period_purchase_index + 1)

# Getting This Period Spent Column From Sheet
period_spent_index = header_list.index("This Period Spent")
period_spent_value = facebook_automation_sheet.col_values(
    period_spent_index + 1)

# Getting This Period Daily Spent Column From Sheet
period_daily_spent_index = header_list.index("This Period Daily Spent")
period_daily_spent_value = facebook_automation_sheet.col_values(
    period_daily_spent_index + 1)

# Getting Total Lifetime Budget Column From Sheet
total_lifetime_budget_index = header_list.index("Total Lifetime Budget")
total_lifetime_budget_value = facebook_automation_sheet.col_values(
    total_lifetime_budget_index + 1)

# Getting Total Lifetime Budget Column From Sheet
budget_remaining_index = header_list.index("Budget Remaining")
budget_remaining_value = facebook_automation_sheet.col_values(
    budget_remaining_index + 1)

# Getting Next Period Date Stop Column From Sheet
next_period_date_stop_index = header_list.index("Next Period Date Stop")
next_period_date_stop_value = facebook_automation_sheet.col_values(
    next_period_date_stop_index + 1)

# Getting New Daily Budget Column From Sheet
new_daily_budget_index = header_list.index("New Daily Budget")
new_daily_budget_value = facebook_automation_sheet.col_values(
    new_daily_budget_index + 1)

# Getting New Lifetime Budget Added Column From Sheet
new_lifetime_budget_added_index = header_list.index(
    "New Lifetime Budget Added")
new_lifetime_budget_added_value = facebook_automation_sheet.col_values(
    new_lifetime_budget_added_index + 1)

# Getting New Total Budget Column From Sheet
new_total_budget_index = header_list.index("New Total Budget")
new_total_budget_value = facebook_automation_sheet.col_values(
    new_total_budget_index + 1)

# Setting Field and Paramenter to get all Business Manager
fields1 = [
    'name',
    'id',
    'business'
]
params1 = {
    'effective_status': ['ACTIVE', 'PAUSED'],
}

# Get all Business Manager
business_manager_one = Business(business_id_one).get_owned_ad_accounts(
    fields=fields1, params=params1, )
business_manager_two = Business(business_id_two).get_owned_ad_accounts(
    fields=fields1, params=params1, )
business_manager_three = Business(business_id_three).get_owned_ad_accounts(fields=fields1,
                                                                           params=params1, )
business_manager_four = Business(business_id_four).get_owned_ad_accounts(fields=fields1,

                                                                         params=params1, )
# Setting Fields and Parameter to get Insight.
fields = [
    'account_id',
    'account_name',
    'campaign_id',
    'campaign_name',
    'adset_id',
    'adset_name',
    'spend',
    'impressions',
    'actions',
]
params = {
    'date_preset': 'this_week_sun_today',
    # 'date_preset': 'last_week_mon_sun'
    # 'date_preset': 'last_7d'
    # 'date_preset': 'this_week_mon_today'
    # 'time_range': {'since':'2020-8-16','until':'2020-8-17'},
    'level': 'adset',
}

# Getting all Add Account Insight value in a list of Dictionaries
ad_account_one_insight = AdAccount(
    ad_account_id_one).get_insights(fields=fields, params=params, )
ad_account_two_insight = AdAccount(
    ad_account_id_two).get_insights(fields=fields, params=params, )
ad_account_three_insight = AdAccount(
    ad_account_id_three).get_insights(fields=fields, params=params, )


# Saving all Needed Ad account in a list to dynamically loop through
all_adsets_data = [ad_account_one_insight, ad_account_two_insight]

# looping through all business account and and saving id in an empty list
first_adaccount_id = []
for business_1 in business_manager_one:
    first_adaccount_id.append(business_1['id'])

second_adaccount_id = []
for business_2 in business_manager_two:
    second_adaccount_id.append(business_2['id'])

third_adaccount_id = []
for business_3 in business_manager_three:
    third_adaccount_id.append(business_3['id'])

forth_adaccount_id = []
for business_4 in business_manager_four:
    forth_adaccount_id.append(business_4['id'])

# Setting Time Fomat to suit facebook requirement
datetimeFormat = '%Y-%m-%dT%H:%M:%S+0100'

row = 1  # Initializing rows
cells = []  # initializing cells for updating data to google sheet
api_calls = 0
time_elapse = 0


facebook_campaign_list = []

for index in range(len(all_adsets_data)):

    start_time = time.time()  # Getting program start time

    # Looping through all Ads Account dynamically using index to Running Logic on its Ad sets
    for key1 in all_adsets_data[index]:

        # Checking What Business Account Own an Ad set or Ad Account
        if 'act_' + key1['account_id'] in first_adaccount_id:
            business_id = business_1['business']['id']
            business_name = (business_1['business']['name'])
        elif 'act_' + key1['account_id'] in third_adaccount_id:
            business_id = business_2['business']['id']
            business_name = (business_2['business']['name'])
        elif 'act_' + key1['account_id'] in second_adaccount_id:
            business_id = business_3['business']['id']
            business_name = (business_3['business']['name'])
        elif 'act_' + key1['account_id'] in forth_adaccount_id:
            business_id = business_4['business']['id']
            business_name = (business_4['business']['name'])

        # Getting/Reading Some information From Ad Set using the Adset Id
        adset = AdSet(key1['adset_id'])

        fields3 = [
            AdSet.Field.lifetime_budget,
            AdSet.Field.end_time,
            AdSet.Field.budget_remaining,
        ]
        # User api_get Instead of romote_read
        adset_values = adset.api_get(fields=fields3)

        # Setting up Parameters and Field to Get Last Week Insight Running From Sunday - Saturday
        fields4 = [
            'actions',
            'spend',
        ]
        params4 = {
            'date_preset': 'last_week_sun_sat',
        }
        last_week_data = adset.get_insights(fields=fields4, params=params4)

        if len(last_week_data) > 0:
            last_week_trimed_data = last_week_data[0]
            last_week_spend = last_week_trimed_data['spend']

            # Looping through last_week_data action and getting site purchase
            for last_week_action in last_week_trimed_data['actions']:
                if last_week_action['action_type'] == "purchase":
                    last_purchase = int(last_week_action['value'])
                elif last_week_action['action_type'] == None:
                    last_purchase = 0

        # Looping through recent week action and getting landing page view and site purchase
        for action_value in key1['actions']:
            if action_value['action_type'] == "landing_page_view":
                landing_page_view = int(action_value['value'])
            elif action_value['action_type'] == None:
                landing_page_view = 0

            if action_value['action_type'] == "purchase":
                ad_purchase = int(action_value['value'])
            elif action_value['action_type'] == None:
                ad_purchase = 0

        # Appending values to cells and updating to google sheet.
        cells.append(
            Cell(row=row + 1, col=business_manager_name_index + 1, value=business_name))
        cells.append(
            Cell(row=row + 1, col=business_manager_id_index + 1, value=business_id))
        cells.append(
            Cell(row=row + 1, col=ads_account_name_index + 1, value=key1['account_name']))
        cells.append(Cell(row=row + 1, col=ads_account_id_index +
                     1, value=key1['account_id']))
        cells.append(Cell(row=row + 1, col=campaign_name_index +
                     1, value=key1['campaign_name']))
        cells.append(Cell(row=row + 1, col=campaign_id_index +
                     1, value=key1['campaign_id']))
        cells.append(Cell(row=row + 1, col=adsets_name_index +
                     1, value=key1['adset_name']))
        cells.append(Cell(row=row + 1, col=adsets_id_index +
                     1, value=key1['adset_id']))
        cells.append(Cell(row=row + 1, col=date_start_index +
                     1, value=key1['date_start']))
        cells.append(Cell(row=row + 1, col=date_stop_index + 1,
                     value=adset_values['end_time']))  # adset_values['end_time']
        cells.append(
            Cell(row=row + 1, col=program_running_index + 1, value=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        cells.append(
            Cell(row=row + 1, col=last_period_purchase_index + 1, value=last_purchase))
        cells.append(
            Cell(row=row + 1, col=last_period_spend_index + 1, value=last_week_spend))
        cells.append(Cell(
            row=row + 1, col=this_period_impressions_index + 1, value=key1['impressions']))
        cells.append(
            Cell(row=row + 1, col=this_period_landing_index + 1, value=landing_page_view))
        cells.append(
            Cell(row=row + 1, col=this_period_purchase_index + 1, value=ad_purchase))
        cells.append(
            Cell(row=row + 1, col=period_spent_index + 1, value=key1['spend']))
        cells.append(Cell(row=row + 1, col=period_daily_spent_index + 1, value=float(key1['spend']) / float((((datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d') -
                                                                                                               datetime.strptime(key1['date_start'], '%Y-%m-%d')).days) + ((datetime.strptime(datetime.now().strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime('08:00:00', '%H:%M:%S')).total_seconds()/3600)/16))))
        cells.append(Cell(row=row + 1, col=total_lifetime_budget_index +
                     1, value=int(adset_values['lifetime_budget'])))

        cells.append(Cell(row=row + 1, col=budget_remaining_index +
                     1, value=int(adset_values['budget_remaining'])))

        # Update All columns in google sheets using with cells values
        facebook_automation_sheet.update_cells(cells)

        row += 1   # Incrementing loop

        end_time = time.time()  # Getting program execution end time
        time_elapse += end_time - start_time  # Getting time Elapse
        api_calls += 1  # Incrementing Amounting of calls x2 call per loop

        # Checking if 100 calls already made and pause the program for some seconds using time elapse
        if api_calls == 99:
            if time_elapse < 100:
                time.sleep(120 - int(time_elapse))
            api_calls = 0
            time_elapse = 0
