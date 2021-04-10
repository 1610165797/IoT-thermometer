import requests
import json

def vacc_init():
	params={'country':'US','ab':'US','continent':'North America',}
	response = requests.get('https://covid-api.mmediagroup.fr/v1/vaccines', params)
	if response.status_code == 200:
		data = response.json()
		vacc_partial=json.dumps(data["United States"]["All"]["people_partially_vaccinated"])
		print("US Vaccinated: "+vacc_partial)
		return "US Vaccinated: "+vacc_partial
	else:
		print('error: got response code %d' % response.status_code)
		print(response.text)
		return None

MY_APP = {
    'name': 'Vaccine Rate',
    'init': vacc_init
}

if __name__ == '__main__':
	vacc_init()