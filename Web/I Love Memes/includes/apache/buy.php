<?php 
session_start();

if(!isset($_SESSION["loggedin"]) && $_SESSION["loggedin"]!=="y"){
    header("Location: index.php");
}

if(isset($_POST) && !empty($_POST)){
    extract($_POST);
    require "dbconn.php";
    $code = mysqli_real_escape_string($conn,$actcode);

    $sql = "SELECT * FROM `activation` WHERE `code` LIKE '$code'";

    $result=mysqli_query($conn,$sql);
    $codes= mysqli_fetch_all($result,MYSQLI_ASSOC);
    
    if(empty($codes)){
        echo "Invalid Code";
    }
    else {
        $codeDetails = $codes[0];
        if((int)$codeDetails['used'] === 1 ){
            echo "Code is used. Buy new one";
        }
        else if($codeDetails['code']===$code) {
            $userId = $_SESSION['userId'];
            $sql = "UPDATE `users` SET `isPremium` = '1' WHERE `users`.`id` = $userId";
            
            if(mysqli_query($conn, $sql)){
                $codeId = $codeDetails['id'];
                $_SESSION['isPremium'] = '1';
                $sql = "UPDATE `activation` SET `used` = '1' WHERE `activation`.`id` = $codeId ";
                if(mysqli_query($conn, $sql))
                    header("Location: memes.php");
                else 
                    echo "Error updating codes";
            }
            else {
                echo "Error processing request try contacting admin";
            }
        }
    }
}

?>

<?php require "header.php"; ?>

<div class="container">
    <div class="row my-3">
        <div class="col">
            <h2> Thanks for purchasing our product </h2>       
        </div>
    </div>
    <div class="row">
        <div class="col">
            <form action="<? echo $_SERVER['PHP_SELF'] ?>" method="POST">
                <label>
                    Enter your super secret activation code bought from our stores: 
                    <input name="actcode" type="text" required>
                </label> 
                <input type="submit" name="submit"  value="Submit">   
            </form>
        </div>
    </div>

</div>

<div class="container">
    <div class="row justify-content-center">
        <div class="col-1 my-5">
            <a href="logout.php" class="btn btn-primary">Logout</a>
        </div>
    </div>
</div>

<?php require "footer.php"; ?>

<!-- /sources/buy.html -->