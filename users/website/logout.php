<?php
session_start();
//phpinfo();
session_destroy();
header('Location: index.php');
exit;
?>