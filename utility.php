<!--
File description:




 -->

<?php

/*
TO-DO:

POSSIBLE BUGS:
	-may need to set permissions for newly created diff and changed files to avoid program failure


-CORE: parse diff file titles for : time, file-name, user. present them to admin in correct order


-let admin commit or revert the diff change

-make getters and setters for ALL directories PATH uses, even the ssh command

-getter for all diff file changes

-getter: most recent diff file w.r.t singular file

-create new user registration 
	-Create admin page notification showing the persons name, email, and short synopsis of why they want to crowdsource
	-if admin confirms, 
		-(add username and email to text files)
		-email person telling them they can crowdsource
	-else
		-email person telling them they cant crowdsource
		
-make user type their name everytime they commit a change and check to see if they are a user

-make sure all files have correct permissions

-make file opens and closes error proof

-ask for specific Multilab account for this project, ie get it off mtlank2
	-anywhere that mtlank2 is in the path, get it out
*/












//This command executes a string passed command on the remote Multilab server, and returns the result
function executeRemoteCommand($command){
	putenv("PATH=/bin:/usr/local/bin:/usr/local/bin/csrepo;/usr/local/gnu/bin:/usr/openwin/bin:/usr/local/X11R6/bin:/usr/ccs/bin:/usr/bin:/usr/ucb:/etc:/usr/local/java/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/mounts/u-zon-d2/ugrad/mtlank2/HTML/scripts:/usr/bin/expect:/usr/bin/X11/expect:/usr/share/man/man1/expect.1.gz:/usr/lib/x86_64-linux-gnu/libserf-1.so.1");
	putenv("LD_LIBRARY_PATH=/lib:/usr/lib:/usr/lib/x86_64-linux-gnu:/usr/lib/x86_64-linux-gnu/libserf-1.so.1");
	//echo "<br>debug: ".'2>&1 ssh mtlank2@penstemon.cs.engr.uky.edu "'.$command.'"'."<br>";
	//echo pass_thru('ssh mtlank2@penstemon.cs.engr.uky.edu "'.$command.'"');
	return passthru('2>&1 ssh mtlank2@penstemon.cs.engr.uky.edu "'.$command.'"');
}


//This command takes the ABSOLUTE (pwd) path of where the OCR files are located and stores this string in a file
function setOcrFilesPath($directoryLocation){
file_put_contents("constants/ocrFilesPath.txt" ,$directoryLocation); 
}






?>