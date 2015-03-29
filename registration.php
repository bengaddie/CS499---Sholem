 <?php

 if(isset($_POST['submit_btn']))
 {
  $username = $_POST['email'];
  $reason = $_POST['reason'];
  $text = $username . ": " . $reason . "\n";
  $fp = fopen('info.txt', 'a+');

    if(fwrite($fp, $text))  {
        echo '<h1> Thank You </h1> <br> <p>Your request has been sent. Dr. Finkle will contact you as soon as possible </p>';

    }
   fclose ($fp);
  }
else {
?>

 <form action = "registration.php" method="POST">
      <h1> Please enter your information and a (short) reason why you want to work on this project</h1>
        <p>
          <label>Email:</label><input type = "text"  name = "email" />
          <!-- <label>Password:</label><input type = "password" name = "pwd" /> -->
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
