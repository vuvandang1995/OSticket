# OSticket

 
## Environment 
-----------
python3.5
pip9.0.2


## Install
-------

Clone and install dependences :

```
git clone git@github.com:vuvandang1995/OSticket.git
cd OSticket
cd osticket_v1
sudo apt-get install libmysqlclient-dev
sudo pip3 install mysqlclient
sudo pip3 install simplejson
sudo pip3 install -U channels
docker run -p 6379:6379 -d redis:2.8
pip3 install channels_redis
```

## Runserver: 

`python manage.py runserver`
