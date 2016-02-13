from pygame import mixer # Load the required library

mixer.init()
mixer.music.load('/home/pi/CollarPlayground/Mac_Startup_Sound.mp3')
mixer.music.play()