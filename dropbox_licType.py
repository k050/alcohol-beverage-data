from subprocess import call
CSV = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/ABC/lic_type.csv lic_type.csv"
call([CSV], shell=True)
