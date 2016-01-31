#start mosquitto deamon 
# mosquitto -dtop

cd /home/pi/py-beacon
#start beacon collactor and emitter
sudo python ./collector.py &
sudo python ./emitter.py &

#gotto working directory
cd /home/pi/example

# python py-beacon-mqtt-subscriber.py &