# dirwatcher
A Long Running Program with signal handling and logging

The Objective:
Create a long running program
Demonstrate signal handling
Demonstrate program logging
Use exception handling to keep the program running
Create and structure your own code repository using best practices
Show that you know how to read a set of requirements and deliver on them,
asking for clarification if anything is unclear.

My Goal:
Is to create a smaller long running program that will accept command line arguments
and asssist in monitoring "magic words" within my dirwatcher program. These files should
show rather they are found and also if they are deleted. 

How do I test this??

Testing Program Operation

Test your dirwatcher program using TWO terminal windows.  In the first window, start your Dirwatcher with various sets of command line arguments.  Open a second terminal window and navigate to the same directory where your Dirwatcher is running, and try these procedures:

Run Dirwatcher with non-existent directory -- Every polling interval, it should complain about the missing watch directory.
Create the watched directory with mkdir -- Dirwatcher should stop complaining.
Add an empty file with target extension to the watched directory -- Dirwatcher should report a new file added.
Append some magic text to first line of the empty file -- Dirwatcher should report that some magic text was found on line 1, only once.
Append a few other non-magic text lines to the file and then another line with two or more magic texts -- Dirwatcher should correctly report the line number just once (don't report previous line numbers)
Add a file with non-magic extension and some magic text -- Dirwatcher should not report anything
Delete the file containing the magic text -- Dirwatcher should report the file as removed, only once.
Remove entire watched directory -- Dirwatcher should revert to complaining about a missing watch directory, every polling interval.
Testing the Signal Handler

To test the OS signal handler part of your Dirwatcher, send a SIGTERM to your program from a separate shell window.

While your Dirwatcher is running, open a new shell terminal.
Find the process id (PID) of your dirwatcher.  PID is the first column listed from the ps utility.
Send a SIGTERM to your Dirwatcher
Your signal handler within your python program should be called.  Your code should exit gracefully with a Goodbye message ...