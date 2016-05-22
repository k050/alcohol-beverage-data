# alcohol-beverage-data beginner python
4/10/2016
Started learning to code with intro programming MOOC

5/6/2016
Due to steep learning curve did not start writing this code until 5/6.
This is something I will actually use.

5/10/2016
It's not pretty, but it looks to be returning the data.
Trying out Github to save and work on different versions so I can try different
things but still revert back to something in the past if I don't like it.
May need some help at some point.

5/11/2016
CA website had a bad link.  Added try-except(lic_number) right after tlst[] to skip these.  Added iso date just in case it's needed later.

5/12/2016
    Don't update from CA website in the AM as they sometimes haven't.  
    Finished uploading pages and have multiple bad links.
    Not wanting to leave my laptop on all day, I need to move this to somewhere that's always on.

5/13/2016
    Thinking about how to execute this automatically test each day.
    I decided to order a Pi and scheduling the program to run through linux(which I have no idea how to use).  This task may take a few days.  Also, created a log file on Pi to leave a record of the execution.

5/14/2016
    Set-up the Pi.  Created a Crontab file to execute script everyday at 5PM.  If you do this again, don't forget to edit directory and file read, write, execute permissions for the database.  Otherwise program will throw an error when attempting to write to db.
    
5/17/2016
    Added Dropbox-Uploader script (Thank you to the person that created it!) to crontab to upload the db file so I can share the db.  We can start using the compiled info right away using the table feature in db viewer.  
    It's just a temporary solution, while I think about how to to best query the database and output only desired leads.  Less spare-time these days to work on this.
    
5/18/2016 - 5/19/2016
    Noticed that sometimes the census tract field is blank from the CA server.  Added Try-Except to make the field None if there's no data instead if filling the field in with the next heading.
    Created a query script to look for entries from the five counties in Southern CA that we operate in, further reduced by a list of common last names based on target ethnic demographic, output a csv file with only relevant data that a sales person would want to look at or use.
    Added another Dropbox-Uploader for the outputted csv file that gets overwritten everyday.
    Made required crontab updates.
    
5/20/2016
    This program is FINALLY running and live a Raspberry Pi!  The csv file shared to office staff will be used for direct mail marketing starting next week!

5/21/2016
    Noticed the programs weren't being executed automatically at their schedule times.
    Checked online sources for possible errors with my crontab, but did not notice any obvious issues.  Ended up re-writing the crontab file again from scratch and it seems to be working now.(..?)  I added a time updater with all fields as *wildcards and it's updating the log file every minute.
    I'll have to keep checking on it this weekend.  
