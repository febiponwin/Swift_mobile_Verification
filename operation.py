import datetime
import base64 
import pyqrcode
import png
from pyqrcode import QRCode

class operation:
	#to get current system time
	global current_time

	def __init__(self):
		operation.current_time = datetime.datetime.now()
	
	def calculate_code(self,cws,no,model):
		final_string = cws+no+model+operation.current_time.strftime("%Y-%m-%d %H:%M:%S")
		final_string_bytes = final_string.encode("ascii")
		base64_bytes = base64.b64encode(final_string_bytes)
		base64_string = base64_bytes.decode("ascii")
		return operation.current_time,base64_string

	def qr_code_png(self,ids,cws):
		url = pyqrcode.create(ids)
		url.png(cws+'.png', scale=6)
		return True


			
			

