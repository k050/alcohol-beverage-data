from subprocess import call
CSV = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/ABC/koreanLaOc.csv koreanLaOc.csv"
call([CSV], shell=True)
