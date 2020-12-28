<nav class="navbar navbar-dark bg-dark mt-0 d-flex" id="topnav">
    <a href="index.php" class="navbar-brand mr-auto p-2">
      <img src="images/mm.png" alt="logo" height="50px">
    </a>
    <h1 class='text-white'>Moriarty Mart</h1>
    <?php if(isset($_SESSION['loggedIn']) && $_SESSION['loggedIn'] === true): ?>
        <a href="logout.php" class="btn btn-outline-success p-2 mx-1">Logout</a>
    <?php else: ?>
        <a href="login.php" class="btn btn-outline-success p-2 mx-1">Login</a>
    <?php endif; ?>
    
</nav>