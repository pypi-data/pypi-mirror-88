<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
 
require 'src/Exception.php';
require 'src/PHPMailer.php';
require 'src/SMTP.php';

function sendM($to,$s,$m, $f = 0, $h = false)
{
    $passs = "";

    $from = 'no-reply@nvg-group.com';
    $mail = new PHPMailer(true);
    $mail->isSMTP(); 
    $mail->SMTPDebug = 0; 
    $mail->Host = "smtp.yandex.ru"; 
    $mail->Port = "465"; // typically 587 
    $mail->SMTPSecure = 'ssl'; // ssl is depracated
    $mail->SMTPAuth = true;
    $mail->Username = $from;
    $mail->CharSet = "utf-8";
    $mail->Password = $passs;
    $mail->addReplyTo($from);
    $mail->setFrom($from, "NVG Group");
    $mail->addAddress($to);
    $mail->Subject = $s;

    if($h)
    {
        $mail->msgHTML($m); // remove if you do not want to send HTML email
        $mail->AltBody = 'HTML not supported';
    }
    else
    {
        $mail->IsHTML(false);
        $mail->Body = $m;
    }

    if($f!=0)
        $mail->AddAttachment($f['tmp_name'], $f['name']);
    $mail->send();
}
?>