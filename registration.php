 <?php

 if(isset($_POST['submit_btn']))
 {
  $first = $_POST['first'];
  $last = $_POST['last'];
  $username = $_POST['email'];
  $reason = $_POST['reason'];
  $password = $_POST['password'];

  $dom = new DomDocument();
  $dom->load("info.xml"); // rename xml file
  $dom->formatOutput = true;

/* Failed attemot
  $fragment = $dom->createDocumentFragment();
  $fragment->appendXML(" <user> 
<Email>".$username."</Email>
<First>".$first."</First>
<Last>".$last."</Last>
<Password>".$password."</Password>
<Reason>".$reason."</Reason>
</user>
");
$dom->documentElement->appendChild($fragment);
echo "test 3";
*/

  $root = $dom->getElementsByTagName('info');//->item(0);

  // Create new <user> tag
  $newUser = $dom->createElement('user');

  // Add the user tag before the first element in the info tag.
  //$root->insertBefore($newUser, $root->firstChild); removed <-

  // Create and fill <Email> tag
  $newEmail = $dom->createElement('Email');
  $newUser->appendChild($newEmail);
  $emailText = $dom->createTextNode($username);
  $newUser->appendChild($emailText);

  // Create and fill <First> tag
  $newFirst = $dom->createElement('First');
  $newUser->appendChild($newFirst);
  $firstText = $dom->createTextNode($first);
  $newUser->appendChild($firstText);

  // Create and fill <Last> tag
  $newLast = $dom->createElement('Last');
  $newUser->appendChild($newLast);
  $lastText = $dom->createTextNode($last);
  $newUser->appendChild($lastText);

  // Create and fill <Password> tag
  $newPass = $dom->createElement('Password');
  $newUser->appendChild($newPass);
  $passText = $dom->createTextNode($Password);
  $newUser->appendChild($passText);

  // Create and fill <Reason> tag
  $newReason = $dom->createElement('Reason');
  $newUser->appendChild($newReason);
  $reasonText = $dom->createTextNode($reason);
  $newUser->appendChild($reasonText);

  $dom->save("info.xml");

  echo '<h1> Thank You </h1> <br> <p>Your request has been sent. Dr. Finkle will contact you as soon as possible </p>';

  }

  else
  {
?>

 <form action = "registration.php" method="POST">
      <h1> Please enter your information and a (short) reason why you want to work on this project</h1>
        <p>
          <label>First:</label><input type = "text"  name = "first" /><br>
          <label>Last:</label><input type = "text"  name = "last" /><br>
          <label>Email:</label><input type = "text"  name = "email" /><br>
          <label>Password:</label><input type = "password" name = "password" /> 
          <br/>
	<br/>
    <textarea name="reason" cols="50" rows="5">
Enter reason here...
    </textarea>
    <br />



          <br/>
        </p>
      <input type = "submit" name="submit_btn" id = "submit" value = "submit"/>
    </form>
<?php
}
?>
