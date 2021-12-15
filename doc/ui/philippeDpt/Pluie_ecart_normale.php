<?php
// appel du script de connexion
require("../highcharts4/mysql_connect.php");




$start=mktime(0,0,0,1,1,2020);
$stop =mktime(23,59,59,12,31,2020);

$sql = "SELECT dateTime, SUM(`sum`*10) as PluieJour, substr(from_unixtime(dateTime)+0, 1, 6) AS AnneeMois FROM `archive_day_rain` WHERE dateTime > '$start' AND dateTime <= '$stop' GROUP BY AnneeMois";
$query = mysql_query($sql);
$i=0;
while ($list = mysql_fetch_assoc($query)) {
if (date("I",time())==0) {
   $time[$i]=($list['dateTime']+14400)*1000;
   }
else {
   $time[$i]=($list['dateTime']+14400)*1000;
  }

$Rain_jour[$i]=$list['PluieJour']*1;

   if (date("m",$time[$i]/1000)==1) {$NormaleMensuelle[$i]=278.6;}
   elseif (date("m",$time[$i]/1000)==2) {$NormaleMensuelle[$i]=351;}
   elseif (date("m",$time[$i]/1000)==3) {$NormaleMensuelle[$i]=232.5;}
   elseif (date("m",$time[$i]/1000)==4) {$NormaleMensuelle[$i]=154.3;}
   elseif (date("m",$time[$i]/1000)==5) {$NormaleMensuelle[$i]=97.6;}
   elseif (date("m",$time[$i]/1000)==6) {$NormaleMensuelle[$i]=76.9;}
   elseif (date("m",$time[$i]/1000)==7) {$NormaleMensuelle[$i]=57.8;}
   elseif (date("m",$time[$i]/1000)==8) {$NormaleMensuelle[$i]=57.8;}
   elseif (date("m",$time[$i]/1000)==9) {$NormaleMensuelle[$i]=50;}
   elseif (date("m",$time[$i]/1000)==10) {$NormaleMensuelle[$i]=43.4;}
   elseif (date("m",$time[$i]/1000)==11) {$NormaleMensuelle[$i]=70;}
   elseif (date("m",$time[$i]/1000)==12) {$NormaleMensuelle[$i]=188.7;}

$Ecart[$i]=$Rain_jour[$i]-$NormaleMensuelle[$i];


$i++;
}

$Normale=array(278.6, 351, 232.5, 154.3, 97.6, 76.9, 57.8, 57.8, 50, 43.4, 70, 188.7);
$Time=array("Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","Septembre","Octobre","Novembre","Décembre");
$Pluie=array($Rain_jour[0],$Rain_jour[1],$Rain_jour[2],$Rain_jour[3],$Rain_jour[4],$Rain_jour[5],$Rain_jour[6],$Rain_jour[7],$Rain_jour[8],$Rain_jour[9],$Rain_jour[10],$Rain_jour[11],$Rain_jour[12]);
$Normale_an= 1658.6;
$Pluie_an = $Rain_jour[0]+$Rain_jour[1]+$Rain_jour[2]+$Rain_jour[3]+$Rain_jour[4]+$Rain_jour[5]+$Rain_jour[6]+$Rain_jour[7]+$Rain_jour[8]+$Rain_jour[9]+$Rain_jour[10]+$Rain_jour[11]+$Rain_jour[12];
$Ecart=array($Ecart[0],$Ecart[1],$Ecart[2],$Ecart[3],$Ecart[4],$Ecart[5],$Ecart[6],$Ecart[7],$Ecart[8],$Ecart[9],$Ecart[10],$Ecart[11],$Ecart[12]);

 ?>
<script type="text/javascript">
eval(<?php echo  "'var dTime =  ".json_encode($Time)."'" ?>);
eval(<?php echo  "'var dPluie =  ".json_encode($Pluie)."'" ?>);
eval(<?php echo  "'var dNormale =  ".json_encode($Normale)."'" ?>);
eval(<?php echo  "'var dEcart =  ".json_encode($Ecart)."'" ?>);
</script>
