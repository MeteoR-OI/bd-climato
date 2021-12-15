<?php
require("../highcharts4/mysql_connect.php");
mysql_connect($server,$user,$pass) or die ("Erreur SQL : ".mysql_error() );
mysql_select_db($db) or die ("Erreur SQL : ".mysql_error() );
// On récupère le timestamp du dernier enregistrement
$sql="select max(dateTime) from archiveweewx";
$query=mysql_query($sql);
$list=mysql_fetch_array($query);
// On détermine le stop et le start de façon à récupérer dans la prochaine requête
$stop=$list[0];
$start=$stop-(86400*366);
$sql = "SELECT dateTime, outTemp,  dewpoint, heatindex
FROM archiveweewx where dateTime >= '$start' and dateTime <= '$stop' ORDER BY 1";


                  $query=mysql_query($sql);
                  $i=0;
                  while ($list = mysql_fetch_assoc($query)) {
$time[$i]=($list['dateTime']+14400)*1000;
$outdoortemperature[$i]=$list['outTemp']*1;
$dewpoint[$i]=$list['dewpoint']*1;
$outdoorheatindex[$i]=$list['heatindex']*1;
$i++;
}
?>
<script type="text/javascript">
eval(<?php echo "'var time = ".json_encode($time)."'" ?>);
eval(<?php echo "'var dewpoint = ".json_encode($dewpoint)."'" ?>);
eval(<?php echo "'var outdoortemperature = ".json_encode($outdoortemperature)."'" ?>);
eval(<?php echo "'var outdoorheatindex = ".json_encode($outdoorheatindex)."'" ?>);
</script>
