<?php
require_once 'common.php';
$db = getConnection();

$sql = " SELECT ctype, stype, chapterid from cs_exams_tmp group by ctype, stype, chapterid ";
$stmt = $db->query($sql);
$res = $stmt->fetchAll(PDO::FETCH_ASSOC);
$db = null;
$a = array();
foreach ($res as $val) {
    $a[] = implode('|', $val);
}
$msg = implode("\n", $a);
save_chapter('chapter-id.txt', $msg);

/* main work flow is ended here*/

function save_chapter($fn = 'log.txt', $msg = '') {
    if (file_exists($fn)) {
        $fp = fopen($fn, 'a');
    } else {
        $fp = fopen($fn, 'w');
    }
    if ($msg != '') {
        $msg .= "\n";
    }
    fwrite($fp, $msg);
    fclose($fp);
}
