Introduction
============

Upload po files to a po server.

Documentation
=============

After installing this egg you will find a new script in your ./bin
directory. The script has an own help. Try INSTANCE_HOME/bin/poupload --help
to get more information.


Where and how to place login and server Information.
Put a file with the name .thepofiles in the home folder
you are working with. /home/MYLOGINNAME/.thepofiles.

The content of file should looks like the following example.

Code::

    [poupload]
    name=MYLOGINNAME TO PO SERVER
    password=MY PO SERVER PASSWORD
    url=PO SERVER URL/@@poin/upload'
