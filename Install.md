## Install python3

```
sudo apt-get update
sudo apt-get -y upgrade
```

## Intall pip3

`sudo apt-get install -y python3-pip`

## Install mysql

`sudo apt-get install mysql-server`

## Install git

`sudo apt-get install git`

## Clone repo and run requirements.txt file

```
git clone https://github.com/vuvandang1995/OSticket.git
cd OSticket
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo pip3 install -r requirements.txt
```

## Install redis-server

`sudo apt install redis-server`

*You need to VPN to Meditech network to use the system.*

## Run server OSticket

```
cd OSticket
cd osticket_chat_template
python3 manage.py runserver 0.0.0.0:8080
```

## You can use the system via browser: IP_your_server:8080
