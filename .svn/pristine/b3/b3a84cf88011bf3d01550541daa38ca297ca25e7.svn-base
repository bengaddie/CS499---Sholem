<?php

require_once "globals.php";
require_once "utility.php";




//This condition will catch if a user makes a editing change from user.php.  This condition is caught after user.php calls validate.php (this file) using a POST redirect of information.
//Upon catching from user.php, this block of control will store an old copy of the pre-edited text into our logs, updating the new version to the edited version, and lastly compare the 
//two previously mentioned files via a diff command.
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['ocrMakeChange']) ){

	//This is the exact OCR file that we wish to update and change
	$locationOfOcrFile = $locationOfAllOcrFiles."/".$_POST['book']."/".$_POST['page'];

	//Make a new text file of format "userEditsBookPageAtTime", which is comprised of the contents of the file before the user made any changes. In other words, the log file which stores
	//the pre-edited file is renamed to explain who edited it, what file was edited, and at what time
	$preEditFileName = "_".$_POST['user']."~".$_POST['book']."~".$_POST['page']."~".time();
	//echo $preEditFileName."<br>";
	
	//Save the pre-edited version of the file into our logs directory
	file_put_contents($locationOfLogFiles."/".$preEditFileName, file_get_contents($locationOfOcrFile));

	//Get the text that was just edited by the user.  This comes from the textarea in user.php 
	$textChangeFromUser = $_POST['editedText'];
	//echo $textChangeFromUser;
	
	//Replace the main repo OCR file with the newly edited text
	file_put_contents($locationOfOcrFile, $textChangeFromUser);
	
	//Now we have 2 files.  The old file (pre-edit without changes) and the new file (post-edit with changes) 
	//Run a diff command on the old file versus the newly edited file. This will give us the exact change(s) made. Save as a diff file
	$command = "diff ".$locationOfOcrFile." ".$locationOfLogFiles."/".$preEditFileName." > ".$locationOfLogFiles."/".$preEditFileName."~diff"; //cd "realpath(__DIR__);
	//echo $command;
	echo executeRemoteCommand($command);
	
	//Leave this script and return back to user.php, since the user may want to make another change
	header('Location: user.php');    
	exit;	
}





//Admin has approved of crowdsourced change, now we commit that change
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['commitOcrChange'])){

	///mounts/u-zon-d2/ugrad/mtlank2/HTML/499/logs/-someGuy_book_0016_1427842410_diff
	$locationOfIndividualLogFile = $locationOfLogFiles."/".$_POST['user']."~".$_POST['book']."~".$_POST['page']."~".$_POST['time'];
	//echo $locationOfIndividualLogFile."<br>";
	
	//Commit the change
	$command = "cd ".$locationOfAllOcrFiles."/".$_POST['book']."; svn commit ".$_POST['page']." -m '".$_POST['user']."'"; //Put user name in comment
	//echo $command."<br>";
	//Perform the commit to the main repo
	executeRemoteCommand($command);
	echo "Change approved and stored.<br>";

	executeRemoteCommand("rm ".$locationOfIndividualLogFile." ".$locationOfIndividualLogFile."~diff");
	
	header('Location: admin.php');    
	exit;	
}




//Deny the most recent crowdsourced change
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['denyOcrChange'])){
	$locationOfLogFile =realpath(__DIR__)."/"."logs/".$_POST['user']."~".$_POST['book']."~".$_POST['page']."~".$_POST['time'];
	//echo file_get_contents("constants/ocrFilesPath.txt")."/".$_POST['book']."/".$_POST['page']. "         ". $locationOfLogFile;
	file_put_contents(file_get_contents("constants/ocrFilesPath.txt")."/".$_POST['book']."/".$_POST['page'], file_get_contents($locationOfLogFile));

	executeRemoteCommand("rm ".$locationOfLogFile." ".$locationOfLogFile."~diff");

	//executeRemoteCommand("svn commit"." ".file_get_contents("constants/ocrFilesPath.txt")."/0016");
	header('Location: admin.php');    
	exit;
} 









//Set the new path of the OCR files you want crowdsourced
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['ocrFilesPath'])){
	//$adminInfo = gatherAdminInfo();
	//adminInfo[ocrFilesPath] = $_POST['ocrFilesPath']
	setOcrFilesPath($_POST['ocrFilesPath']);
	echo "<br>Administrator has set a new path for the OCR file directory.<br>";
	echo "Click here to return to the <a href='admin.php'>Administrator page</a>.";
	//header('Location: admin.php');    
	//exit;
} 

















?>