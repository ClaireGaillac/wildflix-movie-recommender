"""
Wildflix — Bandeau hero cinématographique pour Streamlit
=========================================================
Une caméra (construite en CSS pur) projette un faisceau lumineux doré qui révèle le titre WILDFLIX lettre par
lettre. 100 % CSS, aucune dépendance JavaScript, robuste dans Streamlit.

Utilisation dans un autre fichier :
    from bandeau import afficher_bandeau
    afficher_bandeau()
"""

import streamlit as st

# --- Le bandeau hero Wildflix ---
WILDFLIX_HERO = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@300;400;500&display=swap');

  /* ======================  WILDFLIX HERO  ====================== */
  .wf-hero{
    --gold:#ffce7a;
    position:relative;
    width:100%;
    height:420px;
    overflow:hidden;
    background:
      radial-gradient(120% 140% at 12% 50%, #1c140c 0%, #100b07 38%, #070504 78%, #050302 100%);
    font-family:'Oswald',sans-serif;
    border-radius:14px;
    isolation:isolate;
  }

  /* grain de film + vignette */
  .wf-hero::after{
    content:"";position:absolute;inset:0;pointer-events:none;z-index:7;
    background:radial-gradient(130% 120% at 50% 50%, transparent 55%, rgba(0,0,0,.55) 100%);
    mix-blend-mode:multiply;
  }
  .wf-grain{
    position:absolute;inset:-50%;z-index:6;pointer-events:none;opacity:.05;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    animation:wf-grain 1.2s steps(3) infinite;
  }
  @keyframes wf-grain{0%{transform:translate(0,0)}50%{transform:translate(-4%,3%)}100%{transform:translate(2%,-2%)}}

  /* ----------  FAISCEAU LUMINEUX (cône objectif -> titre)  ---------- */
  .wf-beam{
    position:absolute;left:142px;top:50%;
    width:78%;height:300px;
    transform:translateY(-50%) scaleX(0);
    transform-origin:left center;z-index:2;
    clip-path:polygon(0% 44%, 0% 56%, 100% 100%, 100% 0%);
    background:linear-gradient(90deg,
        rgba(255,214,140,.55) 0%, rgba(255,210,130,.18) 35%,
        rgba(255,205,120,.07) 70%, rgba(255,205,120,0) 100%);
    filter:blur(2px);opacity:0;
    animation:wf-beam-grow 1.1s .35s cubic-bezier(.2,.8,.25,1) forwards,
              wf-flicker 4.5s 1.5s ease-in-out infinite;
  }
  @keyframes wf-beam-grow{to{transform:translateY(-50%) scaleX(1);opacity:1}}
  @keyframes wf-flicker{
    0%,100%{filter:blur(2px) brightness(1)}
    42%{filter:blur(2px) brightness(1.08)}44%{filter:blur(2px) brightness(.82)}
    46%{filter:blur(2px) brightness(1.12)}48%{filter:blur(2px) brightness(.95)}
    70%{filter:blur(2px) brightness(1.05)}
  }
  .wf-beam-core{
    position:absolute;left:150px;top:50%;width:72%;height:3px;
    transform:translateY(-50%) scaleX(0);transform-origin:left center;z-index:3;
    background:linear-gradient(90deg, rgba(255,235,190,.9), rgba(255,220,150,0));
    filter:blur(1px);animation:wf-core 1s .4s ease-out forwards;
  }
  @keyframes wf-core{to{transform:translateY(-50%) scaleX(1)}}

  /* poussières flottant dans le faisceau */
  .wf-dust{position:absolute;inset:0;z-index:4;pointer-events:none}
  .wf-dust span{
    position:absolute;border-radius:50%;
    background:radial-gradient(circle, rgba(255,235,200,.9), rgba(255,235,200,0));
    opacity:0;animation:wf-float linear infinite;
  }
  @keyframes wf-float{
    0%{opacity:0;transform:translate(0,0)}15%{opacity:.8}
    85%{opacity:.5}100%{opacity:0;transform:translate(40px,-26px)}
  }

  /* ----------  CAMÉRA (formes CSS pures)  ---------- */
  .wf-camera{
    position:absolute;left:42px;top:50%;
    transform:translateY(-50%) translateX(-40px);z-index:5;opacity:0;
    animation:wf-cam-in 1s .1s cubic-bezier(.2,.8,.25,1) forwards;
    filter:drop-shadow(0 10px 24px rgba(0,0,0,.6));
  }
  @keyframes wf-cam-in{to{opacity:1;transform:translateY(-50%) translateX(0)}}
  .wf-cam-body{
    position:relative;width:108px;height:74px;border-radius:9px;
    background:linear-gradient(155deg,#3a3128,#1d1813 70%);
    border:1px solid rgba(255,206,122,.22);
  }
  .wf-reel{
    position:absolute;top:-30px;width:46px;height:46px;border-radius:50%;
    background:radial-gradient(circle at 50% 40%,#2a241d,#15110d);
    border:2px solid #4a3f31;box-shadow:inset 0 0 0 6px rgba(0,0,0,.35);
    animation:wf-spin 6s linear infinite;
  }
  .wf-reel.l{left:8px} .wf-reel.r{left:54px;animation-duration:5s}
  .wf-reel::before,.wf-reel::after{
    content:"";position:absolute;inset:0;margin:auto;
    width:7px;height:7px;border-radius:50%;background:#6b5b46;
  }
  .wf-reel::after{width:26px;height:2px;border-radius:2px;background:rgba(140,120,90,.5)}
  @keyframes wf-spin{to{transform:rotate(360deg)}}
  .wf-lens-housing{
    position:absolute;right:-26px;top:50%;transform:translateY(-50%);
    width:34px;height:46px;border-radius:6px;
    background:linear-gradient(90deg,#2a241d,#3a3128);
    border:1px solid rgba(255,206,122,.25);
  }
  .wf-lens{
    position:absolute;right:-40px;top:50%;transform:translateY(-50%);
    width:30px;height:30px;border-radius:50%;
    background:radial-gradient(circle at 50% 50%, #fff6e2 0%, #ffce7a 30%, #8a6a3a 70%, #2a2017 100%);
    box-shadow:0 0 18px 5px rgba(255,206,122,.65), 0 0 42px 12px rgba(255,200,110,.3);
    animation:wf-lens-pulse 3.5s ease-in-out infinite;
  }
  @keyframes wf-lens-pulse{
    0%,100%{box-shadow:0 0 18px 5px rgba(255,206,122,.6),0 0 40px 12px rgba(255,200,110,.28)}
    50%{box-shadow:0 0 26px 7px rgba(255,214,140,.85),0 0 60px 18px rgba(255,200,110,.4)}
  }

  /* ----------  TITRE  ---------- */
  .wf-stage{position:absolute;z-index:5;right:7%;top:50%;transform:translateY(-50%);text-align:right}
  .wf-kicker{
    font-family:'Oswald',sans-serif;font-weight:300;letter-spacing:.62em;
    text-transform:uppercase;font-size:13px;color:rgba(255,222,180,.72);
    margin:0 4px 10px 0;opacity:0;animation:wf-fade 1s 1.5s forwards;
  }
  .wf-title{
    font-family:'Bebas Neue',sans-serif;font-size:118px;line-height:.86;margin:0;
    display:flex;justify-content:flex-end;letter-spacing:.02em;flex-wrap:nowrap;
  }
  .wf-title span{
    display:inline-block;
    background:linear-gradient(180deg,#fff8ec 0%,#ffd98f 48%,#e8a445 100%);
    -webkit-background-clip:text;background-clip:text;color:transparent;
    filter:drop-shadow(0 2px 1px rgba(0,0,0,.5));
    opacity:0;transform:translateY(14px) scale(.92);
    animation:wf-letter .6s forwards, wf-glow 3.5s ease-in-out infinite;
  }
  .wf-title span:nth-child(1){animation-delay:.65s,2s}
  .wf-title span:nth-child(2){animation-delay:.74s,2.1s}
  .wf-title span:nth-child(3){animation-delay:.83s,2.2s}
  .wf-title span:nth-child(4){animation-delay:.92s,2.3s}
  .wf-title span:nth-child(5){animation-delay:1.01s,2.4s}
  .wf-title span:nth-child(6){animation-delay:1.10s,2.5s}
  .wf-title span:nth-child(7){animation-delay:1.19s,2.6s}
  .wf-title span:nth-child(8){animation-delay:1.28s,2.7s}
  @keyframes wf-letter{to{opacity:1;transform:translateY(0) scale(1)}}
  @keyframes wf-glow{
    0%,100%{filter:drop-shadow(0 2px 1px rgba(0,0,0,.5)) drop-shadow(0 0 14px rgba(255,190,110,.25))}
    50%{filter:drop-shadow(0 2px 1px rgba(0,0,0,.5)) drop-shadow(0 0 26px rgba(255,200,120,.55))}
  }
  @keyframes wf-fade{to{opacity:1}}
  .wf-underline{
    height:2px;width:0;margin:14px 4px 0 auto;
    background:linear-gradient(90deg,rgba(255,206,122,0),#ffce7a);
    box-shadow:0 0 12px rgba(255,206,122,.6);
    animation:wf-line 1s 1.7s cubic-bezier(.2,.8,.25,1) forwards;
  }
  @keyframes wf-line{to{width:340px}}

  @media (max-width:760px){
    .wf-title{font-size:62px}
    .wf-camera{left:18px;transform:translateY(-50%) scale(.8)}
    .wf-stage{right:5%}
    .wf-beam{left:90px}
  }
</style>

<div class="wf-hero">
  <div class="wf-grain"></div>

  <div class="wf-beam"></div>
  <div class="wf-beam-core"></div>
  <div class="wf-dust">
    <span style="left:240px;top:46%;width:5px;height:5px;animation-duration:5s;animation-delay:1.6s"></span>
    <span style="left:340px;top:54%;width:3px;height:3px;animation-duration:6.5s;animation-delay:2.1s"></span>
    <span style="left:430px;top:40%;width:4px;height:4px;animation-duration:5.5s;animation-delay:1.9s"></span>
    <span style="left:520px;top:60%;width:3px;height:3px;animation-duration:7s;animation-delay:2.4s"></span>
    <span style="left:300px;top:58%;width:4px;height:4px;animation-duration:6s;animation-delay:3s"></span>
    <span style="left:610px;top:48%;width:3px;height:3px;animation-duration:6.8s;animation-delay:2.7s"></span>
    <span style="left:200px;top:52%;width:4px;height:4px;animation-duration:5.2s;animation-delay:3.4s"></span>
  </div>

  <div class="wf-camera">
    <div class="wf-cam-body">
      <div class="wf-reel l"></div>
      <div class="wf-reel r"></div>
      <div class="wf-lens-housing"></div>
      <div class="wf-lens"></div>
    </div>
  </div>

  <div class="wf-stage">
    <p class="wf-kicker">Stream the Wild Side</p>
    <div class="wf-title" role="heading" aria-level="1">
      <span>W</span><span>I</span><span>L</span><span>D</span><span>F</span><span>L</span><span>I</span><span>X</span>
    </div>
    <div class="wf-underline"></div>
  </div>
</div>
"""

def afficher_bandeau():
    st.markdown(
        """
        <style>
          .block-container { padding-top: 1.2rem; padding-bottom: 0; max-width: 100%; }
          header[data-testid="stHeader"] { background: transparent; }
          #MainMenu, footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # --- Affiche le bandeau hero ---
    st.markdown(WILDFLIX_HERO, unsafe_allow_html=True)
