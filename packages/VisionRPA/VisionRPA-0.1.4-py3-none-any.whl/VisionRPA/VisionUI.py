
from urllib.parse import urlencode
from urllib.request import Request,urlopen
import base64
import cv2
import pygetwindow as gw
import win32gui, win32con
from PIL import ImageGrab
import numpy as np
import json
import pandas as pd
import re,time
import pyautogui,gzip
import pygetwindow as gw
import logging
import win32com.client
# import logging

def get_all_active_app():
	top_windows = []
	return_app_list=[]
	win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	return_app_list=[i[1]  for i in top_windows if (i[1]!='' and i[1]!='MSCTFIME UI' and i[1]!='Default IME' and i[1]!='Message')]
	return return_app_list
def windowEnumerationHandler(hwnd, top_windows):
	    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))	
def take_screen_shot(application_name):
	    # global application_name
	    results = []
	    top_windows = []
	    find=False
	    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
	    for i in top_windows:
	        # print(i[1])
	        # print(top_windows) Sample Web Form - ClickDimensions - Google Chrome

	        if application_name in i[1]:

	            global hwnd,height,width,screenshot,X,Y
	            hwnd = win32gui.FindWindow(None, i[1])
	            if hwnd!=0:
		            window = gw.getWindowsWithTitle(application_name)[0] 
		            if window.isMinimized==True:
		            	window.restore() 
		            # try:
		            shell = win32com.client.Dispatch("WScript.Shell")
		            shell.SendKeys('%')
		            win32gui.SetForegroundWindow(hwnd)
		            if window.isMinimized==True:
		            	window.restore() 
		            win32gui.SetForegroundWindow(hwnd)
		            left_x, top_y, right_x, bottom_y = win32gui.GetWindowRect(hwnd)
		            if left_x>0:
		            	X=left_x
		            else:
		            	X=0	
		            if top_y>0:	
		            	Y=top_y
		            else:
		            	Y=0	
		            time.sleep(0.9)
		            screen = np.array(ImageGrab.grab(bbox=(left_x+6, top_y, right_x-6, bottom_y-6) ))
		            screenshot = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
		            cv2.imwrite('screenshot.jpg',screenshot)
		            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
		            height,width,_=img.shape
		            find=True
		            return [X,Y,img]
	            else:
	            	logging.error('application not open or not focusable')
	            	break  
	    if find==False:
	    	return[-1,-1]
	            	 
def Get_RT_app_elements(application_id, app_name):
	try:
		global application_name
		application_name=app_name
		start_coordinates=take_screen_shot(application_name)
		if start_coordinates[:2]!=[-1,-1]:
			img=start_coordinates[2]
			img_b64 = base64.b64encode(gzip.compress(img)).decode()
			api_data_json_form = {
			    "image_name":application_id,
			    "image": img_b64,
			    "shape": img.shape,
			}
			# addr="http://192.168.100.10:8000"
			addr="http://3.21.226.218:8000"
			test_url = addr + "/get_automation/"
			api_data_encoded = urlencode(api_data_json_form).encode("utf-8")
			responce_from_server = Request(test_url, api_data_encoded)
			responce_from_server = urlopen(responce_from_server)
			responce_decode = responce_from_server.read().decode("utf-8")
			responce_json_form = json.loads(responce_decode)
			# print(responce_json_form)
			

			if responce_json_form["data"]!='false':
				csv_data = pd.read_json(responce_json_form["data"])
				dic={'csv_data':csv_data,'coordinates':start_coordinates}
				return dic
			else:
			   logging.error('application content change')
			   return None	
		else:
			logging.error('Error application is not open or not in focus state')
			return None
	except:
		logging.error('Server did not responding ')
		return None
def draw_rectangle_on_UI_element(csv_data):
	csv_file=csv_data['csv_data']
	img=cv2.imread('screenshot.jpg')
	for index,el in csv_file.iterrows():
		remve_right=re.sub(r"\]"," ",str(el['combine_coordinates_label_UI']))
		rmv_left=re.sub(r"\["," ",remve_right)
		integer=np.fromstring(rmv_left,dtype=float,sep=",")
		[ box_x, box_y, box_w, box_h]=integer[:4]
		
		cv2.rectangle(img,(int(box_x), int(box_y)),(int(box_x + box_w), int(box_y + box_h)),(50, 255, 255),2,)
	cv2.imwrite('rectangle_screenShot.jpg',img)
def add_action(action,csv_data,app_name,index_no=None,label_=None,enter_text=None):
	if csv_data is not None:
		if enter_text is None and action.lower()!='click' :
			   logging.error('enter_text is None')
		elif label_ is None and index_no is None:
		       logging.error('label_ and index_no both None')	   
		else:	
			import time
			hwnd = win32gui.FindWindow(None,app_name)
			window = gw.getWindowsWithTitle(application_name)[0] 
			if window.isMinimized==True:
				window.restore() 
			shell = win32com.client.Dispatch("WScript.Shell")
			shell.SendKeys('%')
			win32gui.SetForegroundWindow(hwnd)
			if window.isMinimized==True:
				window.restore()
			win32gui.SetForegroundWindow(hwnd) 
			csv_file=csv_data['csv_data']
			[X,Y,_]=csv_data['coordinates']  
			for index,el in csv_file.iterrows():
				remve_right=re.sub(r"\]"," ",str(el['combine_coordinates_label_UI']))
				rmv_left=re.sub(r"\["," ",remve_right)
				integer=np.fromstring(rmv_left,dtype=float,sep=",")
				[ box_x, box_y, box_w, box_h]=integer[:4]
				box_x=box_x+(box_w/2)
				box_y=box_y
				# print('>>>>>>>>>',re.sub("[^A-Za-z0-9]+", "", el['label_text']))
				if action.lower()=='click' and re.sub("[^A-Za-z0-9]+", "", el['label_text'])==label_ or index==index_no and enter_text is None:
					label_=''
					time.sleep(1)
					if el['elements_class']=='Radio Button' or el['elements_class']=='Unfilled Radio Button':
						pyautogui.click(box_x, box_y)
					else:
						pyautogui.click(box_x, box_y)
					break
				elif enter_text is not None:
					if index_no is not None:
						if int(index_no)==int(index):
							time.sleep(0.7)
							pyautogui.click(box_x, box_y)
							time.sleep(0.7)
							pyautogui.typewrite('')
							time.sleep(0.5)
							pyautogui.typewrite(enter_text)
							break
					elif re.sub("[^A-Za-z0-9]+", "",el['label_text'])==re.sub("[^A-Za-z0-9]+", "",label_):
						label_=''
						time.sleep(0.7)
						pyautogui.click(box_x, box_y)
						if el['elements_class']!='Dropdown':
							pyautogui.hotkey('ctrl', 'a')
							time.sleep(0.7)
							pyautogui.typewrite('')
							time.sleep(0.5)
							pyautogui.typewrite(enter_text)
							break
						else:
							time.sleep(0.7)
							pyautogui.typewrite('')
							time.sleep(0.5)
							pyautogui.typewrite(enter_text)
							pyautogui.press('enter')
							break
	else:
	    logging.error('csv data is None')         
     	

