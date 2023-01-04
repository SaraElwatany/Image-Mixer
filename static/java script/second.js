// var canvas1 = document.getElementById("canvas1");
var context1 = canvas1.getContext('2d');
let newImage1 = new Image();
newImage1.src =  "../static/Images/phase2.png"
function mag2(opto2) {
  for (var i = 0; i < boxes1.length; i++) {
    boxes1.pop(boxes1[0]);
    boxes1.pop(boxes1[1]);
  }

  newImage1.src =  "../static/Images/magnitude2.png"  
  context1.drawImage(newImage1, 0, 0, 440, 230);

  n1= opto2;
   const dict_boxe = {n1}          //Pass the javascript variables to a dictionary.
   const b = JSON.stringify(dict_boxe);      // Stringify converts a JavaScript object or value to a JSON string
   $.ajax({
   url:"/opt2",
   type:"POST",
   contentType: "application/json",
   data: JSON.stringify(b)});
}
function phase2(opto2) {
  for (var i = 0; i < boxes1.length; i++) {
    boxes1.pop(boxes1[0]);
    boxes1.pop(boxes1[1]);
  }
 newImage1.src =  "../static/Images/phase2.png"  
 context1.drawImage(newImage1, 0, 0, 440, 230);

 n2= opto2;
  const dict_box = {n2}          //Pass the javascript variables to a dictionary.
  const b1 = JSON.stringify(dict_box);      // Stringify converts a JavaScript object or value to a JSON string
  $.ajax({
  url:"/opt2",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(b1)});
}
var lineOffset = 4;
var anchrSize = 3;
var mousedown = false;
var clickedArea1 = {box: -1, pos:'o'};
var x1 = -1;
var y1 = -1;
var x2 = -1;
var y2 = -1;
var X3= -1;
var Y3= -1;
var F3= -1;
var G3= -1;
var boxno2= -1;
var boxes1 = [];
var tmpBox1 = null;

   

document.getElementById("canvas1").onmousedown = function(e) {
  mousedown = true; 
  clickedArea1 = findCurrentArea1(e.offsetX, e.offsetY);
  x1 = e.offsetX;
  y1 = e.offsetY;
  x2 = e.offsetX;
  y2 = e.offsetY;
  
  const dict_values = {boxno2, X3 , Y3, F3, G3}          //Pass the javascript variables to a dictionary.
  const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
  $.ajax({
  url:"/test2",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(s)});
};


// let newImage2 = new Image(); 
// newImage2.src =  "../static/Images/output.png"
// var output=document.getElementById("out");
document.getElementById("canvas1").onmouseup = function(e) {
  // newImage2.src =  "../static/Images/output.png"
  // output.scr="../static/Images/output.png"
	if (clickedArea1.box == -1 && tmpBox1 != null) {
     boxes1.push(tmpBox1);
    } 
  
  clickedArea1 = {box: -1, pos:'o'};
  tmpBox1 = null;
  mousedown = false;
  console.log(boxes1);
  const dict_values = {boxno2, X3 , Y3, F3, G3}         //Pass the javascript variables to a dictionary.
  const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
  $.ajax({
  url:"/test2",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(s)});
  
};

document.getElementById("canvas1").onmousemove = function(e) {
  if (mousedown && clickedArea1.box == -1) {
    if(boxes1.length==2){
      boxes1.pop(tmpBox1);
    }
    x2 = e.offsetX;
    y2 = e.offsetY;
    // boxes1.pop(tmpBox1);
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
  const dict_values = {boxno2, X3 , Y3, F3, G3}           //Pass the javascript variables to a dictionary.
  const s = JSON.stringify(dict_values);      // Stringify converts a JavaScript object or value to a JSON string
  $.ajax({
  url:"/test2",
  type:"POST",
  contentType: "application/json",
  data: JSON.stringify(s)});
  // const dict_valu = {boxno2, X3 , Y3, F3, G3}          //Pass the javascript variables to a dictionary.
  // const s1 = JSON.stringify(dict_valu);      // Stringify converts a JavaScript object or value to a JSON string
  // $.ajax({
  // url:"/test2",
  // type:"POST",
  // contentType: "application/json",
  // data: JSON.stringify(s1)});
}


function redraw1() {
  var context = canvas1.getContext('2d');
  context.clearRect(0, 0,440, 230);
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
    for (var i = 0; i < boxes1.length; i++) {
    boxno2= i;
    X3= boxes1[i].x1;
    Y3= boxes1[i].y1;
    F3= boxes1[i].x2;
    G3= boxes1[i].y2;
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
        boxes1.pop(boxes1[0]);
        boxes1.pop(boxes1[1]);
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

  context1.drawImage(newImage1, 0, 0, 440, 230);
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
  context.strokeStyle = box.color;
  context.fillStyle = box.color;
  context.lineWidth = box.lineWidth;
  context1.drawImage(newImage1, 0, 0, 440, 230);
  context.rect(box.x1, box.y1, (box.x2 - box.x1), (box.y2 - box.y1));
    
  context.stroke();
  

  
  for (var j = 0; j < boxes1.length; j++) {
    
    var box = boxes1[j];
    xCenter = box.x1 + (box.x2 - box.x1) / 2;
    yCenter = box.y1 + (box.y2 - box.y1) / 2;
    context.fillStyle="blue";
  context.fillRect(box.x1 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x1 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(box.x2 - anchrSize, box.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillStyle="red";
  context.fillRect(xCenter - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);}


  for (var i = 0; i < boxes1.length; i++) {
    boxno2= i;
    X3= boxes1[i].x1;
    Y3= boxes1[i].y1;
    F3= boxes1[i].x2;
    G3= boxes1[i].y2;

    }
    no_boxes= boxes1.length;
    const dictboxes = {no_boxes}          //Pass the javascript variables to a dictionary.
    const b4 = JSON.stringify(dictboxes);      // Stringify converts a JavaScript object or value to a JSON string
    $.ajax({
    url:"/boxes2",
    type:"POST",
    contentType: "application/json",
    data: JSON.stringify(b4)});
  

}


function readURL() {
  var form = document.getElementById('form1');
  form.submit();
}


