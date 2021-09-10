const video = document.getElementById('gum-local');
const body = document.querySelector('body');
const canvas = document.querySelector('#canvas');


function showCaptured() {
	// var canvas = document.getElementById('canvas');
	// console.log(canva.getContext)
	var context = canvas.getContext('2d');
	context.drawImage(video, 0, 0, video.clientWidth, video.clientHeight);
	// context.drawImage(video,0,0,640,480);
	var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '');
	captureImg(img_base64);
}

//Captured image data(base64)POST
function captureImg(img_base64) {
    body.appendChild('img', img_base64);
    xhr.open('POST', 'http://localhost:5000/capture_img', true);
    xhr.onload = () => {
        console.log(xhr.responseText)
    };
    xhr.send(body);
}

async function init(){
	var xhr = new XMLHttpRequest();
	showCaptured();
}

if(canvas !== null){
	document.querySelector("#webcamBtn").addEventListener("click", init());
}
