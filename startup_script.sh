#/bin/sh
#enable gpio 16 buzzer
gpio mode 16 out
#fire
max=3
for i in `seq 1 $max`
do  
	echo $i
	sleep 1
	gpio -g write 16 1
	sleep 1
	gpio -g write 16 0
	sleep 1
done
sleep 1

#startup jingle
mpg321 /home/pi/CollarPlayground/XEX_ifva_Speech_Startup.mp3 &

cd /home/pi/CollarPlayground/
echo "sync master"
sudo git reset --hard
sudo git pull origin master
sleep 1
#mount disk if avaiable
echo "mount /media/usb"
find /dev/  -name "sda1" -print0 | xargs -0 -r -I file mount file /media/usb
sleep 2
for i in /media/usb/contents/* 
do
	echo "cp \"$i\" /home/pi/CollarPlayground/"
	cp "$i" /home/pi/CollarPlayground/
done
sleep 2
echo "unmount /media/usb"
sudo umount /media/usb
echo "done"
#start core process
#start mosquitto deamon 
mosquitto -d

cd /home/pi/CollarPlayground/py-beacon/
echo "start beacon collactor and emitter"
sudo python ./collector.py &
sudo python ./emitter.py &

echo "gotto working directory"
cd /home/pi/CollarPlayground
sudo python select_language.py
echo 'start the game'
python py-beacon-mqtt-subscriber.py &
sudo python counter.py &
sudo python shutdown_script.py &