<?php
    session_start();

    if(isset($_SESSION['loggedIn'])){
        header("Location:index.php");
    }

    if(isset($_POST['login'])){
        require "includes/databaseConnection.php";

        $username=mysqli_real_escape_string($conn,$_POST['username']);
        $password=mysqli_real_escape_string($conn,$_POST['password']);
    
    
        $sql="SELECT * FROM `users` WHERE `username` LIKE '$username'";
  
        $result=mysqli_query($conn,$sql);
        $userDetails= mysqli_fetch_all($result,MYSQLI_ASSOC);
    
        if(empty($userDetails)){
        $noUser=true;
        $loginFail=true;
        }
    
        else{
            $userDetails=$userDetails[0];

            if(password_verify($password,$userDetails['password'])){
                
                $_SESSION['loggedIn']=true;
                $_SESSION['username']=$userDetails['username'];
                $_SESSION['userId']=$userDetails['user_id'];
                header("Location:index.php");
            }
            
            else {
                $wrongPassword=true;
                $loginFail=true;
            }
        
        }

        
    }

?>

<?php require "includes/header.php" ?>

<body>
  <nav class="navbar navbar-dark bg-dark mt-0 d-flex" id="topnav">
    <a href="index.php" class="navbar-brand mr-auto p-2">
      <img src="images/mm.png" alt="logo" height="50px">
    </a>
    <h1 class='text-white'>Moriarty Mart</h1>
    <a href="index.php" class="btn btn-outline-success p-2 mx-1">Home</a>
  </nav>

  <?php if(isset($loginFail)): ?>

  <?php if(isset($noUser)): ?>
  <div class="alert alert-danger alert-dismissible " role="alert">Incorrect username. Please try again.<button
      type="button" class="close" data-dismiss="alert">
      <span>&times;</span>
    </button>
  </div>
  <?php endif; ?>


  <?php if(isset($wrongPassword)): ?>
  <div class="alert alert-danger alert-dismissible " role="alert">Incorrect password. Please try again.<button
      type="button" class="close" data-dismiss="alert">
      <span>&times;</span>
    </button>
  </div>
  <?php endif; ?>
  <?php endif; ?>

  <div class="container text-center my-4">
    <h3>Login</h3>

    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="POST">

      <div class="form-group row my-3">
        <label for="username" class="col-sm-2 col-form-label">Username</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" name="username" id="username" placeholder="Username"
            value="<?php if(isset($_POST['login'])) echo htmlspecialchars($username); ?>" required>
        </div>
      </div>

      <div class="form-group row my-3">
        <label for="password" class="col-sm-2 col-form-label">Password</label>
        <div class="col-sm-10">
          <input type="password" class="form-control" name="password" id="password" placeholder="Password"
            value="<?php if(isset($_POST['login'])) echo htmlspecialchars($password); ?>" required>
        </div>
      </div>

      <div class="row justify-content-center">
        <input type="submit" class="btn btn-success" name="login" value="Login">
      </div>

    </form>
  </div>


  <?php require "includes/bootstrapScripts.php"; ?>


</body>