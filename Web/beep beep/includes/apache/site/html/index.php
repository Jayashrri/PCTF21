<?php

require "../shabot.php";
require "flag.php";
if(stripos($_SERVER['HTTP_USER_AGENT'], "bot" )===false) {
    include ("humans.html");
    die();
}


if(isset($_GET["botdetails"])){

    if( isSafe($_GET["botdetails"])){
        include($_GET["botdetails"]);
        die();
    }
    else {
        die();
    }
}

//only true bots can bypass this as no human can compute it
if( isset($_POST["provebot1"]) && isset($_POST["provebot2"]) ){
   
    $safe1 = (string) $_POST["provebot1"];
    $safe2 = (string) $_POST["provebot2"];
    if($safe1!==$safe2 && md5(sha1($_POST["provebot1"])) === md5(sha1($_POST["provebot2"]))){
        echo json_encode($coordinates);
        die();
    }
}
?>

<?php require("templates/header.php") ?>

<body style="background: black">
    <div class="container text-center my-5">
        <h1 style="color: red">Leaders </h1>
    </div>    

    <div class="container justify-content-between" style="border: 1px solid black; color: white">
        <img src="images/spot.png" width="450" height="300">
        <h3> <a href="<?php echo $_SERVER["PHP_SELF"] . "?botdetails=spot.html" ?>"> Spot </a> </h3>
        <p>Lead spy</p>
    </div>

    <div class="container justify-content-between" style="border: 1px solid black; color: white">
        <img src="images/handle.png" width="450" height="300">
        <h3> <a href="<?php echo $_SERVER["PHP_SELF"] . "?botdetails=handle.html" ?>"> Handle </a> </h3>
        <p>Lead Supplies Manager</p>
    </div>

    <div class="container justify-content-between" style="border: 1px solid black; color: white">
        <img src="images/atlas.png" width="450" height="300">
        <h3> <a href="<?php echo $_SERVER["PHP_SELF"] . "?botdetails=atlas.html" ?>"> Atlas </a> </h3>
        <p>Lead fighter </p>
    </div>
<?php require("templates/footer.php") ?>

