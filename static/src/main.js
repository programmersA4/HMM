/*
 *  Copyright (c) 2015 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree.
 */
'use strict';

// Put variables in global scope to make them available to the browser console.
const constraints = window.constraints = {
  audio: false,
  video: true
};

function stopWebcam () {
  const stopButton = document.querySelector('#stopCamera');
  stopButton.onclick  = function () {
    window.stream.getTracks()[0].stop();
    document.querySelector('#showVideo').disabled = false;
    document.querySelector('#stopCamera').disabled = true;
    document.querySelector('#captureBtn').disabled = true;
    document.querySelector('#container').innerHTML = `<div class="row p-1"><video id="gum-local" autoplay playsinline></video></div>`;
    document.querySelector('#canvas-wrapper').innerHTML = `<canvas></canvas>`; 
  };
}

function sendImg(img_base64){
  var xhr = new XMLHttpRequest();

  const formbody = new FormData();
  formbody.append('img', img_base64);
  formbody.append('challenge', localStorage.getItem('challenge'))

  xhr.open('POST', 'http://localhost:5000/capture_img', true);
  xhr.onload = () => {
      var data = JSON.parse(xhr.responseText);
      console.log(data['success']);
      var bcolor = 'danger'
      if (data['success'] === true) {
        bcolor = 'success'
      }
      localStorage.setItem('img', data['img']);
      document.querySelector('#canvas-wrapper').innerHTML = 
      `<img src="http://localhost:5000/image/${localStorage.getItem('img')}" 
        class="mt-1 border border-5 border-${bcolor} rounded px-0" width="640" height="480"
        >
      </img>`
    };
  xhr.send(formbody)
}

function captureImg(){
  const video = document.querySelector('video');
  document.querySelector('#canvas-wrapper').innerHTML = `<canvas></canvas>`; 
  const canvas = document.querySelector('canvas');
  canvas.width = 640;
  canvas.height = 480;

  const captureButton = document.querySelector('#captureBtn');
  captureButton.onclick = function() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    var img_base64 = canvas.toDataURL('image/jpeg').replace(/^.*,/, '');
    sendImg(img_base64);
  };
}

function handleSuccess(stream) {
  const video = document.querySelector('video');
  const videoTracks = stream.getVideoTracks();
  console.log('Got stream with constraints:', constraints);
  console.log(`Using video device: ${videoTracks[0].label}`);
  window.stream = stream; // make variable available to browser console
  video.srcObject = stream;
  captureImg();
  stopWebcam(stream);
}

function handleError(error) {
  if (error.name === 'ConstraintNotSatisfiedError') {
    const v = constraints.video;
    errorMsg(`The resolution ${v.width.exact}x${v.height.exact} px is not supported by your device.`);
  } else if (error.name === 'PermissionDeniedError') {
    errorMsg('Permissions have not been granted to use your camera and ' +
      'microphone, you need to allow the page access to your devices in ' +
      'order for the demo to work.');
  }
  errorMsg(`getUserMedia error: ${error.name}`, error);
}

function errorMsg(msg, error) {
  const errorElement = document.querySelector('#errorMsg');
  errorElement.innerHTML += `<p>${msg}</p>`;
  if (typeof error !== 'undefined') {
    console.error(error);
  }
}

async function init(e) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    handleSuccess(stream);
    e.target.disabled = true;
    document.querySelector('#captureBtn').disabled = false;
    document.querySelector('#stopCamera').disabled = false;
  } catch (e) {
    handleError(e);
  }
}

document.querySelector('#showVideo').addEventListener('click', e => init(e));
