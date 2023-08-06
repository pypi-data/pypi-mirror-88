#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, syst3m

# settings.
SOURCE_NAME = "netw0rk"
VERSION = "v1"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=2)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH, back=1)
sys.path.insert(1, BASE)

# imports.
import netw0rk
from netw0rk.v1.classes.config import *

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"--network":"Access the network.",
				"    --info":"Retrieve the current network information.",
				"--firewall":"Access the firewall (Linux only).",
				"    --info":"Retrieve the current firewall information.",
				"    --disable":"Disable the firewall.",
				"    --enable":"Enable the firewall.",
				"    --set-default false":"Set the default firewall behaviour (deny/allow).",
				"    --allow 22":"Allow a port in the firewall settings.",
				"    --deny 22":"Deny a port in the firewall settings.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"-c":"Do not clear the logs.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):

		# clear logs.
		if not self.arguments_present(['-c']):
			os.system("clear")

		# help.
		if self.arguments_present(['-h', '--help']):
			print(self.documentation)

		# network.
		elif self.arguments_present(['--network']):

			# info.
			if self.arguments_present(['--info']):
				response = netw0rk.network.info()
				r3sponse.log(response=response)
				if r3sponse.success(response): 
					del response["message"] ; del response["error"] ; del response["success"]
					info = json.dumps(response, indent=0).replace("{\n","").replace("\n}","").replace('",',"").replace('"',"")
					print(info)


			# invalid.
			else:  self.invalid()

		# firewall.
		elif self.arguments_present(['--firewall']):

			# check os.
			syst3m.default.check_operating_system(supported=["linux"])

			# retrieve the firewall information.
			if self.arguments_present(['--info']):
				response = netw0rk.firewall.info()
				r3sponse.log(response=response)
				if r3sponse.success(response): 
					del response["message"] ; del response["error"] ; del response["success"]
					info = json.dumps(response, indent=0).replace("{\n","").replace("\n}","").replace('",',"").replace('"',"")
					print(info)

			# disable the firewall.
			elif self.arguments_present(['--disable']):
				response = netw0rk.firewall.disable()
				r3sponse.log(response=response)

			# enable the firewall.
			elif self.arguments_present(['--enable']):
				response = netw0rk.firewall.enable()
				r3sponse.log(response=response)

			# set the default port action.
			elif self.arguments_present(['--set-default']):
				deny = self.get_argument("--set-default")
				if deny in ["True", "true", True]: deny = True
				else: deny = False
				response = netw0rk.firewall.set_default(deny=deny)
				r3sponse.log(response=response)

			# allow a port.
			elif self.arguments_present(['--allow']):
				port = int(self.get_argument("--allow"))
				response = netw0rk.firewall.allow(port)
				r3sponse.log(response=response)

			# deny a port.
			elif self.arguments_present(['--deny']):
				port = int(self.get_argument("--deny"))
				response = netw0rk.firewall.deny(port)
				r3sponse.log(response=response)


			# invalid.
			else:  self.invalid()

		# invalid.
		else:  self.invalid()

		#
	def invalid(self):
		print(self.documentation)
		print("Selected an invalid mode.")
		sys.exit(1)
	
# main.
if __name__ == "__main__":
	cli = CLI()
	if "--developer" in sys.argv:
		cli.start()
	else:
		try:
			cli.start()
		except KeyboardInterrupt:
			print("Aborted: KeyboardInterrupt")

