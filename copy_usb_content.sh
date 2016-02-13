gpio mode 16 out
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
sleep 2
mpg321 /home/pi/CollarPlayground/Mac_Startup_Sound.mp3 &

echo "mount /media/usb"
find /dev/  -name "sda1" -print0 | xargs -0 -r -I file mount file /media/usb
sleep 2
for i in /media/usb/contents/* 
do
	cp "$i" /home/pi/CollarPlayground/
done
sleep 2
echo "unmount /media/usb"
sudo umount /media/usb
echo "done"