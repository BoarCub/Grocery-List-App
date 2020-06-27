<?php
session_start();
$age=30;
$height=1.5;
$weight=80;
$sex=-1;
$calories=2500;
if (isset($_POST['age'])){
	$age=$_POST['age'];
	if ($age>100){
		$age=100;
	} else if ($age<0){
		$age=0;
	}
} else {
	$age=-1;
}
if (isset($_POST['height'])){
	$height=$_POST['height'];
	if ($height>2){
		$height=2;
	} else if ($height<0){
		$height=0;
	}
} else {
	$height=-1;
}

if (isset($_POST['weight'])){
	$weight=$_POST['weight'];
	if ($weight>1000){
		$weight=1000;
	} else if ($weight<0){
		$weight=0;
	}
} else {
	$weight=-1;
}
if (isset($_POST['sex'])){
	if ($_POST['sex']=='male'){
		$sex=0;
	} else if ($_POST['sex']=='female') {
		$sex=1;
	} else {
		$sex=-1;
	}
} else {
	$sex=-1;
}

if ($age!=-1 && $height!=-1 && $weight!=-1 && $sex!=-1){
	if ($sex==0){
		$calories=66+
		(13.877)*$weight+
		(507.874)*$height-
		(6.8)*$age;
	}
	if ($sex==1){
		$calories=655+(9.482)*$weight+(185.0)*$height-(4.7)*$age;
	}
}
$calories*=1.375;
$calories-=($calories%1);
$url = '/daily_calories/' . $calories;
require($url);
//header("Location: options.html");
/*$vitaminD=false;
if (isset($_POST['VitaminD'])){
	$vitaminD=true;
} else {
	$vitaminD=false;
}
echo "Hello".var_export($vitaminD);
*/
?>
