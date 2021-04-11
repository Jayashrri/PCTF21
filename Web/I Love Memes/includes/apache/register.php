<?php
session_start();
if(isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true ){
    header("Location: memes.php");
}

if(isset($_POST['submit'])){
    require "dbconn.php";
    $username = mysqli_real_escape_string($conn,$_POST['username']);
    $password = mysqli_real_escape_string($conn,$_POST['password']);

    $sql="SELECT * FROM `users` WHERE `username` LIKE '$username'";
    if($username==='' || $password ===''){
        echo "Username or Password cannot be empty";
    } else {
        $result = mysqli_query($conn,$sql);
        $existingUser = mysqli_fetch_all($result, MYSQLI_ASSOC);

        if(empty($existingUser)){
            //create new user
            $hash=password_hash($password, PASSWORD_DEFAULT, array('cost'=>10));
            $sql="INSERT INTO `users`(`username`,`password`) VALUES('$username','$hash') ";
            
            if(mysqli_query($conn,$sql)){
                echo "Registration Successful";
            }
            else{
                echo "Registration failed due to query error";
            }
        }
        else {
            echo "User already exists. Try another username";
        }
    }
}



?>

<?php require "header.php" ?>

<div class="container">
    <div class="row mt-5">
    <h2>Register here</h2>
    </div>
    <div class="row justify-content-center">
        <div class="col-5">
        <form action="<?php echo $_SERVER['PHP_SELF'] ?>" method="POST">
            <label class="my-1">
                Username <input type="text" name="username" required>
            </label>
            <label class="my-1">
                Password <input type="password" name="password" required>
            </label>
            <label class="my-1">
                <input type="submit" name="submit" value="Register">
            </label>
        </form>
        <div class="row">
        <p>To login click <a href="login.php">here</a>.</p> 
        </div>
        </div>
    </div>
</div>

<?php require "footer.php" ?>

<!-- /sources/register.html -->