<?php session_start();  

if(!isset($_SESSION["loggedin"]) && $_SESSION["loggedin"]!=="y"){
    header("Location: index.php");
}
?>

<?php require "header.php"; ?>
<div class="container">
    <div class="row">
        <div class="col text-center">
            <h1>m3m3Flix</h1>
        </div>
    </div>
</div>

<div class="container" style="border:4px solid green; border-radius: 10px">
    <div class="row">
        <div class="col">
        <h2 style="color: green">Free Memes</h2>
        </div>
    </div>
    <div class="row justify-content-center">
        <img src="images/brit.webp" class="col-8" width="500px" height="600px"  >
    </div>
    <div class="row justify-content-center">
        <img src="images/america.webp" class="col-6" width="500px" height="600px"  >
    </div>
    <div class="row justify-content-center">
        <img src="images/essay.webp" class="col-5" width="500px" height="600px"  >
    </div>
</div>


<div class="container" style="border:4px solid gold; border-radius: 10px" >
    <div class="row">
        <div class="col">
            <h2> Premium memes </h2>
        </div>
    </div>
    <?php if($_SESSION['isPremium'] ==='0' ): ?>
    <!-- Buy premium -->
    <div class="row text-center">
        <h3  class="col" style="color: red"> Please <a href="buy.php">purchase</a>  paid version to unlock the premium memes. We have the best meme content. </h3>
    </div>
    <!-- Premium meme -->
    <?php else: ?>
    <?php require "paidMemes.php" ?>
    <?php endif; ?>
</div>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-1 my-5">
            <a href="logout.php" class="btn btn-primary">Logout</a>
        </div>
    </div>
</div>
<?php require "footer.php"; ?>

<!-- /sources/memes.html -->