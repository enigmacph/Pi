# To get one of the scripts running on the EnigmA server

nohup python3 your_script.py &

# How to add sounds

Navigate to the file you want to upload (in this case "etminut.mp3") and use the command "rsync etminut.mp3 pi@192.168.50.252:/var/www/html/ --rsync-path="sudo rsync"" to access it at the URL 192.168.50.252/etminut.mp3.
