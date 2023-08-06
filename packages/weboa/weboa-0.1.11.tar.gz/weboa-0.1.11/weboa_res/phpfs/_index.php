<?php
header("X-Frame-Options: SAMEORIGIN");
header("X-Content-Type-Options: nosniff");
header("X-XSS-Protection: 1; mode=block");

/*LIBS*/
require_once("php/lib/autoload.php");
require_once("php/db.php");
require_once("php/controller/controller.php");
?>
<!DOCTYPE HTML>
<html lang='<?=$lang;?>'>
<head>
    <?php include("php/modules/header.phtml");?>
</head>
<body>
<?php
    include_once "php/controller/index.php";
    include_once "php/modules/footer.phtml";
?>
</body>
</html>    