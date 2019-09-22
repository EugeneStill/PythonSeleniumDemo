# PythonSeleniumDemo
Python Selenium unit test using page object model, environment variables and modular design.

WhatIfSports is a simulated baseball site where you can build teams using real players from past seasons of Major League Baseball.  This test logs on to the draft center and checks for x number of pitchers and y number of hitters that make a minimum expected salary.  The goal is to identify which divisions in which season have the largest number of premium players.

To run the test, create a freee WhatIfSports account: https://idsrv.fanball.com/localregistration

Log into the site and disable 2 factor authentication.

In your environment variables add your username as 'WHAT_IF_USERNAME' and password as 'WHAT_IF_PASSWORD'.  After this you should be able to run the test with the files from this repo.
