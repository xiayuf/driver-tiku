<?php
set_time_limit(0);
header("Content-type:text/html;charset=utf-8");

require_once 'common.php';
$db = getConnection();
/*
 * http://api2.jiakaobaodian.com/api/open/question/question-list.htm?_r=11258564547825243087&questionIds=803600
 */
$f = file_get_contents('resource_chapter_ids.txt');
$exam_ids = explode("\n", $f);
$baseurl = 'http://api2.jiakaobaodian.com/api/open/exercise/chapter.htm?_r=11258564547825243087';
$fields_buf = array(
	'chapterId',
	'ctype',
	'stype',
	'chapter',
	'title',
	'count',
);

$count = 0;
foreach ($exam_ids as $line) {
    $count++;
    echo "Grabling: " . $count . "\n";
    if ($line == '') {
        continue;
    }
    $exam = explode('|', $line);
    $ctype = $exam[0];
    $stype = $exam[1];
    $id = $exam[2];
    $url = $baseurl . '&course=' . $stype . '&carType=' . $ctype . '&chapterId=' . $id;

    $result = file_get_contents($url);
    if ($result) {
        $info = json_decode($result, true)['data']['chapter'];
    } else {
        continue;
    }
    $fn = '';

    $values_buf = array(
        $id,
        $ctype,
        $stype,
        addslashes($info['chapter']),
        addslashes($info['title']),
        addslashes($info['count']),
    );

    $save_ok = save_exam($db = $db, $fields = $fields_buf, $values = $values_buf);
    if ($save_ok) {
        echo $count . " saved ok! \n";
    } else {
        echo "save failed and exam info is $ctype-$stype-$id\n";
    }
}


function save_exam($db, $fields, $values, $table = 'cs_chapter_tmp') {
    $sql = " INSERT INTO `{$table}` (`".implode("`,`", $fields)."`) VALUES ('".implode("','", $values)."') ";
    $stmt = $db->query($sql);
    if ($stmt) {
        return true;
    } else {
        return false;
    }
}

?>
