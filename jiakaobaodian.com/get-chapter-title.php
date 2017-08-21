<?php
require_once 'common.php';
$db = getConnection();
/*
 * api: http://api2.jiakaobaodian.com/api/open/exercise/chapter.htm?_r=11258564547825243087&course=kemu1&chapterId=121&carType=bus
 */

$baseurl = 'http://api2.jiakaobaodian.com/api/open/exercise/chapter.htm?_r=11258564547825243087';

/* configuration */
$ctype = array(
    'C1' => 'car',
    'A1' => 'bus',
    'A2' => 'truck',
    'D' => 'moto',
);
$stype = array(
    '1' => 'kemu1',
    '4' => 'kemu3',
);

$res = file_get_contents('chapter-id.txt');
$chapters = explode("\n", $res);
$fields_buf = array(
    'cid',
    'ctype',
    'stype',
    'title',
    'addtime',
);
foreach ($chapters as $key => $val) {
    if (!$val) {
        continue;
    }
    $chapter_info = explode("|", $val);
    $c = $chapter_info[0];
    $s = $chapter_info[1];
    $chapter_id = $chapter_info[2];
    $url = url_fact($baseurl, $stype[$s], $ctype[$c], $chapter_id);
    $info = json_decode(file_get_contents($url), true);
    $title = $info['data']['chapter']['title'];
    $values_buf = array(
        $chapter_id,
        $c,
        $s,
        $title,
        time(),
    );
    $sql = " INSERT INTO `cs_exam_chapters_tmp` (`".implode("`,`", $fields_buf)."`) VALUES ('".implode("','", $values_buf)."') ";
    $stmt = $db->query($sql);
    if ($stmt) {
        echo "$chapter_id-$c-$s 导入成功" ."\n";
    }
}

/* main work flow is ended here */

function url_fact($baseurl, $stype, $ctype, $chapterid) {
    return $baseurl . '&course=' . $stype . '&chapterId=' . $chapterid . '&carType=' . $ctype;
}
