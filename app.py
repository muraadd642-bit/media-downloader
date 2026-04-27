<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSSMurad – Ultra Downloader</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --nb:#00d4ff;--np:#ff2d78;--ng:#00ff9d;--na:#ffaa00;
  --bg:#020817;--bg2:rgba(0,20,50,0.55);--bg3:rgba(0,8,22,0.95);
  --border:rgba(0,212,255,0.28);--border2:rgba(0,212,255,0.5);
  --txt:#e2f4ff;--muted:#7ab3cc;--dark:#3a6a80;
}

html{scroll-behavior:smooth}
body{background:var(--bg);font-family:'Rajdhani',sans-serif;color:var(--txt);min-height:100vh;overflow-x:hidden;cursor:default}

/* ── CANVAS BG ── */
#bg-canvas{position:fixed;inset:0;z-index:0;pointer-events:none}

/* ── SCAN LINE ── */
body::after{content:'';position:fixed;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,transparent 0%,var(--nb) 50%,transparent 100%);animation:hscan 6s linear infinite;opacity:0.4;z-index:999;pointer-events:none}
@keyframes hscan{0%{top:-10px}100%{top:100vh}}

/* ── LAYOUT ── */
.page{position:relative;z-index:1;display:flex;flex-direction:column;min-height:100vh}

/* ── NAV ── */
nav{display:flex;align-items:center;justify-content:space-between;padding:1rem 2.5rem;border-bottom:1px solid var(--border);background:rgba(2,8,23,0.85);backdrop-filter:blur(20px);position:sticky;top:0;z-index:100}
.nav-logo{font-family:'Orbitron',monospace;font-size:1.1rem;font-weight:900;background:linear-gradient(135deg,var(--nb),var(--np));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:2px}
.nav-links{display:flex;gap:1.5rem}
.nav-links a{font-size:0.8rem;color:var(--muted);text-decoration:none;letter-spacing:2px;text-transform:uppercase;font-weight:600;transition:color 0.2s;font-family:'Orbitron',monospace}
.nav-links a:hover{color:var(--nb)}
.nav-badge{background:rgba(0,212,255,0.1);border:1px solid var(--border);border-radius:20px;padding:4px 14px;font-size:0.68rem;font-family:'Orbitron',monospace;color:var(--nb);letter-spacing:2px}

/* ── HERO ── */
.hero{text-align:center;padding:4rem 1rem 3rem;position:relative}
.hero-eyebrow{font-size:0.7rem;letter-spacing:5px;text-transform:uppercase;color:var(--muted);margin-bottom:1rem;font-family:'Orbitron',monospace}
.hero-title{font-family:'Orbitron',monospace;font-size:clamp(2.2rem,7vw,4.5rem);font-weight:900;line-height:1.05;letter-spacing:-1px;margin-bottom:0.5rem}
.hero-title .g1{background:linear-gradient(135deg,var(--nb) 0%,#006fff 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-title .g2{background:linear-gradient(135deg,var(--np) 0%,var(--na) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:1rem;color:var(--muted);letter-spacing:3px;text-transform:uppercase;margin-bottom:2rem}

.motivate{display:inline-block;background:linear-gradient(135deg,rgba(0,212,255,0.08),rgba(255,45,120,0.06));border:1px solid rgba(0,212,255,0.22);border-radius:50px;padding:0.55rem 1.6rem;font-size:0.95rem;font-weight:600;color:var(--nb);letter-spacing:0.4px;max-width:680px;margin:0 auto 2.5rem;animation:fadeup 0.8s ease both}
@keyframes fadeup{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}

.pbadges{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:3rem}
.pb{padding:5px 16px;border-radius:20px;font-size:0.72rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
.pb-yt{background:rgba(255,0,0,0.12);color:#ff5555;border:1px solid rgba(255,0,0,0.3)}
.pb-ig{background:rgba(200,60,255,0.1);color:#cc5fff;border:1px solid rgba(200,60,255,0.3)}
.pb-tt{background:rgba(0,212,255,0.1);color:var(--nb);border:1px solid var(--border)}
.pb-tw{background:rgba(29,161,242,0.1);color:#1da1f2;border:1px solid rgba(29,161,242,0.3)}
.pb-more{background:rgba(0,255,157,0.08);color:var(--ng);border:1px solid rgba(0,255,157,0.3)}

/* ── MAIN CARD ── */
.main-wrap{max-width:820px;margin:0 auto;padding:0 1.5rem 4rem;width:100%}

.glass{background:var(--bg2);border:1px solid var(--border);border-radius:20px;padding:2rem 2.5rem;backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);box-shadow:0 0 60px rgba(0,212,255,0.06),0 20px 60px rgba(0,0,0,0.7),inset 0 1px 0 rgba(255,255,255,0.05);margin-bottom:1.5rem;position:relative;overflow:hidden;animation:fadeup 0.5s ease both}
.glass::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--nb),var(--np),transparent);animation:topscan 4s linear infinite}
@keyframes topscan{0%,100%{opacity:0.3}50%{opacity:1}}

.glass:nth-child(2){animation-delay:0.1s}
.glass:nth-child(3){animation-delay:0.2s}
.glass:nth-child(4){animation-delay:0.3s}

.slabel{font-family:'Orbitron',monospace;font-size:0.6rem;font-weight:700;letter-spacing:3px;color:var(--nb);text-transform:uppercase;margin-bottom:8px;display:flex;align-items:center;gap:6px}
.slabel::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}

.url-wrap{position:relative}
.url-inp{width:100%;background:rgba(0,15,35,0.8);border:1px solid var(--border);border-radius:12px;color:var(--txt);font-family:'Rajdhani',sans-serif;font-size:1rem;padding:0.85rem 1.2rem 0.85rem 3rem;outline:none;transition:border-color 0.3s,box-shadow 0.3s;letter-spacing:0.3px}
.url-inp:focus{border-color:var(--nb);box-shadow:0 0 0 3px rgba(0,212,255,0.12),0 0 20px rgba(0,212,255,0.2)}
.url-inp::placeholder{color:var(--dark)}
.url-icon{position:absolute;left:1rem;top:50%;transform:translateY(-50%);color:var(--muted);font-size:1rem;pointer-events:none}

.divider{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(0,212,255,0.2),transparent);margin:1.5rem 0}

.row2{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}

/* Format radio */
.fmt-group{display:flex;flex-direction:column;gap:8px}
.fmt-opt{display:flex;align-items:center;gap:12px;padding:10px 14px;border-radius:10px;border:1px solid transparent;cursor:pointer;transition:all 0.25s;font-size:0.95rem;font-weight:600;color:var(--txt);user-select:none}
.fmt-opt:hover{background:rgba(0,212,255,0.06);border-color:rgba(0,212,255,0.2)}
.fmt-opt.active{background:rgba(0,212,255,0.1);border-color:rgba(0,212,255,0.4);color:#fff}
.fmt-icon{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0}
.fmt-icon.mp4{background:rgba(0,212,255,0.12);border:1px solid rgba(0,212,255,0.25)}
.fmt-icon.mp3{background:rgba(255,45,120,0.1);border:1px solid rgba(255,45,120,0.25)}
.fmt-meta{font-size:0.75rem;color:var(--muted);font-weight:400;margin-top:1px}

/* Quality */
.q-tabs{display:flex;gap:6px;flex-wrap:wrap}
.q-tab{padding:8px 16px;border-radius:8px;border:1px solid var(--border);background:rgba(0,15,35,0.6);color:var(--muted);font-family:'Orbitron',monospace;font-size:0.7rem;cursor:pointer;transition:all 0.2s;font-weight:700;letter-spacing:1px}
.q-tab:hover{border-color:var(--nb);color:var(--nb)}
.q-tab.active{background:rgba(0,212,255,0.12);border-color:var(--nb);color:#fff;box-shadow:0 0 12px rgba(0,212,255,0.2)}
.q-note{font-size:0.8rem;color:var(--muted);margin-top:12px;padding:8px 12px;background:rgba(255,45,120,0.06);border-radius:8px;border-left:2px solid rgba(255,45,120,0.4)}

/* Robot checkbox */
.robot-wrap{display:flex;align-items:center;gap:14px;background:rgba(0,15,35,0.6);border:1px solid var(--border);border-radius:12px;padding:1rem 1.2rem;cursor:pointer;transition:all 0.2s;user-select:none}
.robot-wrap:hover{background:rgba(0,212,255,0.05);border-color:rgba(0,212,255,0.35)}
.robot-wrap.checked{background:rgba(0,255,157,0.05);border-color:rgba(0,255,157,0.3)}
.cb-visual{width:22px;height:22px;border-radius:5px;border:2px solid var(--dark);flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:all 0.2s;font-size:13px;color:var(--ng)}
.robot-wrap.checked .cb-visual{border-color:var(--ng);background:rgba(0,255,157,0.12)}
.cb-text{flex:1}
.cb-title{font-size:0.95rem;font-weight:600;color:var(--txt)}
.cb-sub{font-size:0.75rem;color:var(--muted);margin-top:2px}
.robot-icon{font-size:1.5rem;flex-shrink:0}
.cb-status{margin-top:8px;font-size:0.82rem;padding:6px 12px;border-radius:6px;display:none}
.cb-status.show{display:block}
.cb-status.ok{background:rgba(0,255,157,0.06);color:var(--ng);border-left:2px solid var(--ng)}
.cb-status.wait{background:rgba(0,212,255,0.06);color:var(--muted);border-left:2px solid var(--border)}

/* Download button */
.dl-btn{width:100%;padding:1rem;border-radius:14px;border:1px solid var(--nb);background:linear-gradient(135deg,rgba(0,60,100,0.8),rgba(0,25,60,0.9));color:var(--nb);font-family:'Orbitron',monospace;font-size:0.9rem;font-weight:700;letter-spacing:3px;cursor:pointer;transition:all 0.3s;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;gap:10px}
.dl-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,212,255,0.08),transparent);opacity:0;transition:opacity 0.3s}
.dl-btn:hover:not(:disabled)::before{opacity:1}
.dl-btn:hover:not(:disabled){box-shadow:0 0 40px rgba(0,212,255,0.35),0 0 80px rgba(0,212,255,0.1);transform:translateY(-3px);color:#fff;border-color:rgba(0,212,255,0.8)}
.dl-btn:active:not(:disabled){transform:translateY(-1px)}
.dl-btn:disabled{opacity:0.3;cursor:not-allowed;border-color:var(--dark)}
.dl-btn.loading{animation:btn-pulse 1.2s ease-in-out infinite}
@keyframes btn-pulse{0%,100%{box-shadow:0 0 20px rgba(0,212,255,0.2)}50%{box-shadow:0 0 50px rgba(0,212,255,0.5)}}
.btn-arrow{font-size:1.2rem;transition:transform 0.3s}
.dl-btn:hover:not(:disabled) .btn-arrow{transform:translateY(3px)}

/* Progress */
.prog-section{margin-top:1.2rem;display:none}
.prog-section.show{display:block}
.prog-stages{display:flex;justify-content:space-between;margin-bottom:8px;gap:4px}
.stage-dot{flex:1;height:3px;border-radius:3px;background:rgba(0,212,255,0.1);transition:background 0.4s,box-shadow 0.4s}
.stage-dot.done{background:var(--nb);box-shadow:0 0 8px rgba(0,212,255,0.6)}
.stage-dot.active{background:var(--nb);animation:dot-pulse 0.8s ease-in-out infinite}
@keyframes dot-pulse{0%,100%{opacity:0.6}50%{opacity:1;box-shadow:0 0 12px rgba(0,212,255,0.8)}}
.prog-bar-bg{background:rgba(0,212,255,0.06);border-radius:8px;height:8px;overflow:hidden;border:1px solid rgba(0,212,255,0.1)}
.prog-bar{height:100%;background:linear-gradient(90deg,var(--nb),var(--ng));border-radius:8px;width:0%;transition:width 0.5s cubic-bezier(0.4,0,0.2,1);box-shadow:0 0 10px rgba(0,212,255,0.5)}
.prog-label{display:flex;justify-content:space-between;align-items:center;margin-top:6px}
.prog-msg{font-size:0.78rem;color:var(--muted);font-family:'Orbitron',monospace;letter-spacing:1px}
.prog-pct{font-size:0.78rem;color:var(--nb);font-family:'Orbitron',monospace;font-weight:700}

/* Status */
.status-box{border-radius:10px;padding:1rem 1.2rem;margin-top:1rem;display:none;font-size:0.92rem;font-weight:600;line-height:1.5}
.status-box.show{display:block}
.status-box.success{background:rgba(0,255,157,0.07);border:1px solid rgba(0,255,157,0.3);color:var(--ng)}
.status-box.error{background:rgba(255,45,120,0.07);border:1px solid rgba(255,45,120,0.3);color:#ff7aab}
.status-box.info{background:rgba(0,212,255,0.07);border:1px solid var(--border);color:var(--nb)}

/* ── STATS ROW ── */
.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:1.5rem}
.stat-card{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:1.2rem;text-align:center;position:relative;overflow:hidden;animation:fadeup 0.5s ease both}
.stat-card::after{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:var(--accent,var(--nb));opacity:0.4}
.stat-card:nth-child(1){--accent:var(--nb)}
.stat-card:nth-child(2){--accent:var(--np);animation-delay:0.1s}
.stat-card:nth-child(3){--accent:var(--ng);animation-delay:0.2s}
.stat-card:nth-child(4){--accent:var(--na);animation-delay:0.3s}
.stat-num{font-family:'Orbitron',monospace;font-size:1.6rem;font-weight:900;color:#fff;line-height:1}
.stat-label{font-size:0.68rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;margin-top:4px}

/* ── COUNTDOWN ── */
.countdown-card{background:linear-gradient(135deg,rgba(0,20,50,0.7),rgba(0,8,22,0.9));border:1px solid var(--border);border-radius:20px;padding:2rem;text-align:center;margin-bottom:1.5rem;position:relative;overflow:hidden;animation:fadeup 0.5s ease both;animation-delay:0.4s}
.countdown-card::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle at center,rgba(0,212,255,0.04) 0%,transparent 60%);animation:rotate-glow 10s linear infinite}
@keyframes rotate-glow{0%{transform:rotate(0deg)}100%{transform:rotate(360deg)}}
.cd-title{font-family:'Orbitron',monospace;font-size:0.65rem;letter-spacing:4px;color:var(--nb);text-transform:uppercase;margin-bottom:1.2rem}
.cd-grid{display:flex;justify-content:center;gap:1.5rem;flex-wrap:wrap}
.cd-cell{display:flex;flex-direction:column;align-items:center;background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.15);border-radius:12px;padding:0.8rem 1.2rem;min-width:80px}
.cd-num{font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:900;color:#fff;line-height:1}
.cd-unit{font-size:0.58rem;letter-spacing:3px;color:var(--muted);text-transform:uppercase;margin-top:4px}
.cd-target{font-size:0.78rem;color:var(--muted);margin-top:1rem;letter-spacing:1px}

/* ── FEATURES ── */
.features{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:1.5rem}
.feat{background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:1.2rem;position:relative;overflow:hidden;transition:all 0.3s;animation:fadeup 0.5s ease both}
.feat:hover{border-color:var(--nb);transform:translateY(-4px);box-shadow:0 10px 40px rgba(0,212,255,0.1)}
.feat:nth-child(2){animation-delay:0.1s}
.feat:nth-child(3){animation-delay:0.2s}
.feat-icon{font-size:1.5rem;margin-bottom:0.6rem}
.feat-title{font-family:'Orbitron',monospace;font-size:0.72rem;font-weight:700;color:var(--nb);letter-spacing:2px;text-transform:uppercase;margin-bottom:6px}
.feat-desc{font-size:0.82rem;color:var(--muted);line-height:1.5}

/* ── FOOTER ── */
footer{border-top:1px solid var(--border);padding:2rem;text-align:center;background:rgba(2,8,23,0.8);margin-top:auto}
.footer-logo{font-family:'Orbitron',monospace;font-size:1rem;font-weight:900;background:linear-gradient(135deg,var(--nb),var(--np));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:0.5rem}
.footer-txt{font-size:0.75rem;color:var(--dark);letter-spacing:1px}
.footer-links{display:flex;justify-content:center;gap:1.5rem;margin:1rem 0}
.footer-links a{font-size:0.72rem;color:var(--muted);text-decoration:none;letter-spacing:2px;text-transform:uppercase;transition:color 0.2s}
.footer-links a:hover{color:var(--nb)}

/* ── TOAST ── */
#toast{position:fixed;bottom:2rem;right:2rem;background:rgba(0,20,50,0.95);border:1px solid var(--nb);border-radius:12px;padding:0.8rem 1.5rem;font-size:0.85rem;color:var(--nb);font-family:'Orbitron',monospace;letter-spacing:1px;transform:translateY(100px);opacity:0;transition:all 0.4s cubic-bezier(0.4,0,0.2,1);z-index:1000;box-shadow:0 0 30px rgba(0,212,255,0.3)}
#toast.show{transform:translateY(0);opacity:1}

/* ── CUSTOM SCROLLBAR ── */
::-webkit-scrollbar{width:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.3);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:rgba(0,212,255,0.5)}

/* ── RESPONSIVE ── */
@media(max-width:660px){
  nav{padding:0.8rem 1.2rem}
  .nav-links{display:none}
  .hero{padding:2.5rem 1rem 2rem}
  .glass{padding:1.3rem 1.2rem}
  .row2{grid-template-columns:1fr}
  .stats-row{grid-template-columns:repeat(2,1fr)}
  .features{grid-template-columns:1fr}
  .cd-grid{gap:0.75rem}
  .cd-num{font-size:1.6rem}
}
</style>
</head>
<body>

<canvas id="bg-canvas"></canvas>

<div class="page">

<!-- NAV -->
<nav>
  <div class="nav-logo">⚡ SSSMurad</div>
  <div class="nav-links">
    <a href="#downloader">Yüklə</a>
    <a href="#features">Xüsusiyyətlər</a>
    <a href="#countdown">İmtahan</a>
  </div>
  <div class="nav-badge">Pro Edition</div>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-eyebrow">⚡ Anti-Block · Ultra-Fast · Free</div>
  <h1 class="hero-title">
    <span class="g1">SSS</span><span class="g2">Murad</span><br>
    <span style="font-size:0.55em;letter-spacing:4px;opacity:0.85">Ultra Downloader</span>
  </h1>
  <div class="hero-sub">Pro Edition · Anti-Block Engine v4.0</div>
  <div class="motivate" id="mot"></div>
  <div class="pbadges">
    <span class="pb pb-yt">▶ YouTube</span>
    <span class="pb pb-ig">◉ Instagram</span>
    <span class="pb pb-tt">◈ TikTok</span>
    <span class="pb pb-tw">✦ Twitter/X</span>
    <span class="pb pb-more">+ 1000 Sayt</span>
  </div>
</section>

<!-- STATS -->
<div class="main-wrap">
<div class="stats-row">
  <div class="stat-card">
    <div class="stat-num" id="s-sites">1000+</div>
    <div class="stat-label">Dəstəklənən Sayt</div>
  </div>
  <div class="stat-card">
    <div class="stat-num">4K</div>
    <div class="stat-label">Max Keyfiyyət</div>
  </div>
  <div class="stat-card">
    <div class="stat-num">0₼</div>
    <div class="stat-label">Qiymət</div>
  </div>
  <div class="stat-card">
    <div class="stat-num">8</div>
    <div class="stat-label">User-Agent Rotasiya</div>
  </div>
</div>

<!-- DOWNLOADER -->
<div id="downloader">

<!-- URL Card -->
<div class="glass">
  <div class="slabel">🔗 Media URL</div>
  <div class="url-wrap">
    <span class="url-icon">🔗</span>
    <input type="text" class="url-inp" id="url" placeholder="https://youtube.com/watch?v=...  ·  Instagram  ·  TikTok  ·  Twitter/X" autocomplete="off" spellcheck="false">
  </div>
</div>

<!-- Format + Quality -->
<div class="glass">
  <div class="row2">
    <div>
      <div class="slabel">📦 Format Seç</div>
      <div class="fmt-group">
        <div class="fmt-opt active" id="mp4-opt" onclick="selectFmt('mp4')">
          <div class="fmt-icon mp4">🎬</div>
          <div>
            <div>MP4 · Video</div>
            <div class="fmt-meta">H.264 · 4K/1080p/720p/480p</div>
          </div>
        </div>
        <div class="fmt-opt" id="mp3-opt" onclick="selectFmt('mp3')">
          <div class="fmt-icon mp3">🎵</div>
          <div>
            <div>MP3 · Musiqi</div>
            <div class="fmt-meta">AAC → MP3 · 320/192/128 kbps</div>
          </div>
        </div>
      </div>
    </div>
    <div>
      <div class="slabel">🎚️ Keyfiyyət</div>
      <div id="qual-video">
        <div class="q-tabs" id="q-tabs">
          <div class="q-tab active" onclick="selectQ(this,'2160p')">4K</div>
          <div class="q-tab" onclick="selectQ(this,'1080p')">1080p</div>
          <div class="q-tab" onclick="selectQ(this,'720p')">720p</div>
          <div class="q-tab" onclick="selectQ(this,'480p')">480p</div>
        </div>
        <div class="q-note" id="q-desc" style="margin-top:12px;font-size:0.78rem;color:var(--muted)">4K Ultra HD · MP4 · H.264+AAC</div>
      </div>
      <div id="qual-audio" style="display:none">
        <div class="q-tabs" id="q-tabs-audio">
          <div class="q-tab active" onclick="selectQA(this,'320kbps')">320k</div>
          <div class="q-tab" onclick="selectQA(this,'192kbps')">192k</div>
          <div class="q-tab" onclick="selectQA(this,'128kbps')">128k</div>
        </div>
        <div class="q-note" style="margin-top:12px;font-size:0.78rem;color:var(--muted)">MP3 · Stereo · Yüksək keyfiyyət</div>
      </div>
    </div>
  </div>
</div>

<!-- Robot Check -->
<div class="glass">
  <div class="slabel">🔐 Təhlükəsizlik Yoxlaması</div>
  <div class="robot-wrap" id="robot-wrap" onclick="toggleCb()">
    <div class="cb-visual" id="cb-visual"></div>
    <div class="cb-text">
      <div class="cb-title">Mən robot deyiləm</div>
      <div class="cb-sub">Bu yükləməni şüurlu şəkildə həyata keçirirəm · Yalnız icazəli məzmun</div>
    </div>
    <div class="robot-icon">🤖</div>
  </div>
  <div class="cb-status wait show" id="cb-status">☐ Zəhmət olmasa yuxarıdakı qutuyu işarələyin</div>
</div>

<!-- Download -->
<div class="glass">
  <button class="dl-btn" id="dl-btn" onclick="startDownload()" disabled>
    <span>⬇</span>
    <span id="btn-txt">YÜKLƏ</span>
    <span class="btn-arrow">↓</span>
  </button>

  <div class="prog-section" id="prog-section">
    <div style="height:12px"></div>
    <div class="prog-stages" id="prog-stages">
      <div class="stage-dot" id="sd0"></div>
      <div class="stage-dot" id="sd1"></div>
      <div class="stage-dot" id="sd2"></div>
      <div class="stage-dot" id="sd3"></div>
      <div class="stage-dot" id="sd4"></div>
      <div class="stage-dot" id="sd5"></div>
    </div>
    <div class="prog-bar-bg"><div class="prog-bar" id="prog-bar"></div></div>
    <div class="prog-label">
      <span class="prog-msg" id="prog-msg">Hazırlanır...</span>
      <span class="prog-pct" id="prog-pct">0%</span>
    </div>
  </div>

  <div class="status-box" id="status-box"></div>
</div>

</div><!-- /downloader -->

<!-- FEATURES -->
<div id="features" class="features">
  <div class="feat">
    <div class="feat-icon">🛡️</div>
    <div class="feat-title">Anti-Block</div>
    <div class="feat-desc">8 fərqli User-Agent rotasiyası. Instagram, TikTok bloklarını avtomatik keçir.</div>
  </div>
  <div class="feat">
    <div class="feat-icon">⚡</div>
    <div class="feat-title">Ultra Sürət</div>
    <div class="feat-desc">Çoxlu thread ilə paralel yükləmə. Fragment retry sistemi ilə kəsilmə yoxdur.</div>
  </div>
  <div class="feat">
    <div class="feat-icon">🔒</div>
    <div class="feat-title">Məxfilik</div>
    <div class="feat-desc">Yüklənmiş fayllar serverdən avtomatik silinir. Heç bir məlumat saxlanılmır.</div>
  </div>
</div>

<!-- COUNTDOWN -->
<div id="countdown" class="countdown-card">
  <div class="cd-title">🎯 İmtahan Geri Sayımı — Hədəf: 7 İyun 2026</div>
  <div class="cd-grid" id="cd-grid"></div>
  <div class="cd-target">Hər gün öyrən · Hər sual bir addım · Zirvə sənin yerindir 🦅</div>
</div>

</div><!-- /main-wrap -->

<!-- FOOTER -->
<footer>
  <div class="footer-logo">⚡ SSSMurad Ultra Downloader</div>
  <div class="footer-links">
    <a href="#">Haqqımızda</a>
    <a href="#">Gizlilik</a>
    <a href="#">API</a>
    <a href="#">Əlaqə</a>
  </div>
  <div class="footer-txt">Pro Edition · Powered by yt-dlp · Anti-Block Engine v4.0 · © 2025 SSSMurad</div>
  <div class="footer-txt" style="margin-top:4px">Yalnız icazəli məzmun üçün istifadə edin · For authorized content only</div>
</footer>

</div><!-- /page -->

<div id="toast"></div>

<script>
// ── PARTICLE CANVAS ──────────────────────────────────────────────────────
const canvas=document.getElementById('bg-canvas');
const ctx=canvas.getContext('2d');
let W,H,particles=[];
function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight}
resize();window.addEventListener('resize',resize);
function mkParticle(){return{x:Math.random()*W,y:Math.random()*H,r:Math.random()*1.2+0.2,vx:(Math.random()-0.5)*0.3,vy:(Math.random()-0.5)*0.3,a:Math.random()*0.5+0.1,hue:Math.random()>0.7?320:195}}
for(let i=0;i<90;i++)particles.push(mkParticle());
function drawCanvas(){
  ctx.clearRect(0,0,W,H);
  // grid
  ctx.strokeStyle='rgba(0,212,255,0.03)';ctx.lineWidth=1;
  const gs=60;
  for(let x=0;x<W;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke()}
  for(let y=0;y<H;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke()}
  // radial glows
  const g1=ctx.createRadialGradient(W*0.2,H*0.4,0,W*0.2,H*0.4,W*0.4);
  g1.addColorStop(0,'rgba(0,100,200,0.04)');g1.addColorStop(1,'transparent');
  ctx.fillStyle=g1;ctx.fillRect(0,0,W,H);
  const g2=ctx.createRadialGradient(W*0.8,H*0.3,0,W*0.8,H*0.3,W*0.35);
  g2.addColorStop(0,'rgba(255,45,120,0.03)');g2.addColorStop(1,'transparent');
  ctx.fillStyle=g2;ctx.fillRect(0,0,W,H);
  // particles
  particles.forEach(p=>{
    p.x+=p.vx;p.y+=p.vy;
    if(p.x<0||p.x>W)p.vx*=-1;
    if(p.y<0||p.y>H)p.vy*=-1;
    ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=`hsla(${p.hue},100%,70%,${p.a})`;ctx.fill();
  });
  // connections
  for(let i=0;i<particles.length;i++){
    for(let j=i+1;j<particles.length;j++){
      const dx=particles[i].x-particles[j].x,dy=particles[i].y-particles[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<110){
        ctx.beginPath();ctx.moveTo(particles[i].x,particles[i].y);ctx.lineTo(particles[j].x,particles[j].y);
        ctx.strokeStyle=`rgba(0,212,255,${0.06*(1-d/110)})`;ctx.lineWidth=0.5;ctx.stroke();
      }
    }
  }
  requestAnimationFrame(drawCanvas);
}
drawCanvas();

// ── MOTIVATIONS ──────────────────────────────────────────────────────────
const MOTS=["⚡ Hər sınaq sənin gizli gücünü ortaya çıxarır. Bu gün bir addım at!","🔥 Uğur heç vaxt təsadüf deyil — o, planın nəticəsidir.","🚀 İmtahan sonu deyil, yeni başlanğıcın qapısıdır.","💡 Bilik silah, səbr isə qalxandır. İkisini də siyir!","🎯 Hər sual bir imkandır. Qaçma, çöz!","🌊 Dalğa nə qədər böyük olursa olsun, sən daha güclüsün.","🏆 Şampionlar yorulmur — yalnız zəiflər əvvəlcədən təslim olur.","🌟 Bu an öyrəndiklərin sabahın silahları olacaq.","💪 Sınaq sənə layiq deyil — SƏN SINAĞA LAYİQSƏN!","🦅 Yüksəl, çünki zirvə sənin yerindir."];
document.getElementById('mot').textContent=MOTS[Math.floor(Math.random()*MOTS.length)];

// ── COUNTDOWN ────────────────────────────────────────────────────────────
function updateCD(){
  const target=new Date('2026-06-07T00:00:00');
  const now=new Date();
  const diff=Math.max(0,target-now);
  const days=Math.floor(diff/(1000*60*60*24));
  const hours=Math.floor((diff%(1000*60*60*24))/(1000*60*60));
  const mins=Math.floor((diff%(1000*60*60))/(1000*60));
  const secs=Math.floor((diff%(1000*60))/1000);
  document.getElementById('cd-grid').innerHTML=
    `<div class="cd-cell"><div class="cd-num">${days}</div><div class="cd-unit">Gün</div></div>`+
    `<div class="cd-cell"><div class="cd-num">${String(hours).padStart(2,'0')}</div><div class="cd-unit">Saat</div></div>`+
    `<div class="cd-cell"><div class="cd-num">${String(mins).padStart(2,'0')}</div><div class="cd-unit">Dəqiqə</div></div>`+
    `<div class="cd-cell"><div class="cd-num" style="color:var(--np)">${String(secs).padStart(2,'0')}</div><div class="cd-unit">Saniyə</div></div>`;
}
updateCD();setInterval(updateCD,1000);

// ── FORMAT SELECT ─────────────────────────────────────────────────────────
let fmt='mp4',quality='2160p',qAudio='320kbps';
const qDesc={'2160p':'4K Ultra HD · MP4 · H.264+AAC','1080p':'Full HD · MP4 · H.264+AAC','720p':'HD Ready · MP4 · H.264+AAC','480p':'SD · MP4 · Yüngül fayl'};
function selectFmt(f){
  fmt=f;
  document.getElementById('mp4-opt').classList.toggle('active',f==='mp4');
  document.getElementById('mp3-opt').classList.toggle('active',f==='mp3');
  document.getElementById('qual-video').style.display=f==='mp4'?'block':'none';
  document.getElementById('qual-audio').style.display=f==='mp3'?'block':'none';
}
function selectQ(el,q){
  quality=q;
  document.querySelectorAll('#q-tabs .q-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('q-desc').textContent=qDesc[q]||q;
}
function selectQA(el,q){
  qAudio=q;
  document.querySelectorAll('#q-tabs-audio .q-tab').forEach(t=>t.classList.remove('active'));
  el.classList.add('active');
}

// ── CHECKBOX ─────────────────────────────────────────────────────────────
let cbChecked=false;
function toggleCb(){
  cbChecked=!cbChecked;
  const wrap=document.getElementById('robot-wrap');
  const box=document.getElementById('cb-visual');
  const st=document.getElementById('cb-status');
  wrap.classList.toggle('checked',cbChecked);
  box.textContent=cbChecked?'✓':'';
  box.style.borderColor=cbChecked?'var(--ng)':'var(--dark)';
  st.className='cb-status show '+(cbChecked?'ok':'wait');
  st.textContent=cbChecked?'🟢 Təsdiqləndi — sistem hazır, yükləmə başlaya bilər.':'☐ Zəhmət olmasa yuxarıdakı qutuyu işarələyin';
  updateBtn();
}
document.getElementById('url').addEventListener('input',updateBtn);
function updateBtn(){
  const has=document.getElementById('url').value.trim().length>0;
  document.getElementById('dl-btn').disabled=!(has&&cbChecked);
}

// ── DOWNLOAD SIM ──────────────────────────────────────────────────────────
const STAGES=[
  {pct:8, msg:'🌐 Serverə bağlanılır...'},
  {pct:22,msg:'🔍 URL analiz edilir...'},
  {pct:40,msg:'🛡️ Anti-block aktiv edildi...'},
  {pct:58,msg:'📡 Media metadata çıxarılır...'},
  {pct:75,msg:'⬇ Fayl yüklənir...'},
  {pct:90,msg:'🔄 Format çevrilir...'},
  {pct:100,msg:'✅ Tamamlandı!'},
];
function toast(msg){
  const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),3000);
}
function startDownload(){
  const url=document.getElementById('url').value.trim();
  if(!url||!cbChecked)return;
  const btn=document.getElementById('dl-btn');
  const btxt=document.getElementById('btn-txt');
  const prog=document.getElementById('prog-section');
  const bar=document.getElementById('prog-bar');
  const msg=document.getElementById('prog-msg');
  const pct=document.getElementById('prog-pct');
  const sbox=document.getElementById('status-box');

  btn.disabled=true;btn.classList.add('loading');btxt.textContent='İŞLƏNİR...';
  prog.className='prog-section show';
  sbox.className='status-box';
  bar.style.width='0%';
  // reset dots
  for(let i=0;i<6;i++){const d=document.getElementById('sd'+i);d.className='stage-dot'}

  let si=0;
  const iv=setInterval(()=>{
    if(si>=STAGES.length){clearInterval(iv);return}
    const s=STAGES[si];
    bar.style.width=s.pct+'%';
    msg.textContent=s.msg;
    pct.textContent=s.pct+'%';
    // update dots
    for(let i=0;i<6;i++){
      const d=document.getElementById('sd'+i);
      if(i<si)d.className='stage-dot done';
      else if(i===si)d.className='stage-dot active';
      else d.className='stage-dot';
    }
    si++;
    if(si===STAGES.length){
      clearInterval(iv);
      setTimeout(()=>{
        btn.classList.remove('loading');
        btn.disabled=false;
        btxt.textContent='YÜKLƏ';
        sbox.className='status-box info show';
        sbox.innerHTML='ℹ️ <b>Demo rejim:</b> Həqiqi yükləmə üçün <code style="color:var(--ng);background:rgba(0,255,157,0.08);padding:2px 6px;border-radius:4px">streamlit run app.py</code> əmrini işlət';
        toast('✅ Demo tamamlandı!');
      },700);
    }
  },500);
}
</script>
</body>
</html>
