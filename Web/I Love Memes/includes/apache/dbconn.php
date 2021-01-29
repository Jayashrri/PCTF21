<?php
$conn = mysqli_connect('db','root','secpass','pctfenc');

if(!$conn){
    die("Connection Error to DB");
}
