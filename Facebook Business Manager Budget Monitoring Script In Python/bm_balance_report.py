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
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, time


# Facebook App access token, app secret and app id
access_token = '<access_token>'
app_secret = '<app_secret>'
app_id = '<app_id>'


# Get All Ad Account ID in BM i.e act_2408768415887341
account_id_one = '<account_id_one>'
account_id_two = '<account_id_two>'
account_id_three = '<account_id_three>'

FacebookAdsApi.init(app_id, app_secret, access_token)

# Connecting to Twilo account using Sid and Auth Token from twilio.com/console
account_sid = '<account_sid>'
auth_token = '<auth_token>'
twilio_client = Client(account_sid, auth_token)


def job_function():

    # Setting Fields and Parameter to get Insight.
    fields = [
        'account_id',
        'account_name',
        'spend',
    ]

    params = {
        'date_preset': 'lifetime',
        'level': 'account',
    }

    # Getting All the balance base on parameter - Unlimited ad account can me added
    account_one_balance = AdAccount(account_id_two).get_insights(
        fields=fields, params=params)
    account_two_balance = AdAccount(account_id_three).get_insights(
        fields=fields, params=params)
    account_three_balance = AdAccount(
        account_id_one).get_insights(fields=fields, params=params)

    all_accounts_balance = [account_one_balance,
                            account_two_balance, account_three_balance]

    for index in range(len(all_accounts_balance)):

        fields2 = [
            'spend',
            'account_name',
        ]

        params2 = {
            'date_preset': 'yesterday',
            'level': 'account'
        }

        for key in all_accounts_balance[index]:
            # Code to check Through
            fields1 = [
                AdAccount.Field.spend_cap,
            ]

            account = AdAccount('act_' + key['account_id'])
            spend_cap_data = account.api_get(fields=fields1, params=params)

            previous_day_spend = account.get_insights(
                fields=fields2, params=params2)

            formated_cap = spend_cap_data['spend_cap'][:-
                                                       2] + '.' + spend_cap_data['spend_cap'][-2:]

            remaining_balance = float(formated_cap) - float(key['spend'])

            # Setting Up all Ad Rules and sending whatsapp message using Twilio
            if (remaining_balance < float(previous_day_spend[0]['spend'])):
                # Send Message to administrator

                message = twilio_client.messages.create(
                    from_='whatsapp:<twilio_phone_number>',
                    body='*IMPORTANT*: Current Balance for ' + key['account_name'] + '* is *' + str(
                        remaining_balance) + ' lesser than yesterdays spent of *' + str(previous_day_spend[0]['spend']) + '* Please, recharge',
                    to='whatsapp:<administrators_phone_number>'
                )

            else:
                # Send Message to administrators
                message = twilio_client.messages.create(
                    from_='whatsapp:<twilio_phone_number>',
                    body='The Current Balance for ' + str(key['account_name']) + ' is *' + str(
                        remaining_balance) + '* and yesterdays spent was *' + str(previous_day_spend[0]['spend']) + '*',
                    to='whatsapp:<administrators_phone_number>'
                )

# Sheduller to run the program every 6 hours


sched = BlockingScheduler()

# Schedule job_function to be called every two hours
sched.add_job(job_function, 'interval', hours=6)

sched.start()
