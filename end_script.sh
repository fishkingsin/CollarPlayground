#/bin/sh
#enable gpio 16 buzzer
#long buzzer
gpio mode 16 out
#fire
gpio -g write 16 1
sleep 5
gpio -g write 16 0
sleep 1
#end jingle
mpg321 /home/pi/CollarPlayground/XEX_ifva_Speech_Bye.mp3
sudo shutdown -h now