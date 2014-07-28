<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>COMPARE SCENES</title>
<link href="css/templatemo_style.css" rel="stylesheet" type="text/css" />


<?php
$myarray = array();

$url = 'http://195.134.67.70/LOTRscenes/';

$html = file_get_contents($url);

$count = preg_match_all('/<td><a href="([^"]+)">[^<]*<\/a><\/td>/i', $html, $files);

for ($i = 1; $i < $count; ++$i) {
    $var=$url. $files[1][$i];
	
	array_push($myarray, $var);
    
}

session_start();
 $_SESSION['TextName']=null;
 $_SESSION['fname']=null;
 $_SESSION['array']=$myarray;

?>


<link rel="stylesheet" type="text/css" href="css/ddsmoothmenu.css" />
<link href="//vjs.zencdn.net/4.6/video-js.css" rel="stylesheet">
<script type="text/javascript" src="js/script.js"></script>


  
</head>
<body onload='kkk(<?php echo json_encode($_SESSION['array']) ?>)'>

	<div id="templatemo_top" style="background-color:black">
    	
    </div> <!-- end of top -->
    
    <div id="Compare" style="background-color:black"><center><h2 class="fancy-font"> <a href="http://irss.iit.demokritos.gr/"> irss 2014 </a> <font color="white"> <span style="font-size:120%">|</span> movie analysis project </font></h2> <br> </center><br></div>
        
                  
            <br>  <br>
    
	    <center><h4> Instructions: You will see 3 movie scenes. Choose the most <i>irrelevant</i> one.</h4></center>
		<center>
	  <div  class="inline">
		  <b>  Scene 1</b> <br> <br>
        <video id="example_video_1" class="video-js vjs-default-skin vjs-big-play-centered" 
  controls  width="400" height="200"
  poster="" src="" type="video/mp4"
  data-setup='{"example_option":true}'controls muted >
 <!--<source id="mp4_src1" src="" type='video/mp4' />-->

 <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
</video>


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		</div>
		
		<div  class="inline">
         <b> Scene 2</b><br> <br>
        <video id="example_video_2" class="video-js vjs-default-skin vjs-big-play-centered"
 controls  width="400" height="200"
  poster="" src="" type="video/mp4"
  data-setup='{"example_option":true}'>
 <source  src="4" type='video/mp4' />

 <p class="vjs-no-js">To view this video please enable JavaScript, and consider upgrading to a web browser that <a href="http://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a></p>
</video>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  &nbsp;&nbsp;&nbsp;  
        </div>
		
			  <div  class="inline">
            <b> Scene 3</b> <br> <br>
       <video id="example_video_3" class="video-js vjs-default-skin vjs-big-play-centered"
  controls  width="400" height="200"
   src="" type="video/mp4"
  data-setup='{"example_option":true}'>
 <source  src="4" type='video/mp4' />

 </video>  </div>  </center>      <br>  <br> 
            
             
         	<div class="parent">    
    <form action="page1.php" method="get">
	
	<center>
        <h4>Choose the most <i>irrelevant</i> one.</h4>
       
	   
	   
	      <table>
	   <tr>
	   <td>
		<input type="radio" id="radio1" name=scene value="A"> 1<br>
		</td><td> </td>
		</tr>
		
		 <tr>
	   <td>
		<input type="radio" id="radio2"  name=scene value="B" > 2<br>
		</td><td> </td>
		</tr>
		 <tr>
	   <td>
		<input type="radio" id="radio3"  name=scene value="C"> 3<br>
</td><td> </td>
		</tr>
		<tr>
	   <td>
         Last name: </td> <td><input type="text" name="lname" required></td></tr>
          <tr> <td></td><td> 
         <input type="submit" value="Next"></td></tr>
		 </table>
        </center>
		 
         
    </form>            
          </div>  
   
    
 

<br><br>

<div id="templatemo_footer_wrapper">
    <div id="templatemo_footer">
        Copyright © 2014 <a href="http://irss.iit.demokritos.gr/"> IRSS DEMOKRITOS</a> | 
                <div class="cleaner"></div>
    </div>
</div> 
  


</body>
</html>