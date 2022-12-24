var canvas1 = document.getElementById("canvas1");
var context1 = canvas1.getContext('2d');
let newImage1 = new Image();
newImage1.src =  "../static/Images/image2.png"
var lineOffset = 4;
var anchrSize = 2;
var mousedown = false;
var clickedArea1 = {box: -1, pos:'o'};
var x1 = -1;
var y1 = -1;
var x2 = -1;
var y2 = -1;
var boxes1 = [];
var tmpBox1 = null;
window.onload = function() {
    context1.drawImage(newImage1, 0, 0, 250, 200);
   };

  
canvas1.onmousedown = function(e) {
  mousedown = true; 
  clickedArea1 = findCurrentArea1(e.offsetX, e.offsetY);
  x1 = e.offsetX;
  y1 = e.offsetY;
  x2 = e.offsetX;
  y2 = e.offsetY;
};
canvas1.onmouseup = function(e) {
	if (clickedArea1.box == -1 && tmpBox1 != null) {
     boxes1.push(tmpBox1);
    } 
  
  clickedArea1 = {box: -1, pos:'o'};
  tmpBox1 = null;
  mousedown = false;
  console.log(boxes1);
};

canvas1.onmousemove = function(e) {
  if (mousedown && clickedArea1.box == -1) {
    x2 = e.offsetX;
    y2 = e.offsetY;
    boxes1.pop(tmpBox1);
    redraw1();
   }
   else if (mousedown && clickedArea1.box != -1) {
    
    x2 = e.offsetX;
    y2 = e.offsetY;
    xOffset = x2 - x1;
    yOffset = y2 - y1;
    x1 = x2;
    y1 = y2;
    if (clickedArea1.pos == 'i'  || clickedArea1.pos == 'tl' || clickedArea1.pos == 'l'  ||    clickedArea1.pos == 'bl') {
      boxes1[clickedArea1.box].x1 += xOffset;
    }
    if (clickedArea1.pos == 'i'  ||clickedArea1.pos == 'tl' ||clickedArea1.pos == 't'  ||   clickedArea1.pos == 'tr') {
      boxes1[clickedArea1.box].y1 += yOffset;
    }
    if (clickedArea1.pos == 'i'  || clickedArea1.pos == 'tr' || clickedArea1.pos == 'r'  ||clickedArea1.pos == 'br') {
      boxes1[clickedArea1.box].x2 += xOffset;
    }
    if (clickedArea1.pos == 'i' || clickedArea1.pos == 'bl' || clickedArea1.pos == 'b'  || clickedArea1.pos == 'br') {
      boxes1[clickedArea1.box].y2 += yOffset; 
    }
    redraw1();
  }
   
    x = x1;
    y = y1;
   

    const dict_values = {x1, y1, x2, y2}            //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
    //console.log(s);                         // Prints the variables to console window, which are in the JSON format
    $.ajax({
    url:"/test",
    type:"POST",
    contentType: "application/json",
    data: JSON.stringify(s)});
}


function redraw1() {
  var context = canvas1.getContext('2d');
  context.clearRect(0, 0,250, 200);
  context.beginPath();
for (var i = 0; i < boxes1.length; i++) {
    drawBoxOn1(boxes1[i], context);
}
  
  if (clickedArea1.box == -1) {
    tmpBox1 = newBox1(x1, y1, x2, y2);
    if (tmpBox1 != null) {
      drawBoxOn1(tmpBox1, context);
    }
  }
  
}


function findCurrentArea1(x, y) {
  for (var i = 0; i < boxes1.length; i++) {
  
    var box = boxes1[i];
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
    } else if (box.x2 - lineOffset < x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y1 + lineOffset) {
        return {box: i, pos:'tr'};
      } else if (box.y2 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'br'};
      } else if (yCenter - lineOffset <  y && y < yCenter + lineOffset) {
        return {box: i, pos:'r'};
      }
    } else if (xCenter - lineOffset <  x && x < xCenter + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y1 + lineOffset) {
        return {box: i, pos:'t'};
      } else if (box.y2 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'b'};
      } else if (box.y1 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'i'};
      }
    } else if (box.x1 - lineOffset <  x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset <  y && y < box.y2 + lineOffset) {
        return {box: i, pos:'i'};
      }
    }
  }
  
  return {box: -1, pos:'o'};
}

function newBox1(x1, y1, x2, y2) {
  context1.drawImage(newImage1, 0, 0, 250, 200);
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

function drawBoxOn1(box, context) {
  context1.drawImage(newImage1, 0, 0, 250, 200);
  xCenter = box.x1 + (box.x2 - box.x1) / 2;
  yCenter = box.y1 + (box.y2 - box.y1) / 2;
  
  context.strokeStyle = box.color;
  context.fillStyle = box.color;

  context.rect(box.x1, box.y1, (box.x2 - box.x1), (box.y2 - box.y1));
  
  context.lineWidth = box.lineWidth;
  context.stroke();

  context.fillRect(box.x1 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
}