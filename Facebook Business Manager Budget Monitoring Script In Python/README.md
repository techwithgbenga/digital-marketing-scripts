# Facebook-Business-Manager-Budget-Monitoring-Script

Facebook Business Manager Budget Monitoring via API which enable businesses to monitor low budget in facebook business manager. The aim of this short python script is to provide easy & extensible marketing tool for digital marketers and businesses.

#Story

I was trying to get the total remaining budget in a business manager so i can track when budget is low and quickly top up, But unfurtunately Facebook does not create any function to get that information, you can only get amount at ad account level. I search through the internet looking for a solution and i also seek help on the Facebook Cumminity and what am mostly getting is not what am willing to hear. But really needed the solution for my business, since i know there was no solution out there i started finding out how Facebook budget calculation works and now i could come up with the solution to get this data which i believe is very useful to businesses expecially digital marketers that have access to hude Add account manage with a single payment. 

#Problem the script would solve
1. Low Facebook budget might lead to Facebook blocking of your payment card
2. Ad might stop running which is not good for business

#Initial Setup

i. FACEBOOK 
* Crate a facebook application at http://developers.facebook.com/apps 
* Create/Setup your facebook ads account and get ads account id You need valid/live ACCESS TOKEN, use https://developers.facebook.com/tools/explorer/ to generate ACCESS TOKEN for FMA APP with ads_management permission By default facebook access is short lived approximately for 2 minutes, you can extend ACCESS TOKEN for 60 days for better application working at https://developers.facebook.com/tools/accesstoken/ Provide app_id & app_secret

ii. TWILIO 

* Create an account at https://www.twilio.com/ 
* Get a phone number or use default number for testing 
* Get credential from their setting tab

Install Python on your laptop and install all the needed packages.

#Getting Started
1. Confirure all needed information including Facebook API and Twilio API credentials.
2. Host bm_balance_report.py script on any python server or setup job cron on local system.

#THANK YOU

#Need any help 
visit: https://gbenga.afenuvon.com/
