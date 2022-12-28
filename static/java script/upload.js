let result = document.querySelector(".result"),
result2 = document.querySelector(".result2"),
upload1 = document.querySelector("#file-input1"),
upload2 = document.querySelector("#file-input2");

upload1.addEventListener('change' , (e) => {
console.log(e)
    const reader1 = new FileReader();
reader1.onload = (e) => {
if (e.target){
    //upload first image
    let img = document.createElement("img");
    img.id = "img";
    img.src = e.target.result;
    //clean 1st image
    result.innerHTML = " ";
    //add 1st image 
    result.appendChild(img);
    save.classList.remove("hide");

}
};
//read the  1st img & send it 
img1_send =  e.target.files[0];
reader1.readAsDataURL(img1_send);
var xhr=new XMLHttpRequest();
var fd=new FormData();
fd.append("image1",img1_send, './static/uploadedimg/first_img');
xhr.onreadystatechange = function() {
    if (xhr.status == 200) {
        send_img();
        document.getElementById('User-img').style.display = 'block';
    }
    };
xhr.open("POST","/",true);
xhr.send(fd);
selceted1.classList.add("hide");
selceted2.classList.add("hide");
})
////second image
upload2.addEventListener('change' , (e) => {
    
    console.log(e)
        const reader2 = new FileReader();
    reader2.onload = (e) => {
    if (e.target){
        //upload second image
        let img2 = document.createElement("img");
        img2.id = "img2";
        img2.src = e.target.result;
        //clean 2st image
        result2.innerHTML = " ";
        //add 2st image 
        result2.appendChild(img2);
        save2.classList.remove("hide");
     
    
    }
    };
    //read the  2st img & send it to back
    img2_send =  e.target.files[0];
    reader2.readAsDataURL(img2_send);
    var xhr=new XMLHttpRequest();
    var fd=new FormData();
    fd.append("image2",img2_send, './static/uploadedimg/second_img');
    xhr.onreadystatechange = function() {
		if (xhr.status == 200) {
            send_img();
            document.getElementById('User-img').style.display = 'block';

		}
	};
    xhr.open("POST","/",true);
    xhr.send(fd);
    
    })


