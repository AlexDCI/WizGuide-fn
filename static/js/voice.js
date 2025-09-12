// voice.js — press & hold + волны + сохранение в БД + языки из основной формы
document.addEventListener("DOMContentLoaded", () => {
  const FASTAPI_URL = "/voice/speech-translate";

  // Языки берём из твоих селектов формы текстового перевода
  const uiSrc = document.getElementById("source_lang");
  const uiTgt = document.getElementById("target_lang");

  // Маппинг отображаемых названий -> коды. Всё, что не распознано:
  // source -> "auto", target -> "en" (чтобы FastAPI не падал).
  const NAME2CODE = {
    "English":"en", "Russian":"ru", "German":"de",
    "Spanish":"es", "French":"fr", "Italian":"it",
    "Portuguese":"pt", "Chinese":"zh", "Chinese-Traditional":"zh-tw",
    "Japanese":"ja", "Korean":"ko", "Arabic":"ar",
    "Hindi":"hi", "Bengali":"bn", "Urdu":"ur",
    "Turkish":"tr", "Dutch":"nl", "Greek":"el",
    "Polish":"pl", "Czech":"cs", "Hungarian":"hu",
    "Swedish":"sv", "Danish":"da", "Finnish":"fi", "Norwegian":"no",
    "Hebrew":"he", "Thai":"th", "Vietnamese":"vi", "Indonesian":"id", "Malay":"ms",
    "Filipino":"fil", "Romanian":"ro", "Slovak":"sk", "Bulgarian":"bg",
    "Croatian":"hr", "Serbian":"sr", "Slovenian":"sl",
    "Lithuanian":"lt", "Latvian":"lv", "Estonian":"et",
    "Georgian":"ka", "Armenian":"hy", "Persian":"fa", "Pashto":"ps",
    "Azerbaijani":"az", "Kazakh":"kk", "Uzbek":"uz", "Tajik":"tg", "Turkmen":"tk", "Kyrgyz":"ky",
    "Mongolian":"mn", "Swahili":"sw", "Zulu":"zu", "Xhosa":"xh", "Afrikaans":"af",
    "Haitian Creole":"ht", "Basque":"eu", "Galician":"gl", "Catalan":"ca",
    "Irish":"ga", "Welsh":"cy", "Scottish Gaelic":"gd", "Maltese":"mt", "Icelandic":"is",
    "Sanskrit":"sa", "Tibetan":"bo", "Maori":"mi", "Samoan":"sm", "Tongan":"to"
  };
  const srcToCode = (name) => {
    if (!name || name === "Выберите язык") return "auto";
    return NAME2CODE[name] ? NAME2CODE[name] : "auto";
  };
  const tgtToCode = (name) => {
    if (!name || name === "Выберите язык") return "en";
    return NAME2CODE[name] ? NAME2CODE[name] : "en";
  };

  async function getJwt(){
    const r = await fetch("/api/token/me");
    if(!r.ok) throw new Error("Не удалось получить JWT (вы вошли?)");
    const j = await r.json();
    return j.access;
  }
  function getCookie(name){
    const m = document.cookie.match('(^|;)\\s*'+name+'\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }
  function escapeHtml(s){
    return (s || "").replace(/[&<>"']/g, ch => (
      { '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[ch]
    ));
  }
  function prependHistory(src, trg){
    const ul = document.querySelector('.chat-history ul.list-group');
    if (!ul) return;
    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.innerHTML = `<strong>${escapeHtml(src||"")}</strong> → <em>${escapeHtml(trg||"")}</em>`;
    ul.prepend(li);
  }

  // Элементы UI голоса
  const micBtn   = document.getElementById("micBtn");
  const statusEl = document.getElementById("v_status");
  const outSrc   = document.getElementById("v_src");
  const outTrg   = document.getElementById("v_trg");
  const canvas   = document.getElementById("micWaves");
  if (!(micBtn && statusEl && outSrc && outTrg && canvas)) return;

  if (!navigator.mediaDevices || !window.MediaRecorder) {
    statusEl.textContent = "⚠️ Браузер не поддерживает запись аудио.";
    micBtn.disabled = true;
    return;
  }

  // === визуализация «волн» ===
  const ctx = canvas.getContext("2d");
  let audioCtx = null, analyser = null, rafId = null;
  function drawWaves(){
    if (!analyser) return;
    const data = new Uint8Array(analyser.fftSize);
    analyser.getByteTimeDomainData(data);
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.save();
    ctx.translate(canvas.width/2, canvas.height/2);
    const baseR = 28, seg = 64;
    for (let i=0;i<seg;i++){
      const v = (data[Math.floor(i*data.length/seg)]-128)/128; // -1..1
      const r = baseR + 20*Math.abs(v);
      const a = (i/seg)*Math.PI*2;
      const x = Math.cos(a)*r, y = Math.sin(a)*r;
      ctx.fillStyle = "rgba(150, 126, 255, 0.22)";
      ctx.beginPath(); ctx.arc(x,y, 2.4 + 1.6*Math.abs(v), 0, Math.PI*2); ctx.fill();
    }
    ctx.restore();
    rafId = requestAnimationFrame(drawWaves);
  }

  // === запись по удержанию кнопки ===
  let stream = null, mediaRecorder = null, chunks = [];
  let isRecording = false;

  function pickMime(){
    if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) return {mime:"audio/webm;codecs=opus", ext:"webm"};
    if (MediaRecorder.isTypeSupported("audio/webm"))            return {mime:"audio/webm",               ext:"webm"};
    if (MediaRecorder.isTypeSupported("audio/mp4"))             return {mime:"audio/mp4",                ext:"mp4"};
    if (MediaRecorder.isTypeSupported("audio/ogg"))             return {mime:"audio/ogg",                ext:"ogg"};
    return {mime:"", ext:"webm"}; // пусть браузер решит
  }

  async function startRecording(){
    if (isRecording) return;
    try{
      stream = await navigator.mediaDevices.getUserMedia({audio:true});

      // волны
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      analyser = audioCtx.createAnalyser();
      analyser.fftSize = 1024;
      audioCtx.createMediaStreamSource(stream).connect(analyser);
      drawWaves();

      // запись
      const {mime, ext} = pickMime();
      mediaRecorder = new MediaRecorder(stream, mime ? {mimeType:mime} : undefined);
      chunks = [];
      mediaRecorder.ondataavailable = e => { if(e.data && e.data.size) chunks.push(e.data); };
      mediaRecorder.onstop = async () => {
        try{ cancelAnimationFrame(rafId); }catch{}
        rafId = null;
        try{ audioCtx && audioCtx.close(); }catch{}
        audioCtx = null; analyser = null; ctx.clearRect(0,0,canvas.width,canvas.height);
        try{ stream && stream.getTracks().forEach(t => t.stop()); }catch{}
        stream = null;

        const blob = new Blob(chunks, {type: mime || "audio/webm"});
        const file = new File([blob], `recording.${ext}`, {type: mime || "audio/webm"});
        await sendToBackend(file);
      };

      mediaRecorder.start();
      isRecording = true;
      statusEl.textContent = "🔴 Запись… удерживайте кнопку";
      outSrc.innerText = "📝 Распознанный текст:\n—";
      outTrg.innerText = "🌍 Перевод:\n—";
    }catch(err){
      statusEl.textContent = "⚠️ Нет доступа к микрофону: " + err.message;
      isRecording = false;
    }
  }

  function stopRecording(){
    if (!isRecording) return;
    try{ mediaRecorder && mediaRecorder.stop(); }catch{}
    isRecording = false;
    statusEl.textContent = "⏳ Обработка…";
  }

  // Удержание: pointer-события (универсально для мыши/тача)
  micBtn.addEventListener("pointerdown", (e) => {
    e.preventDefault();
    micBtn.setPointerCapture(e.pointerId);
    startRecording();
  });
  micBtn.addEventListener("pointerup", (e) => {
    e.preventDefault();
    try{ micBtn.releasePointerCapture(e.pointerId); }catch{}
    stopRecording();
  });
  // На всякий случай — если ушли с кнопки
  document.addEventListener("pointercancel", stopRecording);
  document.addEventListener("pointerleave",  () => {/* игнор */});

  // === отправка в FastAPI + сохранение результата в Django ===
  async function sendToBackend(file){
    try{
      const srcName = uiSrc ? uiSrc.value : "English";
      const tgtName = uiTgt ? uiTgt.value : "Russian";
      const srcCode = srcToCode(srcName);     // 'auto' | 'ru' | 'en' | 'de'
      const tgtCode = tgtToCode(tgtName);     // 'ru' | 'en' | 'de'

      const token = await getJwt();

      const fd = new FormData();
      fd.append("file", file);
      fd.append("source_lang", srcCode);
      fd.append("target_lang", tgtCode);

      const resp = await fetch(FASTAPI_URL, {
        method: "POST",
        body: fd,
        headers: { "Authorization": "Bearer " + token }
      });

      let data;
      try { data = await resp.json(); }
      catch { data = { error: "Некорректный ответ от FastAPI" }; }

      if (!resp.ok || data.error){
        statusEl.textContent = "⚠️ Ошибка FastAPI: " + (data.error || resp.status);
        return;
      }

      statusEl.textContent = "✅ Готово";
      outSrc.innerText = `📝 Распознанный текст:\n${data.source_text || "—"}`;
      outTrg.innerText = `🌍 Перевод:\n${data.translated_text || "—"}`;

      // сохраняем в общую историю (та же модель ChatHistory)
      await fetch("/api/save-speech", {
        method:"POST",
        headers: {
          "Content-Type":"application/json",
          "X-CSRFToken": getCookie('csrftoken')
        },
        body: JSON.stringify({
          source_text: data.source_text,
          translated_text: data.translated_text,
          comment: null
        })
      });

      prependHistory(data.source_text, data.translated_text);

    }catch(err){
      statusEl.textContent = "⚠️ Ошибка: " + err.message;
    }
  }
});
