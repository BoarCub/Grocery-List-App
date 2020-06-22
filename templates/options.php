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
		$calories=66+(13.877)*$weight+(507.874)*$height-(6.8)*$age;
	}
	if ($sex==1){
		$calories=655+(9.482)*$weight+(185.0)*$height-(4.7)*$age;
	}
}
$calories*=1.375;
$calories-=($calories%1);
echo $age;
/*$vitaminD=false;
if (isset($_POST['VitaminD'])){
	$vitaminD=true;
} else {
	$vitaminD=false;
}
echo "Hello".var_export($vitaminD);
*/
?>
<!DOCTYPE HTML>
<html>
	<head>
	<title>Grocery Reader - Options</title>
	<link href="https://fonts.googleapis.com/css2?family=Balsamiq+Sans&display=swap" rel="stylesheet">
	<link href="Styles/Stylesheet.css" rel="stylesheet" />

	<style>


.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {display:none;}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;

  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;

  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
 
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}

	</style>

	</head>
	
	<body>
		<div class="top_right_container2">


<button id="options_button"><a href="main.html">Back</a></button>

</div>
		<!--<div>
		<button class="top_right_container" id="options_button"><a href="success.php">Back</a></button>
		</div>
		-->

		
		<form method="post" action="options.php">
		<p>Age</p>
		<input type="number" name="age" />
		<h6 style="display:inline">Years</h6>
		<p>Height</p>
		<input type="number" name="height" />
		<h6 style="display:inline">Meters</h6>
		<p>Weight</p>
		<input type="number" name="weight" />
		<h6 style="display:inline">Kilograms</h6>
		<p>Sex</p>
		<select name="sex">
			<option value="male">Male</option>
			<option value="female">Female</option>
		</select>
		
		<br />
		<br />
		<input type="submit" name="submit" value="Update" />
		</form>
		

		<!--<script>
		if (!empty($_POST)){
			echo "Hello the form is not empty!!";
		}
		//document.getElementById("option_form").submit();
		</script>-->
	
	</body>
</html>