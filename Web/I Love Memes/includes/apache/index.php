<?php
session_start();
if(isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === 'y' ){
    header("Location: memes.php");
}
?>
<?php require "header.php" ?>

    <div class="container">    
        <div class="row text-center justify-content-center mt-5">
            <h1 style="color: red">m3m3Flix</h1>
        </div>
        <div class="row text-center">
            <p>
                One stop solution to all your meme needs. We have the best collection of memes.
            </p>
        </div>
        <div class="row justify-content-center">
            <img src="images/front.webp" class="col-5" height="400px" style="border: 1px solid black">
        </div>
        <div class="row text-center mt-2" >
            <p><a href="login.php">Login</a> to see more memes. </p>
        </div>
    </div>

<?php require "footer.php" ?>

<!-- /sources/index.html -->