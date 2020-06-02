# NirvanaIn.py
Add items to your Nirvana Inbox via Terminal 

## June 2, 2020 Update
A recent update in the Nirvana API has ended support for the endpoint I was using to fetch the access token. My workaround uses Nirvana's [add tasks via email](https://help.nirvanahq.com/category/getting-more-from-nirvana/add-your-items/#create-inbox-items-via-email) feature. This adds a couple more steps to installation. 

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
- Restart your Terminal
- Run ```nin --help``` for commands
- When you run `nin mytask` for the first time, you will be asked for your SendGrid API Key and your Nirvana Inbox Address (which we obtained in earlier steps) 

**Not tested on Windows**

Not affiliated with NirvanaHQ. 

![Logo](https://github.com/tash-had/NirvanaIn.py/blob/master/logo.png?raw=true)
