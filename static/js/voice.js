document.addEventListener("DOMContentLoaded", () => {
  const FASTAPI_URL = "http://127.0.0.1:8001/speech-translate";

  async function getJwt(){
    const r = await fetch("/api/token/me");
    const j = await r.json();
    return j.access;
  }

  const recBtn = document.getElementById('recBtn');
  const stopBtn = document.getElementById('stopBtn');
  const statusEl = document.getElementById('status');
  const recognized = document.getElementById('recognized');
  const translated = document.getElementById('translated');
  const level = document.getElementById('level');
  const srcSel = document.getElementById('voice_source');
  const tgtSel = document.getElementById('voice_target');

  let mediaRecorder, chunks=[], audioContext, analyser, dataArray, rafId;

  recBtn.onclick = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});

    // индикатор громкости
    audioContext = new AudioContext();
    analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);
    dataArray = new Uint8Array(analyser.frequencyBinCount);
    const updateMeter = () => {
      analyser.getByteTimeDomainData(dataArray);
      let sum=0; for (let i=0;i<dataArray.length;i++) sum += Math.abs(dataArray[i]-128);
      const volume = Math.min(100, (sum/dataArray.length)*2);
      level.style.width = volume + "%";
      rafId = requestAnimationFrame(updateMeter);
    }; updateMeter();

    // запись
    mediaRecorder = new MediaRecorder(stream, {mimeType:'audio/webm'});
    chunks = [];
    mediaRecorder.ondataavailable = e => { if(e.data.size) chunks.push(e.data); };
    mediaRecorder.onstop = async () => {
      cancelAnimationFrame(rafId); audioContext.close();
      const blob = new Blob(chunks, {type:'audio/webm'});
      const file = new File([blob], "recording.webm", {type:'audio/webm'});
      await sendFile(file);
    };
    mediaRecorder.start();

    recBtn.disabled = true; stopBtn.disabled = false;
    statusEl.textContent = "🔴 Запись идёт…";
    recognized.textContent = "📝 Распознанный текст:\n—";
    translated.textContent = "🌍 Перевод:\n—";
  };

  stopBtn.onclick = () => {
    mediaRecorder.stop();
    recBtn.disabled = false; stopBtn.disabled = true;
    statusEl.textContent = "⏳ Обработка…";
  };

  async function sendFile(file){
    const token = await getJwt();
    const fd = new FormData();
    fd.append("file", file);
    fd.append("source_lang", srcSel.value);
    fd.append("target_lang", tgtSel.value);

    const resp = await fetch(FASTAPI_URL, {
      method:"POST", body: fd,
      headers: { "Authorization": "Bearer " + token }
    });
    const data = await resp.json();

    statusEl.textContent = data.error ? "⚠️ Ошибка" : "✅ Готово";
    recognized.textContent = data.error ? "Ошибка: "+data.error : "📝 Распознанный текст:\n"+(data.source_text||"—");
    translated.textContent = data.error ? "—" : "🌍 Перевод:\n"+(data.translated_text||"—");

    if(!data.error){
      await fetch("/api/save-speech", {
        method:"POST",
        headers: { "Content-Type":"application/json", "X-CSRFToken": getCookie('csrftoken') },
        body: JSON.stringify({ source_text:data.source_text, translated_text:data.translated_text, comment:null })
      });
    }
  }

  function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }
});
