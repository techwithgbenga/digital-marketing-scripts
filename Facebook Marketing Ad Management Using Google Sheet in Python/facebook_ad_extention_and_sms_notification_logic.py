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
#from twilio.rest import Client
from datetime import datetime
import time
import os

# connecting to google sheet API using .json credentials
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
credential = ServiceAccountCredentials.from_json_keyfile_name(
    "credential.json", scope)
client = gspread.authorize(credential)

# Facebook App access token, app secret and app ID
access_token = '<access_token>'
app_secret = '<app_secret>'
app_id = '<app_id>'

# Connecting to facebook using App ID and App Secret
FacebookAdsApi.init(app_id, app_secret, access_token)


# Connecting to Twilo account using Sid and Auth Token from twilio.com/console
account_sid = '<account_sid>'
auth_token = '<auth_token>'
twilio_client = Client(account_sid, auth_token)

# Opening Googlesheet workbook to select sheet 1
facebook_automation_sheet = client.open("<Google_Sheet_Name>").sheet1
# getting the values in list of dictionaries
facebook_automation_data = facebook_automation_sheet.get_all_records()

# getting the header of the sheet
header_list = facebook_automation_sheet.row_values(1)

# Getting New Lifetime Budget Added Column From Sheet
new_lifetime_budget_added_index = header_list.index(
    "New Lifetime Budget Added")
new_lifetime_budget_added_value = facebook_automation_sheet.col_values(
    new_lifetime_budget_added_index + 1)

# Getting New Total Budget Column From Sheet
new_total_budget_index = header_list.index("New Total Budget")
new_total_budget_value = facebook_automation_sheet.col_values(
    new_total_budget_index + 1)

# Setting Time Format to suit Facebook Time Format
datetimeFormat = '%Y-%m-%dT%H:%M:%S+0100'

cells = []  # initializing cells for updating data to google sheet
index = 0
api_calls = 0
time_elapse = 0

for key in facebook_automation_data:

    start_time = time.time()  # Getting program start time

    if facebook_automation_data[index]["Next Period Date Stop"] and facebook_automation_data[index]["New Daily Budget"]:

        # Getting The Ad set Id
        adset = AdSet(facebook_automation_data[index]["Ad sets ID"])

        # Calculating New Lifetime Budget added
        days_amount = ((((datetime.strptime(facebook_automation_data[index]["Next Period Date Stop"], datetimeFormat) - datetime.strptime(facebook_automation_data[index]["Time of Program Running"], '%Y-%m-%d %H:%M:%S')).days) + (((datetime.strptime(str(
            datetime.strptime(facebook_automation_data[index]["Time of Program Running"], '%Y-%m-%d %H:%M:%S').time()), '%H:%M:%S') - datetime.strptime('08:00:00', '%H:%M:%S')).total_seconds()/3600)/16)) * (int(facebook_automation_data[index]["New Daily Budget"]))) * 100

        new_total_budget_added = int(
            float(days_amount)) - int(facebook_automation_data[index]["Budget Remaining"])

        # Calculating Total Lifetime Budget
        newly_total_budget = int(
            facebook_automation_data[index]["Total Lifetime Budget"]) + int(new_total_budget_added)

        # Updating New Lifetime Budget added and Total lifetime budget in Google sheet
        cells.append(Cell(
            row=index + 2, col=new_lifetime_budget_added_index + 1, value=new_total_budget_added))
        cells.append(
            Cell(row=index + 2, col=new_total_budget_index + 1, value=newly_total_budget))
        facebook_automation_sheet.update_cells(cells)

        # Calculating current Running sales Speed Starting from every sunday - from time of running program
        current_sales_speed = float(facebook_automation_data[index]["This Period Spent"]) / int(
            facebook_automation_data[index]["This Period Purchase"])

        # Calculating Last Week Sales Speed From Last week Sunday -  Last Week Saturday
        last_week_sales_speed = float(facebook_automation_data[index]["Last Period Spend"]) / int(
            facebook_automation_data[index]["Last Period Purchase"])

        # Setting Up all Ad Rules and sending whatsapp message using Twilio
        if (float(facebook_automation_data[index]["This Period Spent"]) / int(facebook_automation_data[index]["This Period Landing"])) > 60:
            # Send Message to administrators

            # Sending Message to Administrator
            message = twilio_client.messages.create(
                from_='whatsapp:<twilio_number>',
                body='The Cost Per Click (CPC) for ' +
                facebook_automation_data[index]["Ad sets Name"] +
                ' is higher than 60 Naira',
                to='whatsapp:<telephone_number>'
            )

        elif (float(facebook_automation_data[index]["This Period Spent"]) / int(facebook_automation_data[index]["This Period Landing"])) > 80:

            # Sending Message to Administrator
            message = twilio_client.messages.create(
                from_='whatsapp:<twilio_number>',
                body='The Cost Per Click (CPC) for ' +
                facebook_automation_data[index]["Ad sets Name"] +
                ' is higher than 60 Naira',
                to='whatsapp:<telephone_number>'
            )

        elif ((int(facebook_automation_data[index]["This Period Landing"]) / int(facebook_automation_data[index]["This Period Impressions"])) * 100) < 0.50:

            # Send Message to Administrator
            message = twilio_client.messages.create(
                from_='whatsapp:<twilio_number>',
                body='The Cost Per Click (CPC) for ' +
                facebook_automation_data[index]["Ad sets Name"] +
                ' is higher than 60 Naira',
                to='whatsapp:<telephone_number>'
            )

        elif ((int(facebook_automation_data[index]["This Period Landing"]) / int(facebook_automation_data[index]["This Period Impressions"])) * 100) < 0.30:

            # Sending Message to Administrator
            message = twilio_client.messages.create(
                from_='whatsapp:<twilio_number>',
                body='The Cost Per Click (CPC) for ' +
                facebook_automation_data[index]["Ad sets Name"] +
                ' is higher than 60 Naira',
                to='whatsapp:<telephone_number>'
            )

        elif (last_week_sales_speed * 100) - (current_sales_speed * 100) < 10:

            # Sending Message to Administrator
            message = twilio_client.messages.create(
                from_='whatsapp:<twilio_number>',
                body='The Cost Per Click (CPC) for ' +
                facebook_automation_data[index]["Ad sets Name"] +
                ' is higher than 60 Naira',
                to='whatsapp:<telephone_number>'
            )

        # Updating an adset end time with the new total lifetime budget
        adset.update({
            AdSet.Field.lifetime_budget: newly_total_budget,
            AdSet.Field.end_time: facebook_automation_data[index]["Next Period Date Stop"],
        })
        adset.remote_update()

    end_time = time.time()  # Getting program execution end time
    time_elapse += end_time - start_time  # Getting time Elapse

    index += 1  # Incrementing loop
    api_calls += 1  # Incrementing Amounting of calls x2 call per loop

    # Checking if 100 calls already made and pause the program for some seconds using time elapse
    if api_calls == 99:
        if time_elapse < 100:
            time.sleep(120 - int(time_elapse))
        api_calls = 0
        time_elapse = 0
