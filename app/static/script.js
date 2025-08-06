const recordBtn = document.getElementById("recordBtn");
const responseAudio = document.getElementById("responseAudio");

let mediaRecorder;
let chunks = [];

recordBtn.onclick = async () => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    chunks = [];

    mediaRecorder.ondataavailable = e => chunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("file", blob, "audio.webm");

      // Transcribe
      const transcribeRes = await fetch("/api/transcribe", {
        method: "POST",
        body: formData
      });
      const { text, language } = await transcribeRes.json();
      console.log("Transcript:", text);

      // Speak
      const speakData = new FormData();
      speakData.append("text", text);
      speakData.append("lang", language);

      const speakRes = await fetch("/api/speak", {
        method: "POST",
        body: speakData
      });
      const { audio_path } = await speakRes.json();

      // Play
      responseAudio.src = audio_path;
      responseAudio.style.display = "block";
      responseAudio.play();
    };

    mediaRecorder.start();
    recordBtn.textContent = "⏹️ Stop Recording";
  } else {
    mediaRecorder.stop();
    recordBtn.textContent = "🎤 Start Recording";
  }
};
