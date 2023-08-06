CONTENTS OF THIS FILE
---------------------

 * Introduction
 * Installation
 * Using the App
 * Design Decisions


INTRODUCTION
------------

This is a small (but timecostly) school project that was quite fun. It does not do really much.
You can give it a url (should give out a json) and it will log the atribute you provide.





INSTALLATION
------------

A made it a pip3 package so you can install it with 

pip3 install restlogger

It is a packaged CLI package so it does not need a python3 infront of it when executed.

Otherwise it can be cloned directly from git and there is a install.sh script that probably should be executed before running restlogger.



USING THE APP
-------------

The Arguments that can be given are:
-h or --help: Gives you the help menu
-f or --freq: Define sample rate in [s]
-u or --url: Provide the full url
-x or --xpath: The path to the key in the json responds
-k or --key: What should be logged
-c or --change: Logging only when change happened can be selected

The program can be stopped by pressing Ctrl+c (control+c on Mac)

Read the licence.




DESIGN DECISIONS
----------------

There are odd things in this program, mainly because I do not know it better and some of the imported models I used for the first time.
