from subprocess import call
CSV = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/ABC/new.csv new.csv"
call([CSV], shell=True)
