sudo apt-get update
sudo apt-get upgrade

sudo apt-get install rcconf mpg321 python-pip mosquitto python-smbus python-bluez python-numpy libc-ares-dev raspi-gpio libusb-dev libdbus-1-dev libdbus-glib-1-dev libglib2.0-dev libical-dev libreadline-dev libudev-dev libusb-dev make
wget https://www.kernel.org/pub/linux/bluetooth/bluez-5.32.tar.xz
tar xvf bluez-5.32.tar.xz
rm ./bluez-5.32.tar.xz
cd bluez-5.32
./configure --disable-systemd
make
sudo make install
cd ../
rm -rf ./bluez-5.32
sudo pip install paho-mqtt
sudo pip install rx
sudo cp ./rc.local /etc/rc.local