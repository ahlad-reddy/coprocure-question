import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json

r = requests.get('https://www.sourcewell-mn.gov/cooperative-purchasing/022217-wex#tab-contact-information')
soup = BeautifulSoup(r.content)

header = soup.findAll(attrs={"class":"vendor-contract-header__content"})
header_items = list(header.stripped_strings)
title = header_items[1]
vendor_name = header_items[2]
expiration = datetime.strptime(header_items[3].strip('Maturity Date: '), '%m/%d/%Y').isoformat()
contract_number = header_items[2].strip('#')

pattern = re.compile(r'Contract Form')
contract_forms = soup.findAll('a', text=pattern)[0]['href']

contact_information = soup.findAll(id="tab-contact-information")[0]
vendor_contact = contact_information.findAll('article', attrs={"class":"contract-marketing"})[0]
contact_items = list(vendor_contact.stripped_strings)
name = contact_items[0]
phone = contact_items[2]
email = contact_items[4]

parsed_data = {
	"title": title,
	"expiration": expiration,
	"contract_number": contract_number,
	"files": [
		{
			"contract-forms": contract_forms
		}
	],
	"vendor": {
		"name": vendor_name,
		"contacts": [
			{
				"name": name,
				"phone": phone,
				"email": email
			}
		]
	}
}

with open('data.json', 'w') as outfile:
    json.dump(parsed_data, outfile)


