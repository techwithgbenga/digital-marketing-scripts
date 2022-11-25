# Facebook-Marketing-Automation-Using-Google-Sheet

Facebook Marketing Automation via API which enable businesses to respond to automate their marketing process.

The aim of this short python script is to provide easy & extensible interface to automate facebook marketing including pulling report from a single or multiple business managers into Google Sheet, cheching perfomance base on some predefine rule which can be updated, Sending message to administrator base on rules, Extending campaign budget and ending date.

Facebook Marketing Automation Using Googlesheet is just a basic script that can be updated to preference. The goal is to create guide for small businesses who are willing to automate workload in aspect of digital marketing.

#Initial Setup
1. FACEBOOK
Crate a facebook application at http://developers.facebook.com/apps
Create/Setup your facebook ads account and get ads account id
You need valid/live ACCESS TOKEN, use https://developers.facebook.com/tools/explorer/ to generate ACCESS TOKEN for FMA APP with ads_management permission
By default facebook access is short lived approximately for 2 minutes, you can extend ACCESS TOKEN for 60 days for better application working at https://developers.facebook.com/tools/accesstoken/
Provide app_id & app_secret

2. Google
Crate a google app at https://console.cloud.google.com/
Create a project and get api key and secret
Go to marketplace and and add Google Sheet API to the project
Download credential.json and replace with current one

3. Twilio
Create an account at https://www.twilio.com/
Get a phone number or use default number for testing
Get credential from their setting tab

4. Install Python on your laptop and install all the needed packages.

#Getting Started
1. Download and put credential.json ibn same directory as program files.
2. Setup your google sheet with template provided. You can uodate culumn as needed but please not that you would also need to update inside the program file. 
3. Confirure all needed information including Facebook API, Google API, Twilio API credentials.
4. Provide Google workbook name inside program file.
5. To pull report run facebook_ad_report_to_googlesheet_logic.py script and report will be pulled to googlesheet.
6. After analyzing report, to extend ads with New budget, Add New Daily Budget into Google Sheet Culumn
7. Then you can run the facebook_ad_extention_and_sms_notification_logic.py program to extend add and create new dayly budget.

#THANK YOU

#Need any help
visit: https://gbenga.afenuvon.com/

