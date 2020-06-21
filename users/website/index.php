<!DOCTYPE HTML>
<?php
	session_start();
	$username="1";
	$password="1";
	//instead of fixed correct user and pass, change this
	//to access list of usernames and passwords from Database
	if (isset($_SESSION['loggedin']) && $_SESSION['loggedin']==true){
		header("Location: success.php");
	}
	if (isset($_POST['username']) && isset($_POST['password'])){
		if ($_POST['username']==$username && $_POST['password']==$password){
			$_SESSION['loggedin']=true;
			header("Location: success.php");
		}
	}
?>
<html>
	<head>
	<link href="https://fonts.googleapis.com/css2?family=Balsamiq+Sans&display=swap" rel="stylesheet">
	<link href="Styles/Stylesheet.css" rel="stylesheet" />
	</head>
	<body>
		<div class="login_container">
		<form method="post" action="index.php">
			<p class="login_text">Username:</p><br/>
			<input type="text" name="username" id="username" class="login_button"/><br/>
			<p class="login_text">Password:</p><br/>
			<input type="password" name="password" id="password" class="login_button"/><br/>
			<input type="submit" value="Login!" id="login_click"/>
		</form>
		</div>
	</body>
</html>