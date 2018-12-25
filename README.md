# hostinger_ssl_update
This script is able to automatize the upload of new SSL certificates to  Hostinger Cpanel website. 

To run this script you should have the new certificates: (CA, KEY and CRT)

This certificates can be generated using the client: letsncrypt acme for php. In the following web page, hostinger provides the steps to generate them on its own hosting

https://www.hostinger.com/tutorials/ssl/how-to-install-free-ssl-from-lets-encypt-on-shared-hosting

If you don't want to use the acme client, we've included an script to generate self-signed certificates. If you want to use this script you can execute:

```
cd ssl
chmod +x cfssl.sh && ./cfssl.sh example.com
```

This script will generate the root_ca certificate and a self-signed certificate for this `example.com`

# Setup

First of all we need python 2.6 or greater and pip installed. After that we should install the dependencies:

```
pip install -r requirements.txt
```  

The configuration of the script is under the file `.env.yml`, we provide an example in the file `.env.example.yml`

```
ssl:
  domain: "example.com"
  key: "ssl/example.com-key.pem"
  crt: "ssl/example.com.pem"
  ca_crt: "ssl/example.pem"
hostinger:
  hosting_id: "xxx"
  cpanel_url: "https://www.hostinger.es/cpanel-login?r=index/index"
  username: "xxx@xxx.xxx"
  password: "xxx"
  ```
  
Username, hosting_id and the password can be passed to the script with the following env vars:  HOSTINGER_USER, HOSTINGER_ID, HOSTINGER_PASSWORD

To run the script you must run the following command:
```
python load_ssl.py
```

If it has worked without errors, The following config will appear on cpanel:

![Hostinger Cpanel Config](/screenshots/hostinger.png?raw=true "Hostinger Cpanel Config")
