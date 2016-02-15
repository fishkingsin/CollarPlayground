cd /home/pi/py-beacon
echo "start beacon collactor and emitter"
sudo python ./collector.py &
sudo python ./emitter.py &
echo "gotto working directory"
# cd /home/pi/CollarPlayground
# echo 'start the game'
# python py-beacon-mqtt-subscriber.py &
