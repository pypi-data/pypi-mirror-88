===================
django-slack-logger
===================

   Django errors to Slack channel.

Quick start
-----------

1. Add "django-slack-logger" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-slack-logger',
    ]

2. Config::

    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXXX/XXXX/XXXX"

     1. To create slack app goto `https://api.slack.com/apps` and create new app
     2. In `Create a Slack App` popup enter App Name you want. and select workspace
			and click on Create App.
     3. After creating app under `Add features and functionality` tab click on `Incoming Webhooks` and make it turn on 
     4. Click on "Add New Webhook to Workspace" in new page select channel to post to as an app
     5. Copy `Webhook URL` and set to **SLACK_WEBHOOK_URL** 
	
    SLACK_ERROR_LEVEL** = ["ERROR", "CRITICAL"] # only this logs are send to slack channel "*" for all 


    SLACK_WITH_EMAIL = False # if you want logs in mail default `False` - This will requires email django email configuration to settings.py file


        EMAIL_HOST = 'smtp.gmail.com'
        EMAIL_PORT = 587
        EMAIL_HOST_USER = 'your@gmail.com'
        EMAIL_HOST_PASSWORD = 'password'
        EMAIL_USE_TLS = True
        ADMINS = [('Your Name', 'your@gmail.com'),]

    SLACK_SHORT_MESSAGE = False

