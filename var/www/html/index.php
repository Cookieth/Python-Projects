<!--- COMMENTED OUT		--->
<!--- <?php phpinfo();?>	--->

<?php

$page = $_SERVER['PHP_SELF'];
$sec = "0.25";

$contents = file_get_contents('buttonData.txt');
$displayInfo = "Not Pressed";

$potentiometer = file_get_contents('potentiometerData.txt');

$fontSize = ((double)$potentiometer-180)/100;

$cIC = '#000000';

if($contents === '1'){
	$displayInfo  = "Pressed";
	$cIC = '#88ff3a';
}
else{
	$displayInfo = "Not Pressed";
	$cIC = '#ff3a3a';
}

?>

<html>

<head>

	<!---	<meta http-equiv="refresh" content="<?php echo $sec?>;URL='<?php echo $page?>'"> --->

	<script type="text/javascript">
		window.onload = startInterval;
		function startInterval(){
			setInterval("startTime();",500);
		}

		function startTime(){
			document.getElementById('time').style.backgroundColor = "<?php echo $cIC ?>";
		}
	</script>
</head>

<body style="background-color:DodgerBlue;" align="center">
<font face="Verdana" color="white">

	<br><br><br><br><br><br><br><br><br><br><br><br>

	<h1>Button Status</h1>
	<div><font color="<?php echo $cIC ?>" size="<?php echo $fontSize ?>" id="time"><strong><?php echo $displayInfo ?></strong></font></div>

	<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

	<h1> Friends </h1>
	<img src="https://i.imgur.com/QM3Ahrk.jpg" alt="A wild Ashwin">
	<img src="https://i.imgur.com/PhAfi00.jpg" alt="Haraynay">
</font>
</body>
</html>
