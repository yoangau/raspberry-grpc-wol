# raspberry-grpc-wol
This is a small project to wake on lan your computer when your network card does not support it. It is more of a learning project, but maybe someone is in need of solution, so why not share it. If you happen to have a raspberry-pi, internet and a desktop computer and your card does not support WoL or WoWLAN (or does it?), then this might be the project for you.

# getting prepared
Install the linux distro of your choice on your raspberry-pi. Configure the wifi if needed and install both [docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-engine---community-1) and [docker-compose](https://docs.docker.com/compose/install/). You are going to need a [rsa key pair](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent), since the project uses asymetrique signature for authentication.

# start services
1. copy your public key in the server directory `cp /path/to/id_rsa.pub cp /path/to/server/id_rsa.pub`
2. start services on the raspberry-pi `docker-compose -p raspberry-grpc-wol up -d`
3. to access the services from the public network you are going to do some [port forwarding](https://en.wikipedia.org/wiki/Port_forwarding) on your router from the port of your client to the ip:port of the server (default: your_local_ip:50501). 

# physical setup
1. power up the raspberry-pi from the [inside](https://www.amazon.ca/gp/product/B002GNU2V6/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1)
2. you will need to plug the GPIO the way it is describe in the `gpio_interface.py` ![raspberry-pi-zero-gpio](https://www.raspberrypi.org/documentation/usage/gpio/images/gpio-numbers-pi2.png)
3. plug the other part of the button to a 5v pin
4. let the alimentation of the led on your motherboard

# setup the client
1. install python3 and python-pip
2. go in root folder of the project and execute `sh setup.sh`
3. go to the client directory `cd client`
4. start the client `python desk_wol_client.py {poweron|poweroff|hardreset} -i /path/to/private/key/id_rsa`