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
    if( strpos($str,"..")!==false ){
        echo "Oops! We couldn't find that file in this directory ";
        return false;
    }
    elseif (stripos($str, "php://input")!==false || 
            stripos($str ,"php://output")!==false || 
            stripos($str,"php://fd")!==false ||
            stripos($str, "php://stdin")!==false ||
            stripos($str,"php://stderr")!==false ||
            stripos($str, "php://stdout")!==false ){
                echo "That doesn't seem like a filename.";
                return false;

    }
    elseif (stripos($str, "etc")!==false || stripos($str, "proc")!==false || stripos($str, "log")!==false || stripos($str, "usr")!==false ){
        echo "Oops! We couldn't find that file in this directory ";
        return false;
    }
    elseif (stripos($str, "file://")!==false || stripos($str, "ssh2://")!== false || stripos($str, "expect://")!== false ){
        echo "That doesn't seem like a filename.";
        return false;
    }
    elseif(stripos($str, "shabot")!==false){
        return false;
    }
    else {
        return true;
    }
}
?>
