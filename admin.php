<!-- DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN" "http://www.wapforum.org/DTD/xhtml-mobile10.dtd" -->
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title></title>
</head>

<body>
<form action="check_login.php" method="post">
username:<input type="text" name="username">
<br>
password:<input type="password" name="pass">
<br>
<input type="text" name="code" />
<img id="checkpic" src="yanzhengma.php" alt="看不清楚，换一张" style="cursor: pointer; vertical-align:middle;" onClick="changing()"/>
<!--<button type="button" onClick="create_code()">更换</button>-->
<button type="submit">提交</button>
</form>
<script>
function changing(){
		document.getElementById('checkpic').src="yanzhengma.php?"+Math.random();
}
</script>

</body>
</html>
