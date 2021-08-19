import asyncio
import time
import os
import logging

from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from dotenv import load_dotenv
from chromedriver_py import binary_path

load_dotenv('.env')

Aternos_User = os.getenv('ATERNOS_USERNAME')
Aternos_Password = os.getenv('ATERNOS_PASSWORD')
Default_Server = os.getenv('DEFAULT_MC_SERVER').split('.', 1)[0]

URL = 'https://aternos.org/go/'

# Chrome variables
adblock = False  # For those with network wide ad blockers
headless = False  # If you want a headless window

options = webdriver.ChromeOptions()

if headless:
	options.add_argument('--headless')

options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
					 'Chrome/87.0.4280.88 Safari/537.36')

driver = webdriver.Chrome(options=options, executable_path=binary_path)


async def start_server():
	""" Starts the server by clicking on the start button. The try except part tries to find the confirmation button, and
	if it doesn't, it continues to loop until the confirm button is clicked """

	element = driver.find_element_by_id('start')
	element.click()

	await asyncio.sleep(3)

	# Hides the notification question
	driver.execute_script('hideAlert();')

	# Server state span
	while get_status() == 'Waiting in queue':
		# While in queue, check for the confirm button and try click it
		await asyncio.sleep(3)
		try:
			element = driver.find_element_by_id('confirm')
			element.click()
		except ElementNotInteractableException:
			pass


def get_status():
	""" Returns the status of the server as a string """
	return driver.find_element_by_class_name('statuslabel-label').text


def get_number_of_players():
	""" Returns the number of players as a string, Returns '-1' if offline """
	try:
		return driver.find_element_by_xpath(
			'/html/body/div[2]/main/section/div[3]/div[5]/div[2]/div[1]/div[1]/div[2]/div[2]').text
	except NoSuchElementException:
		return '-1'


def get_address():
	""" Returns the severs IP address """
	return driver.find_element_by_id('ip').text


def get_software():
	""" Returns the server software """
	return driver.find_element_by_id('software').text


def get_version():
	""" Returns the server version """
	return driver.find_element_by_id('version').text


def get_tps():
	""" Returns the server TPS Works; When the server is online, returns '-1' if offline """
	try:
		return driver.find_element_by_xpath(
			'/html/body/div[2]/main/section/div[3]/div[5]/div[2]/div[1]/div[3]/div[2]/div[2]').text
	except NoSuchElementException:
		return '-1'


def get_ram():
	try:
		return driver.find_element_by_xpath(
			'/html/body/div[2]/main/section/div[3]/div[5]/div[2]/div[1]/div[2]/div[2]/div[2]').text
	except NoSuchElementException:
		return '-1'


def get_server_info():
	""" Returns a string of information about the server. Returns: server_ip, server_status, number of players,
	software, version """
	return get_address(), get_status(), get_number_of_players(), get_software(), get_version(), get_tps(), get_ram()


def connect_account():
	""" Connects to the accounts through a headless chrome tab so we don't have to do it every time we want to start or
	stop the server """
	driver.get(URL)

	# Login to aternos
	element = driver.find_element_by_id('user')
	element.send_keys(Aternos_User)
	element = driver.find_element_by_id('password')
	element.send_keys(Aternos_Password)
	element = driver.find_element_by_id('login')
	element.click()
	time.sleep(2)

	element = driver.find_element_by_id('accept-choices')
	element.click()

	elements = driver.find_elements_by_class_name('server-name')

	for element in elements:
		if element.text == Default_Server.lower():
			element.click()

	time.sleep(2)

	# By-passes the 3 second adblock
	if adblock:
		adblock_bypass()

	logging.info('Aternos Tab Loaded')


def adblock_bypass():
	time.sleep(1)
	element = driver.find_element_by_class_name('far fa-sad-tear')
	element.click()
	time.sleep(3)
	logging.debug('Adblock Wall Bypassed')


async def stop_server():
	""" Stops server from aternos panel """
	element = driver.find_element_by_id('stop')
	element.click()

async def restart_server():
	""" Restarts server from aternos panel """
	element = driver.find_element_by_id('restart')
	element.click()


def quit_browser():
	""" Quits the browser driver cleanly """
	driver.quit()


def refresh_browser():
	driver.refresh()
