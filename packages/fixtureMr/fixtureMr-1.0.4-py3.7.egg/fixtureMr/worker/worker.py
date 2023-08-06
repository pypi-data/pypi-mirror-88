# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-12-11 17:08:05
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-12-11 21:05:49
import serial
import time
from fixtureMr.base.con_mysql import UseMysql

class Worker(object):
	def __init__(self,num):
		useMysql = UseMysql()
		port = useMysql.getFixturePort(num)
		try:
			self.open_com = serial.Serial(port,115200)
		except:
			self.open_com.close()
			raise Exception("连接治具异常,请确认端口是否正确")
		self.get_data_flag = True


	def closeLock(self):
		"""
		num 指定关闭哪台治具上的锁
		"""
		
		#关锁前先确认锁的状态
		if self.isOpenStatus():
			self.open_com.write("AT+SETUP_ROTATION_ANGLE:80\r\n".encode())
			time.sleep(2)
			self.get_data()
			if self.isCloseStatus():
				self.open_com.write("AT+SETUP_ROTATION_ANGLE:-80\r\n".encode())
				time.sleep(2)
				self.get_data()
				return True
			else:
				return False
		else:
			self.open_com.close()
			raise Exception("锁还未打开,无法关锁")


	def isOpenStatus(self):
		self.open_com.write("AT+GET_LOCK_STATE\r\n".encode())

		time.sleep(1)

		content = self.get_data()

		if "1" in content:
			return True
		else:
			return False

	def isCloseStatus(self):
		self.open_com.write("AT+GET_LOCK_STATE\r\n".encode())

		time.sleep(1)

		content = self.get_data()

		if "0" in content:
			return True
		else:
			return False		

	def get_data(self,over_time=20):
		start_time = time.time()
		data = ""

		while True:
			end_time = time.time()
			print(end_time)
			print("时间间隔为:",end_time - start_time)
			if (end_time - start_time) < over_time and self.get_data_flag:
				waitNum = self.open_com.inWaiting()
				print("waitNum",waitNum)
				if waitNum>0:
					print(waitNum)
					data = self.open_com.read(waitNum)
					data = str(data)

					if data:
						print("接收的内容为:",data)
						self.get_data_flag = False
						return data

			else:
				break
		print("超时,无消息")
		return data

	def __del__(self):
		self.open_com.close()

