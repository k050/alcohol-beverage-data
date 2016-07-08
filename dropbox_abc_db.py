from subprocess import call
ABCdb = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/ABC/abc.db abc.db"
call([ABCdb], shell=True)
