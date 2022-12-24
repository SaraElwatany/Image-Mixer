var canvas1 = document.getElementById("canvas1");

var lineOffset = 4;
var anchrSize = 2;
var mousedown = false;
var clickedArea = {box: -1, pos:'o'};
var x3 = -1;
var y3 = -1;
var x4 = -1;
var y4 = -1;
var boxes = [];
var tmpBox = null;

canvas1.onmousedown = function(e) {
  mousedown = true; 
  clickedArea = findCurrentArea(e.offsetX, e.offsetY);
  x3 = e.offsetX;
  y3 = e.offsetY;
  x4 = e.offsetX;
  y4 = e.offsetY;
};
canvas1.onmouseup = function(e) {
	if (clickedArea.box == -1 && tmpBox != null) {
     boxes.push(tmpBox);
    } 
  
  clickedArea = {box: -1, pos:'o'};
  tmpBox = null;
  mousedown = false;
  console.log(boxes);
};

canvas1.onmousemove = function(e) {
  if (mousedown && clickedArea.box == -1) {
    x3 = e.offsetX;
    y3 = e.offsetY;
    boxes.pop(tmpBox);
    redraw();
   }
   else if (mousedown && clickedArea.box != -1) {
    
    x3 = e.offsetX;
    y3 = e.offsetY;
    xOffset = x4 - x3;
    yOffset = y4 - y3;
    x3 = x4;
    y3 = y4;
    if (clickedArea.pos == 'i'  || clickedArea.pos == 'tl' || clickedArea.pos == 'l'  ||    clickedArea.pos == 'bl') {
      boxes[clickedArea.box].x3 += xOffset;
    }
    if (clickedArea.pos == 'i'  ||clickedArea.pos == 'tl' ||clickedArea.pos == 't'  ||   clickedArea.pos == 'tr') {
      boxes[clickedArea.box].y3 += yOffset;
    }
    if (clickedArea.pos == 'i'  || clickedArea.pos == 'tr' || clickedArea.pos == 'r'  ||clickedArea.pos == 'br') {
      boxes[clickedArea.box].x4 += xOffset;
    }
    if (clickedArea.pos == 'i' || clickedArea.pos == 'bl' || clickedArea.pos == 'b'  || clickedArea.pos == 'br') {
      boxes[clickedArea.box].y4 += yOffset; 
    }
    redraw();
  }
   
    x = x3;
    y = y3;
    w= width;
    h= height;

    const dict_values = {x3, y3, x4, y4}            //Pass the javascript variables to a dictionary.
    const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
    //console.log(s);                         // Prints the variables to console window, which are in the JSON format
    $.ajax({
    url:"/test",
    type:"POST",
    contentType: "application/json",
    data: JSON.stringify(s)});
}


function redraw() {
  var context1 = canvas1.getContext('2d');
  context1.clearRect(0, 0, 800, 600);
  context1.beginPath();
for (var i = 0; i < boxes.length; i++) {
    drawBoxOn(boxes[i], context1);
}
  
  if (clickedArea.box == -1) {
    tmpBox = newBox(x3, y3, x4, y4);
    if (tmpBox != null) {
      drawBoxOn(tmpBox, context1);
    }
  }
  
}


function findCurrentArea(x, y) {
  for (var i = 0; i < boxes.length; i++) {
  
    var box = boxes[i];
    xCenter = box.x3 + (box.x4 - box.x3) / 2;
    yCenter = box.y3 + (box.y4 - box.y3) / 2;
    if (box.x3 - lineOffset <  x && x < box.x3 + lineOffset) {
      if (box.y3 - lineOffset <  y && y < box.y3 + lineOffset) {
        return {box: i, pos:'tl'};
      } else if (box.y4 - lineOffset <  y && y < box.y4 + lineOffset) {
        return {box: i, pos:'bl'};
      } else if (yCenter - lineOffset <  y && y < yCenter + lineOffset) {
        return {box: i, pos:'l'};
      }
    } else if (box.x4 - lineOffset < x && x < box.x4 + lineOffset) {
      if (box.y3 - lineOffset <  y && y < box.y3 + lineOffset) {
        return {box: i, pos:'tr'};
      } else if (box.y4 - lineOffset <  y && y < box.y4 + lineOffset) {
        return {box: i, pos:'br'};
      } else if (yCenter - lineOffset <  y && y < yCenter + lineOffset) {
        return {box: i, pos:'r'};
      }
    } else if (xCenter - lineOffset <  x && x < xCenter + lineOffset) {
      if (box.y3 - lineOffset <  y && y < box.y3 + lineOffset) {
        return {box: i, pos:'t'};
      } else if (box.y4 - lineOffset <  y && y < box.y4 + lineOffset) {
        return {box: i, pos:'b'};
      } else if (box.y3 - lineOffset <  y && y < box.y4 + lineOffset) {
        return {box: i, pos:'i'};
      }
    } else if (box.x3 - lineOffset <  x && x < box.x4 + lineOffset) {
      if (box.y3 - lineOffset <  y && y < box.y4 + lineOffset) {
        return {box: i, pos:'i'};
      }
    }
  }
  
  return {box: -1, pos:'o'};
}

function newBox(x3, y3, x4, y4) {
  boxx3 = x3 < x4 ? x3 : x4;
  boxy3 = y3 < y4 ? y3 : y4;
  boxx4 = x3 > x4 ? x3 : x4;
  boxy4 = y3 > y4 ? y3 : y4;
  if (boxx4 - boxx3 > lineOffset * 2 && boxy4 - boxy3 > lineOffset * 2) {
    return {x3: boxx3,
            y3: boxy3,
            x4: boxx4,
            y4: boxy4,
            lineWidth: 1,
            color: 'DeepSkyBlue'};
  } else {
   
    return null;
  }
}

function drawBoxOn(box, context1) {
  xCenter = box.x3 + (box.x4 - box.x3) / 2;
  yCenter = box.y3 + (box.y4 - box.y3) / 2;
  
  context1.strokeStyle = box.color;
  context1.fillStyle = box.color;

  context1.rect(box.x3, box.y3, (box.x4 - box.x3), (box.y4 - box.y3));
  
  context1.lineWidth = box.lineWidth;
  context1.stroke();

  context1.fillRect(box.x3 - anchrSize, box.y3 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(box.x3 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(box.x3 - anchrSize, box.y4 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(xCenter - anchrSize, box.y3 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(xCenter - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(xCenter - anchrSize, box.y4 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(box.x4 - anchrSize, box.y3 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(box.x4 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context1.fillRect(box.x4 - anchrSize, box.y4 - anchrSize, 2 * anchrSize, 2 * anchrSize);
}
