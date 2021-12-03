<?php

if(isset($_POST['submit'])){
    $name = $$_POST['name'];
    $subject = $$_POST['subject'];
    $mailFrom = $$_POST['email'];
    $message = $$_POST['message'];

    $mailTo = "skroy08@outlook.com";
    $headers = "From: My portfolio site". $mailFrom;
    $txt= "You have received an e-mail from".$name.".\n\n".$message;

    mail($mailTo, $subject, $txt, $headers);
    header("Location:index.html");
}