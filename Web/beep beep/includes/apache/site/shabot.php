<?php  
$coordinates = new stdClass();
$coordinates->lat = 12.991375324106727;
$coordinates->lon =  80.21656349301354 ;
$coordinates->flag = "p_ctf{4r3_y0u_r3a11y_4_r0b0t_?_y35}";

function decoder($str){
    if(urldecode($str)===$str){
        return $str;
    }
    return decoder(urldecode($str));
}

function isSafe($str){
    $str = decoder($str);
    if( strpos($str,"..")!==false ||
    stripos($str, "php://input")!==false || 
    stripos($str, "etc")!==false || 
    stripos($str, "proc")!==false || 
    stripos($str, "log")!==false  ||
    stripos($str, "file")!==false
    ){
            return false;
        }
    else {
        return true;
    }
}
?>
