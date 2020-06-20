<?php
$target_dir= "uploads/";
$target_file= $target_dir . basename($_FILES['upload_file_button']['name']);
$uploadPoss=1;
$imageFileType=strtolower(pathinfo($target_file,PATHINFO_EXTENSION));

if (isset($_POST['submit'])){
	$check=getimagesize($_FILES['upload_file_button']['tmp_name']);
	if ($check==true){
		echo "File is an image - " . $check['mime'] . ".";
		$uploadPoss=1;
	} else {
		echo "File is not an image.";
		$uploadPoss=0;
	}
}

if (file_exists($target_file)){
	echo "Sorry, file already exists.";
	$uploadPoss=0;
}
if ($_FILES['upload_file_button']['size']>500000){
	echo "Sorry, your file is too large";
	$uploadPoss=0;
}

if ($imageFileType=="jpg" || $imageFileType=="jpeg" || $imageFileType=="png"){

} else {
	echo "Sorry, only JPG, JPEG, or PNG files are allowed.";
	$uploadPoss=0;
}

if ($uploadPoss==0){
	echo "Sorry, your file was not uploaded.";
} else {
	if (move_uploaded_file($_FILES['upload_file_button']['tmp_name'], $target_file)){
		echo "The file " . basename($_FILES['upload_file_button']['name']) . " has been uploaded.";
	} else {
		echo "Sorry, there was an error uploading your file";
	}
}
?>
<!DOCTYPE HTML>
<html>
	<body>
		<link href="https://fonts.googleapis.com/css2?family=Balsamiq+Sans&display=swap" rel="stylesheet">
		<link href="Styles/Stylesheet.css" rel="stylesheet" />
	
	</body>
</html>