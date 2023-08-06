<?php
$uris=explode("/", $_SERVER['REQUEST_URI']);
$main_page=$uris[1];

if($main_page)
{
    $available_pages=[];
    $current_page = (in_array($main_page, $available_pages)) ? $main_page : "main";
}
else
    $current_page = "main";

?>