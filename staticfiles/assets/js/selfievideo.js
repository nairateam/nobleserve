let canvas
let ctx
let webcamStream
let video

const constraints = {
  video: true,
  audio: false
}

const init = function () {
  // obtain canvas context for drawing
  canvas = document.getElementById('myCanvas')
  ctx = canvas.getContext('2d')
}

// get user media and start capturing video streaming
const startWebcam = async function () {
  try {
    if (!webcamStream) {
      webcamStream = await navigator.mediaDevices.getUserMedia(constraints)
      video = document.getElementById('myVideo')
    }

    if (typeof video.srcObject !== 'undefined') {
      video.srcObject = webcamStream
    } else {
      video.src = URL.createObjectURL(webcamStream)
    }

    video.play()
  } catch (err) {
    console.error('error obtaining navigator.mediaDevices.getUserMedia')
    console.error(err.message || err)
    console.error('https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia#Browser_compatibility')
  }
}

const stopWebcam = function () {
  if (video && video.srcObject) {
    const videoTracks = webcamStream.getVideoTracks()
    videoTracks.forEach(track => {
      track.stop()
    })

    if (typeof video.srcObject !== 'undefined') {
      video.srcObject = null
    } else {
      video.src = null
    }

    webcamStream = null
  }
}

// take a snap shot
const takeSnapshot = function () {
  // draw current image from the video onto the canvas
  if (webcamStream) {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
  }
}

const pauseVideo = function () {
  if (video) {
    video.pause()
  }
}

const resumeVideo = function () {
  if (video) {
    video.play()
  }
}

// flip web cam horizontally
const toggleMirror = function () {
  const checked = document.getElementById('mirrorCheckbox').checked
  video.className = checked ? 'mirror' : ''
  canvas.className = checked ? 'mirror' : ''
}

init()
