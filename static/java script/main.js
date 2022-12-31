var canvas = document.getElementById("canvas");
var context = canvas.getContext('2d');
let newImage = new Image();
newImage.src =  "../static/Images/image1.png"
var lineOffset = 4;
var anchrSize = 3;
var mousedown = false;
var clickedArea = {box: -1, pos:'o'};
var x1 = -1;
var y1 = -1;
var x2 = -1;
var y2 = -1;
var boxes = [];
var tmpBox = null;




  document.getElementById("canvas").onmousedown = function(e) {
  mousedown = true; 
  clickedArea = findCurrentArea(e.offsetX, e.offsetY);
  x1 = e.offsetX;
  y1 = e.offsetY;
  x2 = e.offsetX;
  y2 = e.offsetY;
 
};



document.getElementById("canvas").onmouseup = function(e) {
	if (clickedArea.box == -1 && tmpBox != null ) {
   
     boxes.push(tmpBox);}
 clickedArea = {box: -1, pos:'o'};
  tmpBox = null;
  mousedown = false;
  console.log(boxes);
};

document.getElementById("canvas").onmousemove = function(e) {
  if (mousedown && clickedArea.box == -1) {
 
  if(boxes.length>1){
    boxes.pop(tmpBox);
  }
    x2 = e.offsetX;
    y2 = e.offsetY;
   redraw();
  
  } else if (mousedown && clickedArea.box != -1) {
    
    x2 = e.offsetX;
    y2 = e.offsetY;
    xOffset = x2 - x1;
    yOffset = y2 - y1;
    x1 = x2;
    y1 = y2;
    if (clickedArea.pos == 'i'  ||
        clickedArea.pos == 'tl' ||
        clickedArea.pos == 'l'  ||
        clickedArea.pos == 'bl') {
      boxes[clickedArea.box].x1 += xOffset;
    }
    if (clickedArea.pos == 'i'  ||
        clickedArea.pos == 'tl' ||
        clickedArea.pos == 't'  ||
        clickedArea.pos == 'tr') {
      boxes[clickedArea.box].y1 += yOffset;
    }
    if (clickedArea.pos == 'i'  ||
        clickedArea.pos == 'tr' ||
        clickedArea.pos == 'r'  ||
        clickedArea.pos == 'br') {
      boxes[clickedArea.box].x2 += xOffset;
    }
    if (clickedArea.pos == 'i'  ||
        clickedArea.pos == 'bl' ||
        clickedArea.pos == 'b'  ||
        clickedArea.pos == 'br') {
      boxes[clickedArea.box].y2 += yOffset;
    }
    
    redraw();
  }
}

function redraw() {

  // canvas.width = canvas.width;
 var context = document.getElementById("canvas").getContext('2d');
context.clearRect(0, 0,400, 210);
  context.beginPath();
for (var i = 0; i < boxes.length; i++) {
    drawBoxOn(boxes[i], context);
  
  }
  
  if (clickedArea.box == -1) {
    tmpBox = newBox(x1, y1, x2, y2);
    if (tmpBox != null) {
      drawBoxOn(tmpBox, context);
    }
  }
  
}

function findCurrentArea(x, y) {
  
    

  for (var i = 0; i < boxes.length; i++) {
   
    var box = boxes[i];
    xCenter = box.x1 + (box.x2 - box.x1) / 2;
    yCenter = box.y1 + (box.y2 - box.y1) / 2;
    if (box.x1 - lineOffset <  x && x < box.x1 + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y1 + lineOffset) {
        return {box: i, pos:'tl'};
      } else if (box.y2 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'bl'};
      } else if (yCenter - lineOffset <  y && y < yCenter + lineOffset) {
        return {box: i, pos:'l'};
      }
      // boxes.pop(box[i])
    } else if (box.x2 - lineOffset < x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y1 + lineOffset) {
        return {box: i, pos:'tr'};
      } else if (box.y2 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'br'};
      } else if (yCenter - lineOffset <  y && y < yCenter + lineOffset) {
        return {box: i, pos:'r'};
      }
    } // middle
    else if (xCenter - lineOffset <  x && x < xCenter + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y1 + lineOffset) {
        return {box: i, pos:'t'};
      } else if (box.y2 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'b'};
      }// center to delete rectangle 
       else if (boxes[i].y1 - lineOffset <  y && y < boxes[i].y2 + lineOffset) {
       
              boxes.pop(boxes[i]);
              // boxes.pop(boxes[1]);
             
      }

      
    } 
    else if (box.x1 - lineOffset <  x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'i'};
      }
    }
  
  }
    
 
  return {box: -1, pos:'o'};
}

function newBox(x1, y1, x2, y2,e) {
  x= x1;
  y= y1;
  f= x2;
  g= y2;
  const dict_values = {x , y, f, g}          //Pass the javascript variables to a dictionary.
  const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
  //console.log(s);                         // Prints the variables to console window, which are in the JSON format
  $.ajax({
  url:"/test",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(s)});

  boxX1 = x1 < x2 ? x1 : x2;
  boxY1 = y1 < y2 ? y1 : y2;
  boxX2 = x1 > x2 ? x1 : x2;
  boxY2 = y1 > y2 ? y1 : y2;
  if (boxX2 - boxX1 > lineOffset * 2 && boxY2 - boxY1 > lineOffset * 2) {
    return {x1: boxX1,
            y1: boxY1,
            x2: boxX2,
            y2: boxY2,
            lineWidth: 1,
            color: 'DeepSkyBlue'};
  } else {
   
    return null;
  }
}

function drawBoxOn(box, context,e) {

  context.strokeStyle = box.color;
  context.fillStyle = box.color;
  context.lineWidth = box.lineWidth;
  context.rect(box.x1, box.y1, (box.x2 - box.x1), (box.y2 - box.y1));
  context.stroke();
  // for (var i = 0; i < boxes.length; i++) {
   
    // var box = boxes[i];
    xCenter = box.x1 + (box.x2 - box.x1) / 2;
    yCenter = box.y1 + (box.y2 - box.y1) / 2;
    context.fillStyle = ["white", "red", "blue", "green", "pink", "purple", "black", "orange"];
  context.fillRect(box.x1 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize); 
  context.fillStyle="red";
  context.fillRect(xCenter - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  x= box.x1;
  y= box.y1;
  f= box.x2;
  g= box.y2;
  const dict_values = {x , y, f, g}          //Pass the javascript variables to a dictionary.
  const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
  //console.log(s);                         // Prints the variables to console window, which are in the JSON format
  $.ajax({
  url:"/test",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(s)});
// }
  	

}
var img1 = document.getElementById("magPhoto_1");
var img2 = document.getElementById("phasePhoto_1");
function inputImg() {
  // Get the checkbox
  var checkBox1 = document.getElementsByName("choise1");
  var checkBox2 = document.getElementsByName("choise2");

  var img1 = document.getElementsByName('canvas');
  var img2 = document.getElementsByName('canvas1');
  var out = document.getElementsByName('output');
  

  // If the checkbox is checked, display the output text
  if (checkBox1[0].checked == true){
    checkBox2[1].checked = true;
  }
  if (checkBox1[1].checked == true){
    checkBox2[0].checked = true;
  }

  if (checkBox1[0].checked == true){
    img1[0].style.display = "inline";
  } 
  else {
    img1[0].style.display = "none";
  }

  if (checkBox1[1].checked == true){
    img1[1].style.display = "inline";
  } else {
    img1[1].style.display = "none";
  }

  if (checkBox2[0].checked == true){
      img2[0].style.display = "inline";
    } else {
      img2[0].style.display = "none";
  }

  if (checkBox2[1].checked == true){
    img2[1].style.display = "inline";
  } else {
    img2[1].style.display = "none";
  }

  if (checkBox1[0].checked == true && checkBox2[1].checked == true) {
      out[1].style.display = 'inline';
  } else{
      out[1].style.display = 'none';
  }

  if (checkBox1[1].checked == true && checkBox2[0].checked == true) {
      out[0].style.display = 'inline';
  } else{
      out[0].style.display = 'none';
  }
}
