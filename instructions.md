# To add scheduled sound
- Go to sound manager add new line after line 19
include the following line:
schedule.every().day.at("HH:DD").do(play_sound("<name of file>"))

Replace "HH:DD" with time of day you want
Replace <name of file> with your files name without the file-ending. so if the file is lul.mp3 then the string should be "lul"

# How to add sounds
Navigate to the file you want to upload (in this case "etminut.mp3") and use the command "rsync etminut.mp3 pi@192.168.50.252:/var/www/html/ --rsync-path="sudo rsync"" to access it at the URL 192.168.50.252/etminut.mp3.


# Setting up javascript service
PM2

# Setting up python script as service
## To set up new service
sudo vim /etc/systemd/system/<name-of-service>.service

write into this file:

```
[Unit]
Description=Sound manager service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Python/Pi/sound_manager.py
WorkingDirectory=/home/pi/Python/Pi/
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

sudo systemctl daemon-reload

sudo systemctl enable sound_manager.service

sudo systemctl start sound_manager.service

## to start, stop restart
sudo systemctl stop sound_manager.service
sudo systemctl start sound_manager.service
sudo systemctl restart sound_manager.service

## If you make changes to the service itself
sudo systemctl daemon-reload


## Crontab settings

### crontab -e
* * * * * export DISPLAY=:0 && xset q && xset dpms force on

### sudo crontab -e
* * * * * cd /home/pi/Python/Pi/ && git pull >/dev/null 2>&1
0 4 * * * systemctl restart sound_manager.service