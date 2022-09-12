# NirvanaIn.py
Add items to your To-do list app via Terminal 
Most big todo apps today allow for you to add an item to your task list via e-mail. This is a script that leverages that e-mail functionality, so that you can add todo list items from the command line. This helps to add tasks faster, without a context switch. 

<img src="https://github.com/tash-had/NirvanaIn.py/blob/master/logo.png" width="200" height="200">

## June 2, 2020 Update
A recent update in the Nirvana API makes it no longer possible for me to retrieve an access token. I've written a workaround which uses Nirvana's [add tasks via email](https://help.nirvanahq.com/category/getting-more-from-nirvana/add-your-items/#create-inbox-items-via-email) feature to add to your inbox. This adds a couple more steps to installation. 

## Usage
- ```nin Clean room```
- To add notes: ```nin mytask // note for mytask```

## Installation (5 minutes) 
### Create and Setup a Free SendGrid account
- Go [here](https://sendgrid.com/pricing/) and create a Free tier account and click the link in your email to confirm the account. 
- Create a [Sender Identity](https://app.sendgrid.com/settings/sender_auth/senders) on SendGrid. This is required to be able to send e-mails. You can choose "Single Sender Verification" and use an email from a free email service (hotmail, outlook, etc) for this. 
- Go [here](https://app.sendgrid.com/settings/api_keys) and generate an API Key. Save this key somewhere as you'll need it in later steps.

### Get your personal Nirvana Inbox Address
- Go [here](https://help.nirvanahq.com/category/getting-more-from-nirvana/add-your-items/#create-inbox-items-via-email) and follow the instructions to get your personal address. Store this somewhere (we'll use it later). 

### Setup
- Make sure you have ```requests``` and ```sendgrid``` installed. To install, run ```pip install requests sendgrid```
- Clone this repo
- Move it to a directory of your choice
- Navigate to it in Terminal
- Run ```python nirvana_in.py --install```
- Run ```nin --help``` for commands

**Not tested on Windows**

Not affiliated with NirvanaHQ. 
