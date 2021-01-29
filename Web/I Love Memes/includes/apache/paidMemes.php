<?php if( !isset($_SESSION['loggedin'])){
    session_start();
}

if(isset($_SESSION['isPremium']) && $_SESSION['isPremium'] ==='0'  ){
    die();
}
    
?>
    <div class="row">
        <div class="col">
            <h4 style="color: green">Thanks for getting premium membership.</h4>
        </div>
    </div>
    <div class="row justify-content-center" class="my-3">
        <img src="images/supersecm3me1111.png" class="col-5" height="500px" alt="FLAG: p_ctf{m3m35_4r3_co0l_XD}" >
    </div>