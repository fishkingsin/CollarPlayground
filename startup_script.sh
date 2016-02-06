#start mosquitto deamon 
# mosquitto -d

# cd /home/pi/py-beacon
#start beacon collactor and emitter
# sudo python ./collector.py &
# sudo python ./emitter.py &

#gotto working directory
cd /home/pi/CollarPlayground
sudo python select_language.py
echo 'start the game'
python py-beacon-mqtt-subscriber.py &
sudo python counter.py &