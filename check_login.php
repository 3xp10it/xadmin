<?php
session_start();
echo 'session:'.$_SESSION["verification"];
echo '<br>';
echo 'code:'.$_POST['code'];
if($_POST['code'] == $_SESSION["verification"] and $_POST['username']=='admin' and $_POST['pass']=='woaini'){
		echo "Congratulations! you have break it,good job";
		$a="A";
		for($i=0;$i<5000;$i++)
			$a=$a."B";
		echo $a;
		//header("Location: https://3xp10it.cc");
}else{
		echo 'no';
}
?>

