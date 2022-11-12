 function y(){
			var m=document.getElementsByClassName("move-text-component vertical-move-list-clickable");
			var o=m.length;
			var st="";
			for (i=0;i < o;i++){
			  try{
			  st += m.item(i).innerText + " ";
			  }
			  catch(e){}
			}
			//alert(st);
			return st;
			
			}

		  function sendData(){
			  //var data = new FormData();
			  //data.append('white', y());
			  var data=y();

			  var xhr = new XMLHttpRequest();
			  xhr.open('POST', 'http://127.0.0.1:8089/', true);

			  xhr.onload = function () {
				if(xhr.status !== 200){
				
				  return; 
				}

				alert(this.responseText);
			
				
				//window.open(this.responseText, '_blank');
			  };
			  xhr.send(data);
		  }
		  
		  document.onkeyup=function(e){
		  var e = e || window.event; // for IE to cover IEs window event-object
		  if(e.which == 96) {
			sendData();
			return false;
		  }
		}
