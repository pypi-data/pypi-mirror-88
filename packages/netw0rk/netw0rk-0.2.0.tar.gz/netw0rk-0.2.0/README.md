# Netw0rk
Author(s):  Daan van den Bergh<br>
Copyright:  © 2020 Daan van den Bergh All Rights Reserved<br>
<br>
<br>
<p align="center">
  <img src="https://github.com/vandenberghinc/storage/blob/master/images/logo.png?raw=true" alt="Bergh-Encryption" width="50"/>
</p>

## Installation
	pip3 install netw0rk --upgrade

## Python Examples.

### The FireWall object class
The FireWall() object class.
```python

# import the package.
import netw0rk

# retrieve the firewall information.
response = netw0rk.firewall.info()

# disable the firewall.
response = netw0rk.firewall.disable()

# enable the firewall.
response = netw0rk.firewall.enable()

# set the default port action.
response = netw0rk.firewall.set_default(deny=True)

# allow a port.
response = netw0rk.firewall.allow(2200)

# deny a port.
response = netw0rk.firewall.deny(2200)

```

### The Network object class
The Network() object class.
```python

# import the package.
import netw0rk

# get network info.
response = netw0rk.network.info("vandenberghinc.com")

# ping an ip.
response = netw0rk.network.ping("192.168.1.200")

# convert a dns.
response = netw0rk.network.convert_dns("vandenberghinc.com")

```

### The Curl object class
The Curl() object class.
```python

# import the package.
import netw0rk

# initialize the curl object.
curl = n3twork.curl.Curl(
	base_url="https://poker-stats-app.herokuapp.com/",
	headers={})

# get request.
response = curl.get("api/search/", data=None)

# post request.
response = curl.post("api/search/", data=None)

# delete request.
response = curl.delete("api/search/", data=None)

# download an img
response = curl.download_img("static/icon.png", "/tmp/icon.png")


```

### Response Object.
When a function completed successfully, the "success" variable will be "True". When an error has occured the "error" variable will not be "None". The function returnables will also be included in the response.

	{
		"success":False,
		"message":None,
		"error":None,
		"...":"...",
	}