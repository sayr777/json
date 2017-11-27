    var resp="0"; // resp from serv
    var tm="0";
    var st="0";
    var dt="0";

    function init() {

 
serNum   = new steelseries.DisplaySingle('serNum', {  width: 250,height: 50,valuesNumeric: false});       
Error_1   = new steelseries.DisplaySingle('Error_1', {  width: 250,height: 50,valuesNumeric: false, autoScroll: true});       
Error_2   = new steelseries.DisplaySingle('Error_2', {  width: 290,height: 50,valuesNumeric: false, autoScroll: true});       


setInterval(function(){ getData('m_81');}, 500);
    
}

 function parseArray(unitName,data) 
{
                    
                 for (var i = 0; i < data.length; i++) 
           {

                if(data[i].Name == unitName && data[i].Param == 'SerialNumber' ) { serNum.setValue("¹ : "+ data[i].SerialNumber); }

                if(data[i].Name == unitName && data[i].Param == 'Energy_0' ) { 
                                  
                                  document.getElementById("Energy_0_0").innerHTML=(data[i].Energy_0[0]*0.001).toFixed(3);
                                  document.getElementById("Energy_0_1").innerHTML=(data[i].Energy_0[1]*0.001).toFixed(3);
                                  document.getElementById("Energy_0_2").innerHTML=(data[i].Energy_0[2]*0.001).toFixed(3);
                                  document.getElementById("Energy_0_3").innerHTML=(data[i].Energy_0[3]*0.001).toFixed(3);
               }

                if(data[i].Name == unitName && data[i].Param == 'Energy_1' ) { 
                                  
                                  document.getElementById("Energy_1_0").innerHTML=(data[i].Energy_1[0]*0.001).toFixed(2);
                                  document.getElementById("Energy_1_1").innerHTML=(data[i].Energy_1[1]*0.001).toFixed(2);
                                  document.getElementById("Energy_1_2").innerHTML=(data[i].Energy_1[2]*0.001).toFixed(2);
                                  document.getElementById("Energy_1_3").innerHTML=(data[i].Energy_1[3]*0.001).toFixed(2);
               }

                if(data[i].Name == unitName && data[i].Param == 'Energy_2' ) { 
                                  
                                  document.getElementById("Energy_2_0").innerHTML=data[i].Energy_2[0]*0.001;
                                  document.getElementById("Energy_2_1").innerHTML=data[i].Energy_2[1]*0.001;
                                  document.getElementById("Energy_2_2").innerHTML=data[i].Energy_2[2]*0.001;
                                  document.getElementById("Energy_2_3").innerHTML=data[i].Energy_2[3]*0.001;
               }

                if(data[i].Name == unitName && data[i].Param == 'Energy_3' ) { 
                                  
                                  document.getElementById("Energy_3_0").innerHTML=data[i].Energy_3[0]*0.001;
                                  document.getElementById("Energy_3_1").innerHTML=data[i].Energy_3[1]*0.001;
                                  document.getElementById("Energy_3_2").innerHTML=data[i].Energy_3[2]*0.001;
                                  document.getElementById("Energy_3_3").innerHTML=data[i].Energy_3[3]*0.001;
               }

                if(data[i].Name == unitName && data[i].Param == 'Energy_4' ) { 
                                  
                                  document.getElementById("Energy_4_0").innerHTML=data[i].Energy_4[0]*0.001;
                                  document.getElementById("Energy_4_1").innerHTML=data[i].Energy_4[1]*0.001;
                                  document.getElementById("Energy_4_2").innerHTML=data[i].Energy_4[2]*0.001;
                                  document.getElementById("Energy_4_3").innerHTML=data[i].Energy_4[3]*0.001;
               }
               
                if(data[i].Name == unitName && data[i].Param == 'Amper' ) { 
                  document.getElementById("current_1").innerHTML=(data[i].Amper[0]*0.001).toFixed(2);
                  document.getElementById("current_2").innerHTML=(data[i].Amper[1]*0.001).toFixed(2);
                  document.getElementById("current_3").innerHTML=(data[i].Amper[2]*0.001).toFixed(2);
               }


                if(data[i].Name == unitName && data[i].Param == 'Volt' ) { 
                  document.getElementById("suply_1").innerHTML=(data[i].Volt[0]*0.01).toFixed(2);
                  document.getElementById("suply_2").innerHTML=(data[i].Volt[1]*0.01).toFixed(2);
                  document.getElementById("suply_3").innerHTML=(data[i].Volt[2]*0.01).toFixed(2);
               }



                if(data[i].Name == unitName && data[i].Param == 'Power_P' ) { 
                  document.getElementById("powerP_0").innerHTML=(data[i].Power_P[0]*0.01).toFixed(2);
                  document.getElementById("powerP_1").innerHTML=(data[i].Power_P[1]*0.01).toFixed(2);
                  document.getElementById("powerP_2").innerHTML=(data[i].Power_P[2]*0.01).toFixed(2);
                  document.getElementById("powerP_3").innerHTML=(data[i].Power_P[3]*0.01).toFixed(2);
               }

                if(data[i].Name == unitName && data[i].Param == 'Power_Q' ) { 
                  document.getElementById("powerQ_0").innerHTML=(data[i].Power_Q[0]*0.01).toFixed(2);
                  document.getElementById("powerQ_1").innerHTML=(data[i].Power_Q[1]*0.01).toFixed(2);
                  document.getElementById("powerQ_2").innerHTML=(data[i].Power_Q[2]*0.01).toFixed(2);
                  document.getElementById("powerQ_3").innerHTML=(data[i].Power_Q[3]*0.01).toFixed(2);
               }

                if(data[i].Name == unitName && data[i].Param == 'Power_S' ) { 
                  document.getElementById("powerS_0").innerHTML=(data[i].Power_S[0]*0.01).toFixed(2);                  
                  document.getElementById("powerS_1").innerHTML=(data[i].Power_S[1]*0.01).toFixed(2);                  
                  document.getElementById("powerS_2").innerHTML=(data[i].Power_S[2]*0.01).toFixed(2);                  
                  document.getElementById("powerS_3").innerHTML=(data[i].Power_S[3]*0.01).toFixed(2);                  

               }

                if(data[i].Name == unitName && data[i].Param == 'Cos_F' ) { 
                  document.getElementById("cos_F_0").innerHTML=(data[i].Cos_F[0]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_1").innerHTML=(data[i].Cos_F[1]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_2").innerHTML=(data[i].Cos_F[2]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_3").innerHTML=(data[i].Cos_F[3]*0.001).toFixed(3);                  

               }

                if(data[i].Name == unitName && data[i].Param == 'Freq' ) { 
                  document.getElementById("freq").innerHTML=(data[i].Freq*0.01).toFixed(2);                  

               }
                if(data[i].Name == unitName && data[i].Param == 'Angle' ) { 
                  document.getElementById("Angle_1").innerHTML=(data[i].Angle[0]*0.01).toFixed(2);                  
                  document.getElementById("Angle_2").innerHTML=(data[i].Angle[1]*0.01).toFixed(2);                  
                  document.getElementById("Angle_3").innerHTML=(data[i].Angle[2]*0.01).toFixed(2);                  

               }

                if(data[i].Name == unitName && data[i].Param == 'ErrConnect' ) { 
                     if(data[i].ErrConnect == 1)
                    {
                        Error_1.setValue("Connect OK  ");             
                    }
                        else
                    {

                          Error_1.setValue("Error Connect Error");             

                    }



              }






                if(data[i].Name == unitName && data[i].Param == 'ErrOpenChanel' ) 
              { 
                     if(data[i].ErrOpenChanel == 1)

                 {
                  Error_2.setValue("OpenChannel OK  ");             
                 }
                    else
                 {

                  Error_2.setValue("Error OpenChannel Error");             

                 }

               }




       }


}

                   
  function getData(unitName) 
{
         var dataReq='mercury';
//         unitName='m_43';

         if (window.XMLHttpRequest) {  xmlhttp=new XMLHttpRequest();                        }
         else                       {  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");      }



                  xmlhttp.open("GET","http://192.168.0.103:8080/"+dataReq,true);          
                  xmlhttp.setRequestHeader("Authorization", "Basic " + btoa("2:2"));
                  
                  xmlhttp.withCredentials = true;
                  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

                  xmlhttp.send(null);
                  xmlhttp.onreadystatechange=function()           
                 {
                       if (xmlhttp.readyState==4 && xmlhttp.status==200)
                      {
                        resp= xmlhttp.responseText;
                        parseResp=JSON.parse(resp);
                        data=parseResp.mercury;
                        parseArray(unitName,data);  
                      }
                      else {  Error_1.setValue("Error Connect to Slave ");      
                              Error_2.setValue("Error Connect to Slave");             


                      }       

                 }
          
                 

}