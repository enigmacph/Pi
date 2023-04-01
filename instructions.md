# To get one of the scripts running on the EnigmA server
nohup python3 your_script.py &

# To add scheduled sound
- Go to sound manager add new line after line 19
include the following line:
schedule.every().day.at("HH:DD").do(play_sound("<name of file>"))

Replace "HH:DD" with time of day you want
Replace <name of file> with your files name without the file-ending. so if the file is lul.mp3 then the string should be "lul"

# How to add sounds
Navigate to the file you want to upload (in this case "etminut.mp3") and use the command "rsync etminut.mp3 pi@192.168.50.252:/var/www/html/ --rsync-path="sudo rsync"" to access it at the URL 192.168.50.252/etminut.mp3.
