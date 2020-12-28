<?php
error_reporting(0);
session_start();
if(isset($_GET['search'])){

    require "includes/databaseConnection.php";
    $pname =$_GET['search'];

    if($pname==='' || $pname===NULL || $pname[0]==="'")
        $emptyQuery = true;
    else{
        $sql = "SELECT * FROM `products` WHERE `productname` LIKE '%$pname%'";
        $result = mysqli_query($conn,$sql);
        
        if($result===false){
            $wrongInjection = true;
        }
        else
            $wrongInjection = false;
        $products = mysqli_fetch_all($result,MYSQLI_ASSOC);
    }
}

?>

<?php require "includes/header.php"; ?>

<body>

    <?php require "includes/topnav.php"; ?>

    <?php 
    
    if(isset($_SESSION['loggedIn'])){
        echo "
        <div class='container text-center'> <h1 class='row'>Flag: p_ctf{41w4y5_54n1t1z3_1nput} </h1> </div>
        ";
        exit();
    } 
    ?>

    <?php if(isset($emptyQuery) && $emptyQuery===true ): ?>
    <p class="container text-danger text-center">Search parameter cannot be empty!!</p>
    <?php elseif(isset($wrongInjection) && $wrongInjection===true ): ?>
    <p class="container text-danger text-center">Injection Failed</p>
    <?php endif; ?>
    <div class="container">
        <div class="row">
            <form class="d-flex py-5" action="<?php echo $_SERVER['PHP_SELF'];?>" method="GET">
                <input class="form-control me-2" type="search" placeholder="Search for soaps, biscuits, and more...." name="search" value="<?php echo (isset($_GET['search']))? htmlspecialchars($_GET['search']): NULL; ?>" required >
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
        </div>
        <?php if(isset($products)): ?>
        <?php foreach($products as $product): ?>
        <?php if($product['productid']==38) continue; ?>
        <div class="row my-2">
            <div class="card px-0">
                <div class="card-header">
                Product Name: <?php echo $product['productname']; ?>
                </div>
            <div class="card-body">
                <h5 class="card-title">Code: <?php echo $product['code']; ?> </h5>
            </div>
        </div>
        </div>
        <?php endforeach; ?>
        <?php endif; ?>
    </div>



    <?php require "includes/bootstrapScripts.php"; ?>
</body>