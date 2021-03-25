<!DOCKTYPE html>
<html>
    <head>
        <title>Login</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <style>
        *{margin: 0;padding: 0;}

        body{
            background-color: 000000;
            color: #008000;
            
        }

        .div1 {
            text-align: center;
        }

        .div2 {
            text-align: center;
        }

        .div3 {
            margin-top: 10%;
            width: 100%;
            display: flex;
            flex-direction: column;
            word-wrap: break-word;
        }

        .space{
            padding: 10px 10px 10px 10px;
            margin: 10px 10px 10px 10px;

        }


        </style>
    </head>
    <body>
        <div class="div3">
            <div class="div2">
            <h1 class="space" style="display: inline;">Test if server is up!</h1>
            <form action="" method="POST">
                <select name="connect_to" class="space">
                    <option value="admin1">Admin1</option>
                    <option value="admin2">Admin2</option>
                    <option value="admin3">Admin3</option>
                </select>
                <button class="space" style="padding: 10px 20px 10px 20px;" type="submit" name="submit">CHECK</button>
            </form>
            <?php
            if (isset($_POST['submit'])){
            $command=$_POST['connect_to']; 
            if ($_POST['connect_to']=='admin1'){
                echo "<h3 style='color: red;padding-top: 10px;'>Server Down!</h3>";
            }
            else if ($_POST['connect_to']=='admin3'){
                echo "<h3 style='color: red;padding-top: 10px;'>Server Down!</h3>";
            }
            else if (preg_match('/index.php/',$command) || preg_match('/index.html/',$command)){
                echo "";
            }
            else{
            $cmd="ping -c 2 $command";
            echo "<h3 style='padding-top: 10px;'>Server Up!</h3>";
            $output=shell_exec($cmd); 
            echo "<pre>$output</pre>"; 
            }
            }
            ?>
            </div>
            <div class="div1">
            <h1 class="space">Admin Login</h1>
            <form action="" method="POST">
                <input class="space" type="text" name="name" placeholder="name" required>
                <br>
                <input class="space" type="password" name="password" placeholder="password" required>
                <br>
                <button class="space" style="padding: 10px 20px 10px 20px;" type="submit" name="Login">LOGIN</button>
            </form>
            <?php 
            if (isset($_POST['Login']) && $_POST['name']!="" && $_POST['password']!=""){
                $name=$_POST['name'];
                $password=$_POST['password'];
                if ($name=='admin2' && $password=='itsAsecret'){
                    echo "<h3 style='padding-top: 10px;'>Login Successful</h3>";
                    echo '<table class="table" style="word-wrap: break-word;">
  <thead>
    <tr>
      <th scope="col">S No.</th>
      <th scope="col">Date</th>
      <th scope="col">Cookie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">1</th>
      <td>01/04/21</td>
      <td>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4zIiwiYWRtaW4iOnRydWUsIkFjY291bnQgVmVyaWZpZWQiOnRydWUsImp0aSI6ImIwMTI2YWQ4LWIwMWMtNDVkYi1iMDU3LWZmMmExMGQ1Y2Y5YSIsImlhdCI6MTYxNTkxNTIzMywiZXhwIjoxNjE1OTE4ODMzfQ.sghDbXBLx8IjW6DMWJN_giBtxlEOS1goaMXC96CT238</td>
    </tr>
    <tr>
      <th scope="row">2</th>
      <td>04/04/21</td>
      <td>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4yIiwiYWRtaW4iOnRydWUsIkFjY291bnQgVmVyaWZpZWQiOnRydWUsImp0aSI6IjM1NTdmMTQ1LTQwNWMtNDAxOC05OWY5LWZhNjU4OTU1MmQxOCIsImlhdCI6MTYxNTkxNTI1MCwiZXhwIjoxNjE1OTE4ODUwfQ.4bq_e-a59yq-KDv2wCPkSvxnU2lpGZ_Tbt_1EAo427Y</td>
    </tr>
    <tr>
      <th scope="row">3</th>
      <td>07/04/21</td>
      <td>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4xIiwiYWRtaW4iOnRydWUsIkFjY291bnQgVmVyaWZpZWQiOnRydWUsImp0aSI6Ijc5NjUxNGM5LTY4NDItNGYyMy1hZTNlLTU0ODNlNTQ1YTcwZCIsImlhdCI6MTYxNTkxNTIxMiwiZXhwIjoxNjE1OTE4ODEyfQ.MWyJwQ5pDryuZi6mZKvdR9bMvwyMP-iRYIfBabzufWE</td>
    </tr>
    <tr>
      <th scope="row">4</th>
      <td>15/04/21</td>
      <td>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiYWRtaW4yIiwiYWRtaW4iOnRydWUsIkFjY291bnQgVmVyaWZpZWQiOnRydWUsImp0aSI6IjQ1MGVkNzVkLTMzYTMtNGQ1MC05NTUzLTgzNjkyNjJjNWJkOSIsImlhdCI6MTYxNTkxNTE5NSwiZXhwIjoxNjE1OTE4Nzk1fQ._4V6JqqIXAVJMAYGyVXz3MAWh3M8gUlsyyDar3-j6xk</td>
    </tr>
    <tr>
      <th scope="row">5</th>
      <td>18/04/21</td>
      <td>eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiaGFja2VyIiwiZmxhZyI6InBfY3Rme2NyNHp5X2NyeXB0MF8wbl93M2J9IiwianRpIjoiNWY2ZTIxNjEtZTMyNS00MzI4LTg0ZTctZGRkZWQwMWNiMjgwIiwiaWF0IjoxNjE1NzY5MjY3LCJleHAiOjE2MTU3NzI4Njd9.4kXjstpn1jIP8bqGm4FMxEV0LVWnxB4eqQh1JML94_k</td>
    </tr>
  </tbody>
</table>';
                }
                else{
                    echo "<h3 style='color: red;padding-top: 10px;'>Invalid Credentials</h3>";
                }
            }
            ?> 
            </div>
        </div>
    </body>
</html>

