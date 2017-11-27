    var resp="0"; // resp from serv
    var tm="0";
    var st="0";
    var dt="0";

    function init() {

 
serNum   = new steelseries.DisplaySingle('serNum', {  width: 250,height: 50,valuesNumeric: false});       
Error_1   = new steelseries.DisplaySingle('Error_1', {  width: 250,height: 50,valuesNumeric: false, autoScroll: true});       
Error_2   = new steelseries.DisplaySingle('Error_2', {  width: 290,height: 50,valuesNumeric: false, autoScroll: true});       


setInterval(function(){ getTemp();}, 1000);
    
}

  

  function getTemp() 
{
         var dataReq='mercury';
         if (window.XMLHttpRequest) {  xmlhttp=new XMLHttpRequest();                        }
         else                       {  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");      }

          xmlhttp.open("GET","http://192.168.0.103:8080/"+dataReq,true);
          xmlhttp.send(null);

         xmlhttp.onreadystatechange=function()

        {
               if (xmlhttp.readyState==4 && xmlhttp.status==200)
             {
             
                  resp= xmlhttp.responseText;
                  parseResp=JSON.parse(resp);

                  //data=parseResp.mercury[0][0];
          
                  //resp = (parseResp.mercury[1][0].m_81.Energy_0[0]);

                  serNum.setValue("¹ : "+ parseResp.mercury[0][0].m_81.SerialNumber);             

                  document.getElementById("Energy_0_0").innerHTML=parseResp.mercury[1][0].m_81.Energy_0[0]*0.001;
                  document.getElementById("Energy_0_1").innerHTML=parseResp.mercury[1][0].m_81.Energy_0[1]*0.001;
                  document.getElementById("Energy_0_2").innerHTML=parseResp.mercury[1][0].m_81.Energy_0[2]*0.001;
                  document.getElementById("Energy_0_3").innerHTML=parseResp.mercury[1][0].m_81.Energy_0[3]*0.001;

                  document.getElementById("Energy_1_0").innerHTML=parseResp.mercury[2][0].m_81.Energy_1[0]*0.001;
                  document.getElementById("Energy_1_1").innerHTML=parseResp.mercury[2][0].m_81.Energy_1[1]*0.001;
                  document.getElementById("Energy_1_2").innerHTML=parseResp.mercury[2][0].m_81.Energy_1[2]*0.001;
                  document.getElementById("Energy_1_3").innerHTML=parseResp.mercury[2][0].m_81.Energy_1[3]*0.001;

                  document.getElementById("Energy_2_0").innerHTML=parseResp.mercury[3][0].m_81.Energy_2[0]*0.001;
                  document.getElementById("Energy_2_1").innerHTML=parseResp.mercury[3][0].m_81.Energy_2[1]*0.001;
                  document.getElementById("Energy_2_2").innerHTML=parseResp.mercury[3][0].m_81.Energy_2[2]*0.001;
                  document.getElementById("Energy_2_3").innerHTML=parseResp.mercury[3][0].m_81.Energy_2[3]*0.001;

                  document.getElementById("Energy_3_0").innerHTML=parseResp.mercury[4][0].m_81.Energy_3[0]*0.001;
                  document.getElementById("Energy_3_1").innerHTML=parseResp.mercury[4][0].m_81.Energy_3[1]*0.001;
                  document.getElementById("Energy_3_2").innerHTML=parseResp.mercury[4][0].m_81.Energy_3[2]*0.001;
                  document.getElementById("Energy_3_3").innerHTML=parseResp.mercury[4][0].m_81.Energy_3[3]*0.001;
                  
                  document.getElementById("Energy_4_0").innerHTML=parseResp.mercury[5][0].m_81.Energy_4[0]*0.001;
                  document.getElementById("Energy_4_1").innerHTML=parseResp.mercury[5][0].m_81.Energy_4[1]*0.001;
                  document.getElementById("Energy_4_2").innerHTML=parseResp.mercury[5][0].m_81.Energy_4[2]*0.001;
                  document.getElementById("Energy_4_3").innerHTML=parseResp.mercury[5][0].m_81.Energy_4[3]*0.001;
                

                  document.getElementById("current_1").innerHTML=(parseResp.mercury[6][0].m_81.Amper[0]*0.001).toFixed(2);
                  document.getElementById("current_2").innerHTML=(parseResp.mercury[6][0].m_81.Amper[1]*0.001).toFixed(2);
                  document.getElementById("current_3").innerHTML=(parseResp.mercury[6][0].m_81.Amper[2]*0.001).toFixed(2);
                          
                  document.getElementById("suply_1").innerHTML=(parseResp.mercury[7][0].m_81.Volt[0]*0.01).toFixed(2);
                  document.getElementById("suply_2").innerHTML=(parseResp.mercury[7][0].m_81.Volt[1]*0.01).toFixed(2);
                  document.getElementById("suply_3").innerHTML=(parseResp.mercury[7][0].m_81.Volt[2]*0.01).toFixed(2);
                  document.getElementById("powerP_0").innerHTML=(parseResp.mercury[8][0].m_81.Power_P[0]*0.01).toFixed(2);
                  document.getElementById("powerP_1").innerHTML=(parseResp.mercury[8][0].m_81.Power_P[1]*0.01).toFixed(2);
                  document.getElementById("powerP_2").innerHTML=(parseResp.mercury[8][0].m_81.Power_P[2]*0.01).toFixed(2);
                  document.getElementById("powerP_3").innerHTML=(parseResp.mercury[8][0].m_81.Power_P[3]*0.01).toFixed(2);

                  document.getElementById("powerQ_0").innerHTML=(parseResp.mercury[9][0].m_81.Power_Q[0]*0.01).toFixed(2);
                  document.getElementById("powerQ_1").innerHTML=(parseResp.mercury[9][0].m_81.Power_Q[1]*0.01).toFixed(2);
                  document.getElementById("powerQ_2").innerHTML=(parseResp.mercury[9][0].m_81.Power_Q[2]*0.01).toFixed(2);
                  document.getElementById("powerQ_3").innerHTML=(parseResp.mercury[9][0].m_81.Power_Q[3]*0.01).toFixed(2);

                  document.getElementById("powerS_0").innerHTML=(parseResp.mercury[10][0].m_81.Power_S[0]*0.01).toFixed(2);                  
                  document.getElementById("powerS_1").innerHTML=(parseResp.mercury[10][0].m_81.Power_S[1]*0.01).toFixed(2);                  
                  document.getElementById("powerS_2").innerHTML=(parseResp.mercury[10][0].m_81.Power_S[2]*0.01).toFixed(2);                  
                  document.getElementById("powerS_3").innerHTML=(parseResp.mercury[10][0].m_81.Power_S[3]*0.01).toFixed(2);                  

                  document.getElementById("cos_F_0").innerHTML=(parseResp.mercury[11][0].m_81.Cos_F[0]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_1").innerHTML=(parseResp.mercury[11][0].m_81.Cos_F[1]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_2").innerHTML=(parseResp.mercury[11][0].m_81.Cos_F[2]*0.001).toFixed(3);                  
                  document.getElementById("cos_F_3").innerHTML=(parseResp.mercury[11][0].m_81.Cos_F[3]*0.001).toFixed(3);                  
                  
                  document.getElementById("freq").innerHTML=(parseResp.mercury[12][0].m_81.Freq*0.01).toFixed(2);                  

                  document.getElementById("Angle_1").innerHTML=(parseResp.mercury[13][0].m_81.Angle[0]*0.01).toFixed(2);                  
                  document.getElementById("Angle_2").innerHTML=(parseResp.mercury[13][0].m_81.Angle[1]*0.01).toFixed(2);                  
                  document.getElementById("Angle_3").innerHTML=(parseResp.mercury[13][0].m_81.Angle[2]*0.01).toFixed(2);                  
                  if(parseResp.mercury[14][0].m_81.ErrConnect == 1)
                 {
                  Error_1.setValue("Connect OK  ");             
                 }
                    else
                 {

                  Error_1.setValue("Error Connect Error");             

                 }


                  if(parseResp.mercury[15][0].m_81.ErrOpenChanel == 1)
                 {
                  Error_2.setValue("OpenChannel OK  ");             
                 }
                    else
                 {

                  Error_2.setValue("Error OpenChannel Error");             

                 }


//                resp = (data.Temper_1.Val[0]*0.1).toFixed(2);
  //            t=new Date(data.Temper_1.ts);            
    //          tm=(t.getHours()+3)+":"+ t.getMinutes()+":"+ t.getSeconds()+":"+t.getMilliseconds();
      //        dt=t.getDate()+"."+ t.getMonth()+"."+t.getFullYear();

        //      st=data.Temper_1.Status
            //  resp=0;
              }
              

        }
 }

