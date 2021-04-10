<?php 
require "dbconn.php";
$check="SELECT * FROM `users` WHERE `username`='admin' ";
$result=mysqli_query($conn,$check);
$admin= mysqli_fetch_all($result,MYSQLI_ASSOC);
print_r($admin);
$password="supersecpctfadmin9031u4032911";
$hash=password_hash($password, PASSWORD_DEFAULT, array('cost'=>10));

if($admin){
    $sql="UPDATE `users` SET password = '$hash' WHERE `username`='admin' ";
    
    if(mysqli_query($conn,$sql)){
        echo "Admin Seeded Update";
    }
    else{
        echo mysqli_error($conn);
        echo "Error adding admin Update";
    }

} else {
    $sql="INSERT INTO `users`(`username`,`password`) VALUES('admin','$hash') ";
    
    if(mysqli_query($conn,$sql)){
        echo "Admin Seeded";
    }
    else{
        echo "Error adding admin";
    }
}
//$2y$10$qc7UI19IkllhGjEh3KJ4Xe4YZEq/.Rn3oLxZi6Q6l17M3Bi3AplMa
?>
