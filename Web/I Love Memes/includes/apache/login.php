<?php
session_start();
if(isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === "y" ){
    header("Location: memes.php");
}

    if(isset($_POST['submit'])){
        require "dbconn.php";
        $username=mysqli_real_escape_string($conn,$_POST['username']);
        $password=mysqli_real_escape_string($conn,$_POST['password']);

        $sql="SELECT * FROM `users` WHERE `username` LIKE '$username'";
  
        $result=mysqli_query($conn,$sql);
        $userDetails= mysqli_fetch_all($result,MYSQLI_ASSOC);
        
        if(empty($userDetails)){
            echo "User does not exist. Register";
        }
        else{
            $userDetails=$userDetails[0];
        
            if(password_verify($password,$userDetails['password'])){
                session_start();
                $_SESSION['loggedin']="y";
                $_SESSION['username']=$userDetails['username'];
                $_SESSION['userId']=$userDetails['id'];
                $_SESSION['isPremium'] = $userDetails['isPremium'];
                header("Location:memes.php");
            }
            
            else {
                echo "Password is wrong";
            }
        }
        
    
    
    
    }
?>

<?php require "header.php" ?>

<div class="container">
    <div class="row mt-5">
    <h2>Login here</h2>
    </div>

    <div class="row justify-content-center">
        <div class="col-5">
        <form action="<?php echo $_SERVER['PHP_SELF'] ?>" method="POST">
            <label class="my-1">
                Username <input type="text" name="username">
            </label>
            <label class="my-1">
                Password <input type="password" name="password">
            </label>
            <label class="my-1">
                <input type="submit" name="submit" value="Login">
            </label>
        </form>
        <div class="row">
        <p>To create account click <a href="register.php">here</a>.</p> 
        </div>
        </div>
    </div>
</div>

<?php require "footer.php" ?>

<!-- /sources/login.html -->