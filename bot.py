from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools
from constants import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json

class LunchBot:
	def __init__(self):
		self.update_users()
		with open('users.json', 'r') as f:
			self.users = json.load(f)['users']

	def get_responses(self):
		store = file.Storage('token.json')
		creds = store.get()
		if not creds or creds.invalid:
		    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
		    creds = tools.run_flow(flow, store)
		service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
		form_id = SINGLE_USE_FORM_ID
		result = service.forms().responses().list(formId=form_id).execute()
		return result['responses']

	def update_users(self):
		arr = []
		responses = self.get_responses()
		for response in responses:
			def get(key): return response['answers'][key]['textAnswers']['answers'][0]['value']
			obj = {'studentID': get('608b39ce'),
				   'firstName': get('0fac20ba'),
				   'lastName': get('410b8bea'), 
				   'isVegetarian': True if get('66eebd65') == 'Yes' else False,
				   'isOptedIn': True if get('0f51ac6f') == 'Opt-in' else False}
			arr.append(obj)
		json_out = json.dumps({'users': arr}, indent=4)
		with open('users.json', 'w') as f:
			f.write(json_out)

	def print_users(self):
		for user in self.users:
			print(user)		
			
	def order(self):
		for user in self.users:
			if user['isOptedIn']:
				options = webdriver.ChromeOptions()
				options.add_argument('incognito')
				options.add_argument('headless')
				options.add_argument('disalbe-gpu')
				driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
				driver.get(FORM_URL)
				input_txt = [user['studentID'], user['firstName'], user['lastName'], '1', '00']
				txt_fields = driver.find_elements(By.CLASS_NAME, 'whsOnd')
				radio_buttons = driver.find_elements(By.CLASS_NAME, 'AB7Lab')
				arrow = driver.find_element(By.CLASS_NAME, 'e2CuFe')
				actions = ActionChains(driver)
				for i in range(len(txt_fields)):
					actions.click(on_element=txt_fields[i])
					actions.send_keys(input_txt[i])
				actions.click(on_element=radio_buttons[0])
				actions.click(on_element=radio_buttons[2] if user['isVegetarian'] else radio_buttons[2])
				actions.click(on_element=arrow)
				actions.pause(DELAY)
				actions.key_down(Keys.ARROW_DOWN)
				actions.pause(DELAY)
				actions.key_down(Keys.ENTER)
				actions.pause(DELAY)
				actions.key_down(Keys.TAB)
				actions.pause(DELAY)
				actions.key_down(Keys.ENTER)
				actions.perform()

if __name__ == '__main__':
	bot = LunchBot()
	bot.order()
