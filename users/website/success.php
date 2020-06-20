<?php
	session_start();
	if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin']==false){
		header("Location: index.php");
	}
?>
<!DOCTYPE HTML>

<html>
<head>
	<title>Grocery Reader</title>
	<link href="https://fonts.googleapis.com/css2?family=Balsamiq+Sans&display=swap" rel="stylesheet">
	<link href="Styles/Stylesheet.css" rel="stylesheet" />
</head>
<body>
<h1 id="title">Grocery Reader</h1>
<h2>
	You have logged in!
</h2>
<button id="logout_button"><a href="logout.php">Log out</a></button>
<form action="upload.php" method="post" enctype="multipart/form-data">
  <input type="file" id="upload_file_button" name="upload_file_button" />
  <input type="submit" name="submit" value="Upload File" />
</form>
</body>
</html>