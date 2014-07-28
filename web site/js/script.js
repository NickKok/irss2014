function kkk(Scenes) {   

  console.log(Scenes); 

  var getCombination = function(n, list) {
	var avail = new Array(list.length),
	    selection = new Array(n),
		i;
		
	for (i=0; i<avail.length; i+=1) avail[i]=i;
	
	for(i=0; i<n; i+=1){
	 var index= Math.floor(Math.random() * avail.length);
	 selection[i]= list[ avail[index]];
	 avail.splice(index,1);
	
	}

	return selection;
  };
  
  var rand = getCombination(3, Scenes);
      var rand1 = rand[0];
      var rand2 = rand[1];
      var rand3 = rand[2];
       
	document.getElementById("example_video_1").setAttribute("src",rand1);	
        document.getElementById("example_video_2").setAttribute("src", rand2);
        document.getElementById("example_video_3").setAttribute("src",rand3);    
     
         
         document.getElementById("radio1").value=rand3+";"+rand2+";"+rand1;
         document.getElementById("radio2").value=rand1+";"+rand3+";"+rand2;
         document.getElementById("radio3").value=rand1+";"+rand2+";"+rand3;
    
};

