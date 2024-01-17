<?php
session_start();
$conn = mysqli_connect('localhost','root','','damo');

if(! $conn ){
    die('Could not connect: ' . mysqli_error());
}

if(count($_POST)>0){
	// $user = $_POST['uname'];
	// $pass = $_POST['pwd'];
	$result = mysqli_query($conn,"SELECT * FROM user WHERE user='" . $_POST["uname"] . "' and pass = '". $_POST["pwd"]."'");
	$row  = mysqli_fetch_array($result);
	print_r($row['pass']);
	if(is_array($row))
	{
		$_SESSION["uname"] = $row['user'];
        $_SESSION["pwd"] = $row['pass'];
        header("Location:Scraper.php");
		// header('location:Scraper.php');
	}
	else{
		echo '<script>alert("Incorrect username or password")</script>';
		echo '<script>window.location.replace("login.html")</script>';
	}
}

?>