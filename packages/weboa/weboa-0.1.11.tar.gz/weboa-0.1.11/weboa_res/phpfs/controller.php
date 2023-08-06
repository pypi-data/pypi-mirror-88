<?php
include_once "language.php";
if(in_array($lang, $langs))
    include_once("php/configs/".$lang.".php");
else
    include_once("php/configs/en.php");

include_once "router.php";
include_once "php/configs/consts.php";

/*Stat*/
if($_SERVER['HTTP_HOST']!="localhost") {
    $cccc = new nvgData("stati","ips",'ip',$_SITE_TITLE,6,1,1);
    $cccc2 = new nvgCount("stati","visitors",$_SITE_TITLE);
    $cccc2->enableLangC("langs");
    $cccc2->Count();
}
?>