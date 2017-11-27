    var resp="0"; // resp from serv
    var tm="0";
    var st="0";
    var dt="0";
    var mod_1=0;
    function init() {

 var sections = Array( steelseries.Section(22, 24, 'rgba(0, 0, 220, 0.3)'),     
                       steelseries.Section(25, 27, 'rgba(0, 220, 0, 0.3)'),     
                       steelseries.Section(28, 30, 'rgba(220, 0, 0, 0.3)'));     

//----------------------gradient---------------------					   
 var  valGrad = new steelseries.gradientWrapper(  20, // 
                                               85,
                                             [ 0, 0.33, 0.66, 0.85, 1],
                                             [ new steelseries.rgbaColor(0, 0, 200, 1),    
                                               new steelseries.rgbaColor(0, 200, 0, 1),    
                                               new steelseries.rgbaColor(200, 200, 0, 1),  
                                               new steelseries.rgbaColor(200, 0, 0, 1),    
                                               new steelseries.rgbaColor(200, 0, 0, 1) ]);											   
  
var  valGrad2 = new steelseries.gradientWrapper(  5, // 
                                               17,
                                             [ 0, 0.33, 0.66, 0.85, 1],
                                             [ new steelseries.rgbaColor(0, 0, 200, 1),    
                                               new steelseries.rgbaColor(0, 200, 0, 1),    
                                               new steelseries.rgbaColor(200, 200, 0, 1),  
                                               new steelseries.rgbaColor(200, 0, 0, 1),    
                                               new steelseries.rgbaColor(200, 0, 0, 1) ]);	
 
var  valGrad3 = new steelseries.gradientWrapper(  4, // 
                                               17,
                                             [ 0, 0.33, 0.66, 0.85, 1],

                                             [ 

                                               new steelseries.rgbaColor(200, 0, 0, 1),
                                               new steelseries.rgbaColor(200, 0, 0, 1), 
                                               new steelseries.rgbaColor(200, 200, 0, 1), 
                                               new steelseries.rgbaColor(0, 200, 0, 1),  
                                               new steelseries.rgbaColor(0, 0, 200, 1)   ]);

 var areas = Array(steelseries.Section(28, 30, 'rgba(220, 0, 0, 0.3)'));

//----------temper
var tempmeter = new steelseries.RadialBargraph('tempmeter', {
                            minValue: 0,      
  			    maxValue: 100,      
			    threshold: 50, 
                            valueGradient: valGrad, 
		            useValueGradient: true,	
                            backgroundColor: steelseries.BackgroundColor.WHITE,
                            gaugeType: steelseries.GaugeType.TYPE2,
                            size: 201,
                            titleString: 'Температура',
                            unitString: 'в системе',
                            lcdVisible: true
                        });
//----------вольтметр
  var voltmetr = new steelseries.RadialBargraph('voltmetr', {
                    gaugeType: steelseries.GaugeType.TYPE3,
					valueGradient: valGrad3, 
					useValueGradient: true,	
					size: 200,      
					minValue: 0,  
                                        maxValue: 2000,  
					thresholdRising: 8,  
                                        titleString: "Температура",                                
                                        unitString: "батареи",          
                                        frameDesign: steelseries.FrameDesign.BLACK_METAL,
                                        backgroundColor: steelseries.BackgroundColor.LIGHT_GRAY,
               
                    }); 
//----------измеритель тока
var current = new steelseries.RadialBargraph('current', {
                    gaugeType: steelseries.GaugeType.TYPE3, 
					valueGradient: valGrad2, 
					useValueGradient: true,					
					size: 200,       
					minValue: 0,   
                                        maxValue: 100,   
					threshold: 4.6,  
                                        titleString: "Температура",                                
                                        unitString: "нагрузки",          
                                        frameDesign: steelseries.FrameDesign.BLACK_METAL,
                
                                        valueColor: steelseries.ColorDef.YELLOW,  
                                        lcdColor: steelseries.LcdColor.BLUE,      
                                        ledColor: steelseries.LedColor.YELLOW_LED,  
                    }); 

//------------шумомер
  var sound = new steelseries.Radial('sound', {
                    gaugeType: steelseries.GaugeType.TYPE2,
					size: 200,       
					minValue: 0,   
                                        maxValue: 100,   
                                        threshold: 400, 
                                        section: Array(steelseries.Section(25,28,'rgba(0,255,0,0.3)')), 
                                        area: Array(steelseries.Section(28,30,'rgba(255,0,0,0.5)')), 
                    titleString: 'Температура', 
                    unitString: 'генератора', 
                    frameDesign: steelseries.FrameDesign.CHROME, 
                    backgroundColor: steelseries.BackgroundColor.LIGHT_GRAY, 
                    pointerType: steelseries.PointerType.TYPE2, 
                    pointerColor: steelseries.ColorDef.BLUE,    
                    lcdColor: steelseries.LcdColor.BLUE2,                    
                    ledColor: steelseries.LedColor.BLUE_LED,    
                    });


//------------------------move sensor
  move = new steelseries.LinearBargraph('move', {

                            width: 350,
                            height: 80,
                            minValue: 0,   
                            maxValue: 100,   
                            titleString: "Температура",
                            unitString: "move",
                            threshold: 10,
                            lcdVisible: true
                            });

//------------датчик света
  light = new steelseries.Radial('light', {
                    gaugeType: steelseries.GaugeType.TYPE2,
					size: 200,       
					minValue: 0,   
                                        maxValue: 100,   
                                        threshold: 400, 
                                        section: Array(steelseries.Section(25,28,'rgba(0,255,0,0.3)')), 
                                        area: Array(steelseries.Section(28,30,'rgba(255,0,0,0.5)')), 
                    titleString: 'Температура', 
                    unitString: 'света', 
                    frameDesign: steelseries.FrameDesign.CHROME, 
                    backgroundColor: steelseries.BackgroundColor.LIGHT_GRAY, 
                    pointerType: steelseries.PointerType.TYPE2, 
                    pointerColor: steelseries.ColorDef.BLUE,    
                    lcdColor: steelseries.LcdColor.BLUE2,                    
                    ledColor: steelseries.LedColor.BLUE_LED,    
                    });
//-----lcd temp

       lcd1 = new steelseries.DisplaySingle('lcd1', {
                            width: 200,
                            height: 50,
                            valuesNumeric: true,
                            unitStringVisible: true,
                            headerString: "Температура в системе",
                            headerStringVisible: true,
                            unitString: " С"
                            }); 



//----------------- U
       lcd2 = new steelseries.DisplaySingle('lcd2', {
                            width: 200,
                            height: 50,
                            valuesNumeric: true,
                            unitStringVisible: true,
                            headerString: "Температура батареи",
                            headerStringVisible: true,
                            unitString: " B"
                            });
//-------------I
       lcd3 = new steelseries.DisplaySingle('lcd3', {
                            width: 200,
                            height: 50,
                            valuesNumeric: true,
                            unitStringVisible: true,
                            headerString: "Температура батареи",
                            headerStringVisible: true,
                            unitString: " А"

                            });
//-----------state
        lcd4 = new steelseries.DisplaySingle('lcd4', {
                            width: 200,
                            height: 50,
                            valuesNumeric: false
                            });
//--------------resp
txtled = new steelseries.DisplaySingle('txtled', {
                            width: 200,
                            height: 50,
                            //value: "---",
                            autoScroll: true,
                            valuesNumeric: false
                            });


//-----------getCommand
        lcd5 = new steelseries.DisplaySingle('lcd5', {
                            width: 200,
                            height: 50,
                            valuesNumeric: false
                            });



//-------------часы
var  clock1 = new steelseries.Clock('canvasClock1', { width: 301,height: 301});
       
setInterval(function(){ setValue(voltmetr,tempmeter,current,sound);}, 1000);
    
}

  
function setValue(voltmetr,tempmeter,current,sound) {
       
          getTemp();

          voltmetr.setValue(mod_1);
          tempmeter.setValue(resp);
          current.setValue(resp);
          sound.setValue(resp);
          light.setValue(resp);
          move.setValue(resp);
          lcd1.setValue(parseFloat(resp));
          lcd2.setValue(parseFloat(resp));
          lcd3.setValue(parseFloat(resp));
          lcd4.setValue(dt);
          lcd5.setValue(tm);
          txtled.setValue("State: "+st +" ");


}

var monitor = document.querySelector('#monitor');

    function log(str)

    {
var h=(new Date()).getHours();
var m=(new Date()).getMinutes();
var s=(new Date()).getSeconds();
//       monitor.value +=h +":" + m + ":" + s + "->" + str;
       monitor.value += str;

       monitor.scrollTop += 30;
       monitor.focus();
    }

  

  function getTemp() 
{
         var dataReq='temp';
         var login='222', passw='111';
         var ip='192.168.0.156';
         var port='8080';

         if (window.XMLHttpRequest) {  xmlhttp=new XMLHttpRequest();                        }
         else                       {  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");      }


                  xmlhttp.open("GET","https://"+ip+":"+port+"/"+dataReq,true);          
                  xmlhttp.setRequestHeader("Authorization", "Basic " + btoa(login+":"+passw));
                  
                  xmlhttp.withCredentials = true;
                  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send(null);


         xmlhttp.onreadystatechange=function()

        {
               if (xmlhttp.readyState==4 && xmlhttp.status==200)
             {
             
              resp= xmlhttp.responseText;
              parseResp=JSON.parse(resp);
              data=parseResp.temp[0];
              
              log("Val :" + data +"\n");
              resp=data*0.1;
             
              }
              

        }



 }

