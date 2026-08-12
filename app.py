import math
import time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="TOX-PREP 3.2", page_icon="⚗️", layout="wide")

st.markdown("""
<style>
.block-container{max-width:1450px;padding-top:1.2rem}
.hero{padding:1.35rem 1.6rem;border:1px solid #d8e3ef;border-radius:22px;
background:linear-gradient(135deg,#ffffff 0%,#f3f8fc 100%);box-shadow:0 4px 16px rgba(20,50,90,.06)}
.hero h1{margin:0;color:#12315e;font-size:2.55rem}.hero p{margin:.35rem 0 0;color:#52637b;font-size:1.03rem}
.route{padding:1rem;margin:.8rem 0;border-radius:14px;background:#edf5fb;text-align:center;color:#173d6d;font-weight:800}
.modulebox{padding:.8rem;border:1px solid #dbe5ef;border-radius:14px;background:white;min-height:95px}
.mission{padding:1rem 1.15rem;border:1px solid #dbe5ee;border-radius:14px;background:#fff;margin:.7rem 0}
.formula{padding:.85rem;border-radius:12px;background:#f5f8fb;border:1px solid #dfe7ef;text-align:center;font-size:1.13rem}
.key{padding:.9rem 1rem;border-radius:12px;background:#fffaf0;border:1px solid #ead79e;margin-top:.7rem}
.anim{padding:1rem;border:1px solid #cbd9e8;border-radius:15px;background:#fbfdff;margin:.7rem 0}
.animstep{padding:.8rem;border-radius:12px;background:#f3f7fb;border:1px solid #dce6ef;text-align:center;min-height:100px}
.badge{display:inline-block;background:#eaf2fb;color:#173e78;padding:.25rem .7rem;border-radius:999px;font-weight:800}
.small{font-size:.88rem;color:#667085}
div[data-testid="stMetric"]{border:1px solid #e1e8f0;padding:.55rem;border-radius:13px;background:#fff}
.pearson-wrap{padding:1.4rem;border:1px solid #cbd9e8;border-radius:20px;background:linear-gradient(135deg,#ffffff,#f5f9fd);margin:.8rem 0}
.pearson-title{text-align:center;font-size:1.35rem;font-weight:800;color:#12315e;margin-bottom:1rem}
.pearson-grid{display:grid;grid-template-columns:1fr 1.3fr 1fr;gap:1rem;align-items:center}
.pearson-box{padding:1.3rem;border-radius:18px;border:2px solid #d7e3ef;background:white;text-align:center;min-height:135px;display:flex;flex-direction:column;justify-content:center}
.pearson-box strong{font-size:1.8rem;color:#173d6d}.pearson-box span{font-size:.95rem;color:#667085}
.pearson-center{padding:1.5rem;border-radius:50%;border:3px solid #9fb7d1;background:#eef5fb;text-align:center;min-width:150px;min-height:150px;display:flex;flex-direction:column;justify-content:center}
.pearson-center strong{font-size:2rem;color:#12315e}
.arrowbig{text-align:center;font-size:2.2rem;font-weight:900;color:#486b94}
.resultbig{padding:1rem;border-radius:16px;background:#eef7f1;border:1px solid #c8dfcf;text-align:center;font-size:1.2rem;font-weight:700}

.module-nav-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:.8rem 0 1rem}
.modbtn{display:flex;flex-direction:column;justify-content:center;align-items:center;text-decoration:none!important;
padding:1rem .6rem;border-radius:16px;color:white!important;font-weight:850;min-height:88px;
border:2px solid rgba(0,0,0,.08);box-shadow:0 7px 0 rgba(0,0,0,.18),0 10px 18px rgba(0,0,0,.12);
transition:transform .12s ease,box-shadow .12s ease;letter-spacing:.01em}
.modbtn:hover{transform:translateY(3px);box-shadow:0 4px 0 rgba(0,0,0,.18),0 7px 12px rgba(0,0,0,.12)}
.modbtn:active{transform:translateY(6px);box-shadow:0 1px 0 rgba(0,0,0,.2)}
.mod1{background:linear-gradient(180deg,#295f9e,#1f4b82)}
.mod2{background:linear-gradient(180deg,#168b7a,#0d6d60)}
.mod3{background:linear-gradient(180deg,#7a57b5,#604097)}
.mod4{background:linear-gradient(180deg,#d17a20,#a85e12)}
.mod5{background:linear-gradient(180deg,#a84254,#853243)}
.modbtn .mstate{font-size:.82rem;margin-top:.3rem;opacity:.95}

.labstage{position:relative;min-height:350px;border-radius:24px;border:1px solid #cddbea;
background:radial-gradient(circle at 50% 10%,#ffffff 0%,#f6faff 55%,#edf4fb 100%);
overflow:hidden;margin:.8rem 0 1rem;box-shadow:inset 0 -10px 35px rgba(34,72,116,.06)}
.bench{position:absolute;left:0;right:0;bottom:0;height:68px;background:linear-gradient(#d9e3ed,#bac9d8);
border-top:2px solid #aabaca}
.labtitle{position:absolute;top:18px;left:24px;font-weight:900;color:#12315e;font-size:1.25rem}
.flask{position:absolute;width:112px;height:145px;border:5px solid #294968;border-radius:16px 16px 34px 34px;
bottom:62px;background:rgba(255,255,255,.78);overflow:hidden;box-shadow:0 8px 15px rgba(0,0,0,.12)}
.flask:before{content:"";position:absolute;width:44px;height:35px;border:5px solid #294968;border-bottom:0;
top:-39px;left:29px;border-radius:8px 8px 0 0;background:#fff}
.liquid{position:absolute;left:0;right:0;bottom:0;height:32%;background:linear-gradient(180deg,#72b7d8,#3487b3);
animation:fillLiquid 4.8s ease-in-out infinite}
.liquid.green{background:linear-gradient(180deg,#74c8ac,#2d9070)}
.liquid.orange{background:linear-gradient(180deg,#f2bd6b,#d17a20)}
@keyframes fillLiquid{0%,12%{height:12%}55%,100%{height:70%}}
.drop{position:absolute;width:16px;height:22px;background:#4aa0c8;border-radius:50% 50% 58% 58%;
transform:rotate(45deg);animation:dropFall 2s ease-in infinite}
@keyframes dropFall{0%{top:105px;opacity:0}20%{opacity:1}75%{top:230px;opacity:1}100%{top:250px;opacity:0}}
.arrowmove{position:absolute;font-size:3rem;font-weight:900;color:#456b91;animation:arrowPulse 1.3s ease-in-out infinite}
@keyframes arrowPulse{0%,100%{transform:translateX(0);opacity:.45}50%{transform:translateX(13px);opacity:1}}
.balance{position:absolute;bottom:72px;width:150px;height:80px;border-radius:16px;background:#e9eef3;border:4px solid #485e72;
box-shadow:0 8px 14px rgba(0,0,0,.12)}
.balance:before{content:"⚖";font-size:3.2rem;position:absolute;left:45px;top:-48px}
.labeltag{position:absolute;padding:.45rem .7rem;background:white;border:1px solid #cad8e5;border-radius:10px;
box-shadow:0 4px 10px rgba(0,0,0,.08);font-weight:800;color:#173d6d}
.pipette{position:absolute;width:175px;height:18px;background:linear-gradient(90deg,#a9bfd2,#f8fbfd);
border:3px solid #48657d;border-radius:10px;transform:rotate(15deg);animation:pipMove 4s ease-in-out infinite}
.pipette:after{content:"";position:absolute;right:-28px;top:3px;border-left:30px solid #48657d;border-top:5px solid transparent;border-bottom:5px solid transparent}
@keyframes pipMove{0%,100%{transform:translate(0,0) rotate(15deg)}50%{transform:translate(55px,22px) rotate(15deg)}}
.stir{position:absolute;font-size:3rem;animation:spin 2s linear infinite}
@keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}

.calcguide{border-radius:20px;border:1px solid #cddbea;background:linear-gradient(135deg,#fff,#f7fbff);
padding:1.2rem 1.35rem;margin:1rem 0;box-shadow:0 5px 15px rgba(28,61,99,.07)}
.calcguide h4{margin:.1rem 0 .9rem;color:#12315e;font-size:1.25rem}
.calcflow{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;gap:.7rem;align-items:stretch}
.calcstep{padding:1rem;border-radius:15px;background:white;border:1px solid #d9e4ee;text-align:center;
display:flex;flex-direction:column;justify-content:center;min-height:120px}
.calcstep b{color:#173d6d;font-size:1.05rem}.calcstep .big{font-size:1.35rem;font-weight:900;margin-top:.4rem}
.calcarrow{display:flex;align-items:center;font-size:2.3rem;color:#6f88a3;font-weight:900}
@media(max-width:900px){.module-nav-grid{grid-template-columns:1fr 1fr}.calcflow{grid-template-columns:1fr}.calcarrow{justify-content:center;transform:rotate(90deg)}}

.convstage{position:relative;min-height:430px;border-radius:24px;border:1px solid #cbd9e8;
background:linear-gradient(180deg,#fbfdff 0%,#eef5fb 100%);overflow:hidden;margin:.8rem 0 1rem;
box-shadow:inset 0 -12px 35px rgba(25,58,94,.07)}
.convtitle{position:absolute;left:28px;top:20px;font-size:1.35rem;font-weight:900;color:#12315e}
.scale-row{position:absolute;left:7%;right:7%;top:105px;display:grid;grid-template-columns:repeat(7,1fr);gap:10px;align-items:center}
.scale-unit{padding:.75rem .25rem;border-radius:14px;background:white;border:2px solid #d4e0eb;
box-shadow:0 5px 0 #c4d1dd,0 8px 14px rgba(0,0,0,.08);text-align:center;font-weight:900;color:#173d6d}
.scale-unit.active{border-color:#2e6da4;background:#eef6fd;animation:unitPulse 1.8s ease-in-out infinite}
@keyframes unitPulse{0%,100%{transform:translateY(0);box-shadow:0 5px 0 #b9c9d8,0 8px 14px rgba(0,0,0,.08)}50%{transform:translateY(-7px);box-shadow:0 10px 0 #b9c9d8,0 14px 20px rgba(0,0,0,.10)}}
.conv-arrow{position:absolute;left:14%;right:14%;top:208px;height:6px;background:#7da4c5;border-radius:999px}
.conv-arrow:after{content:"";position:absolute;right:-2px;top:-9px;border-left:20px solid #7da4c5;border-top:12px solid transparent;border-bottom:12px solid transparent}
.conv-marker{position:absolute;top:186px;width:32px;height:32px;border-radius:50%;background:#1f5f96;border:5px solid #eaf3fb;
box-shadow:0 4px 12px rgba(0,0,0,.18);animation:moveMarker 4.5s ease-in-out infinite}
@keyframes moveMarker{0%,10%{left:15%}45%,55%{left:48%}90%,100%{left:80%}}
.conv-label{position:absolute;top:245px;left:0;right:0;text-align:center;font-weight:800;color:#4b6480;font-size:1.02rem;padding:0 7%}
.conv-lab{position:absolute;left:8%;bottom:45px;width:175px;height:95px;border-radius:18px;background:#e9eef3;border:5px solid #485e72;box-shadow:0 8px 16px rgba(0,0,0,.13)}
.conv-lab:before{content:"⚖️";position:absolute;font-size:4rem;left:48px;top:-58px}
.conv-beaker{position:absolute;right:10%;bottom:45px;width:130px;height:120px;border:5px solid #46627a;border-top:0;border-radius:0 0 25px 25px;background:rgba(255,255,255,.7);overflow:hidden}
.conv-beaker:before{content:"";position:absolute;left:12px;right:12px;bottom:0;height:60%;background:linear-gradient(180deg,#79bdd9,#3b8fb5);animation:beakerFill 4s ease-in-out infinite}
@keyframes beakerFill{0%,100%{height:25%}50%{height:72%}}
.conv-badge{position:absolute;padding:.45rem .75rem;border-radius:10px;background:white;border:1px solid #cad8e5;box-shadow:0 4px 10px rgba(0,0,0,.08);font-weight:850;color:#173d6d}
.converter-box{border:1px solid #cddbea;border-radius:20px;padding:1.15rem 1.25rem;background:linear-gradient(135deg,#ffffff,#f6faff);margin:1rem 0}
.converter-box h4{margin:0 0 .7rem;color:#12315e;font-size:1.25rem}
.converter-result{padding:1rem;border-radius:14px;background:#eef7f1;border:1px solid #c8dfcf;text-align:center;font-size:1.25rem;font-weight:900;color:#215b3b}

.st-key-module_nav_container div[data-testid="stColumn"] button{
    min-height:110px!important;border-radius:18px!important;border:2px solid rgba(0,0,0,.10)!important;
    color:white!important;font-weight:850!important;font-size:1.05rem!important;
    box-shadow:0 8px 0 rgba(0,0,0,.20),0 12px 20px rgba(0,0,0,.14)!important;
    transition:transform .12s ease,box-shadow .12s ease!important}
.st-key-module_nav_container div[data-testid="stColumn"] button:hover{
    transform:translateY(3px)!important;box-shadow:0 5px 0 rgba(0,0,0,.20),0 9px 15px rgba(0,0,0,.14)!important}
.st-key-module_nav_container div[data-testid="stColumn"] button:active{
    transform:translateY(7px)!important;box-shadow:0 1px 0 rgba(0,0,0,.22)!important}
.st-key-module_nav_container div[data-testid="stColumn"]:nth-child(1) button{background:linear-gradient(180deg,#3169a6,#245286)!important}
.st-key-module_nav_container div[data-testid="stColumn"]:nth-child(2) button{background:linear-gradient(180deg,#1c927f,#11705f)!important}
.st-key-module_nav_container div[data-testid="stColumn"]:nth-child(3) button{background:linear-gradient(180deg,#805bc0,#66439f)!important}
.st-key-module_nav_container div[data-testid="stColumn"]:nth-child(4) button{background:linear-gradient(180deg,#d77f20,#ad6111)!important}
.st-key-module_nav_container div[data-testid="stColumn"]:nth-child(5) button{background:linear-gradient(180deg,#ad4559,#893546)!important}

.st-key-mission_nav_I div[data-testid="stColumn"] button,
.st-key-mission_nav_II div[data-testid="stColumn"] button,
.st-key-mission_nav_III div[data-testid="stColumn"] button,
.st-key-mission_nav_IV div[data-testid="stColumn"] button,
.st-key-mission_nav_V div[data-testid="stColumn"] button{
    min-height:62px!important;border-radius:14px!important;color:white!important;font-weight:800!important;
    border:1px solid rgba(0,0,0,.10)!important;
    box-shadow:0 5px 0 rgba(0,0,0,.18),0 8px 13px rgba(0,0,0,.10)!important;
    transition:transform .12s ease,box-shadow .12s ease!important}
.st-key-mission_nav_I button{background:linear-gradient(180deg,#4d80ba,#35669f)!important}
.st-key-mission_nav_II button{background:linear-gradient(180deg,#35a08e,#21806f)!important}
.st-key-mission_nav_III button{background:linear-gradient(180deg,#936fc9,#7554ad)!important}
.st-key-mission_nav_IV button{background:linear-gradient(180deg,#df9141,#c17526)!important}
.st-key-mission_nav_V button{background:linear-gradient(180deg,#bc6271,#a24758)!important}
.st-key-mission_nav_I button:hover,.st-key-mission_nav_II button:hover,.st-key-mission_nav_III button:hover,
.st-key-mission_nav_IV button:hover,.st-key-mission_nav_V button:hover{
    transform:translateY(2px)!important;box-shadow:0 3px 0 rgba(0,0,0,.18),0 6px 10px rgba(0,0,0,.10)!important}
.st-key-mission_nav_I button:active,.st-key-mission_nav_II button:active,.st-key-mission_nav_III button:active,
.st-key-mission_nav_IV button:active,.st-key-mission_nav_V button:active{
    transform:translateY(5px)!important;box-shadow:0 1px 0 rgba(0,0,0,.18)!important}

.scene{position:relative;min-height:460px;margin:.9rem 0 1rem;border:1px solid #cbd9e8;border-radius:26px;
background:linear-gradient(180deg,#fbfdff 0%,#eef5fb 68%,#dfe9f2 68%,#c8d6e3 100%);
overflow:hidden;box-shadow:inset 0 -15px 35px rgba(25,58,94,.07),0 7px 18px rgba(18,49,94,.05)}
.scene-title{position:absolute;left:28px;top:22px;font-weight:900;color:#12315e;font-size:1.35rem;z-index:20}
.scene-sub{position:absolute;left:28px;top:60px;color:#60758d;font-weight:700;z-index:20}
.glass{position:absolute;width:125px;height:160px;border:6px solid #294968;border-top:0;border-radius:0 0 34px 34px;
bottom:70px;background:rgba(255,255,255,.72);overflow:hidden;box-shadow:0 9px 18px rgba(0,0,0,.12)}
.glass.tall{height:205px;width:145px}
.sol{position:absolute;left:0;right:0;bottom:0;height:20%;background:linear-gradient(#79bdd9,#398eb5)}
.sol.green{background:linear-gradient(#79cdb1,#329071)} .sol.orange{background:linear-gradient(#f4c070,#df8a2d)}
.sol.fill{animation:fillUp 5s ease-in-out infinite}.sol.drain{animation:drainDown 5s ease-in-out infinite}
@keyframes fillUp{0%,12%{height:12%}55%,85%{height:78%}100%{height:35%}}
@keyframes drainDown{0%,15%{height:72%}60%,100%{height:18%}}
.pour-stream{position:absolute;width:13px;height:145px;background:linear-gradient(#86c4df,#3d92b8);border-radius:9px;
animation:stream 3.5s ease-in-out infinite;opacity:0;z-index:8}
@keyframes stream{0%,20%{opacity:0;height:5px}30%,75%{opacity:1;height:140px}90%,100%{opacity:0;height:8px}}
.drop2{position:absolute;width:18px;height:25px;background:#4aa0c8;border-radius:55% 55% 65% 65%;
transform:rotate(45deg);animation:drop2 1.7s ease-in infinite;z-index:10}
@keyframes drop2{0%{transform:translateY(0) rotate(45deg);opacity:0}20%{opacity:1}80%{transform:translateY(120px) rotate(45deg);opacity:1}100%{transform:translateY(140px) rotate(45deg);opacity:0}}
.pipette2{position:absolute;width:220px;height:22px;background:linear-gradient(90deg,#adc2d4,#f8fbfd);
border:4px solid #48657d;border-radius:12px;transform:rotate(14deg);z-index:12;animation:pipetteTravel 4.4s ease-in-out infinite}
.pipette2:after{content:"";position:absolute;right:-35px;top:4px;border-left:38px solid #48657d;border-top:6px solid transparent;border-bottom:6px solid transparent}
@keyframes pipetteTravel{0%,12%{transform:translate(-30px,-15px) rotate(14deg)}45%,75%{transform:translate(90px,35px) rotate(14deg)}100%{transform:translate(-30px,-15px) rotate(14deg)}}
.stir2{position:absolute;font-size:4rem;color:#344b64;animation:spin2 1.7s linear infinite;z-index:12}
@keyframes spin2{from{transform:rotate(0)}to{transform:rotate(360deg)}}
.pulse-arrow{position:absolute;font-size:4rem;color:#6990b3;font-weight:900;animation:pulseArrow2 1.35s ease-in-out infinite;z-index:15}
@keyframes pulseArrow2{0%,100%{transform:translateX(0);opacity:.35}50%{transform:translateX(16px);opacity:1}}
.stage-label{position:absolute;padding:.55rem .8rem;background:white;border:1px solid #c8d6e4;border-radius:11px;
box-shadow:0 4px 10px rgba(0,0,0,.08);font-weight:900;color:#173d6d;z-index:16}
.stepdot{position:absolute;width:38px;height:38px;border-radius:50%;background:#1f5f96;color:white;display:flex;align-items:center;justify-content:center;
font-weight:900;box-shadow:0 4px 12px rgba(0,0,0,.16);z-index:20}
.timeline{position:absolute;left:10%;right:10%;top:105px;height:6px;background:#c9d7e4;border-radius:999px}
.timeline-run{position:absolute;left:10%;top:105px;height:6px;background:#347aaa;border-radius:999px;animation:timelineGrow 5s ease-in-out infinite}
@keyframes timelineGrow{0%{width:0}85%,100%{width:80%}}
.mixbeam{position:absolute;width:210px;height:14px;border-radius:999px;transform-origin:left center;opacity:.75}
.mixbeam.blue{background:#4c9cc1}.mixbeam.green{background:#47a787}
.mergecircle{position:absolute;width:155px;height:155px;border-radius:50%;background:radial-gradient(circle,#f7d39b 0%,#e79b3c 65%,#c9781e 100%);
box-shadow:0 0 0 10px rgba(231,155,60,.12),0 10px 20px rgba(0,0,0,.10);animation:mergePulse 2s ease-in-out infinite}
@keyframes mergePulse{0%,100%{transform:scale(.96)}50%{transform:scale(1.04)}}
.bubble{position:absolute;width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.72);animation:bubbleUp 2.6s linear infinite}
@keyframes bubbleUp{0%{transform:translateY(80px);opacity:0}20%{opacity:.8}100%{transform:translateY(-90px);opacity:0}}

/* --- TOX-PREP 3.2 virtual laboratory --- */
.virtual-lab{position:relative;min-height:520px;border-radius:26px;border:1px solid #c8d7e5;
background:linear-gradient(180deg,#fbfdff 0%,#edf4fb 64%,#dbe7f0 64%,#c6d5e2 100%);
overflow:hidden;margin:1rem 0;box-shadow:inset 0 -16px 38px rgba(28,60,94,.08),0 8px 20px rgba(20,50,90,.06)}
.vtitle{position:absolute;top:22px;left:28px;font-size:1.4rem;font-weight:900;color:#12315e}
.vsubtitle{position:absolute;top:62px;left:28px;color:#62768c;font-weight:700}
.vbench{position:absolute;left:0;right:0;bottom:0;height:82px;background:linear-gradient(#d7e2eb,#bac9d6);border-top:2px solid #aabac8}
.beaker{position:absolute;width:150px;height:145px;border:5px solid #405d75;border-top:0;border-radius:0 0 24px 24px;background:rgba(255,255,255,.72);bottom:80px;overflow:hidden}
.beaker:before{content:"";position:absolute;left:15px;right:15px;top:30px;border-top:2px solid rgba(64,93,117,.25)}
.volflask{position:absolute;width:125px;height:185px;border:5px solid #35536d;border-radius:0 0 55px 55px;background:rgba(255,255,255,.72);bottom:80px;overflow:visible}
.volflask:before{content:"";position:absolute;width:42px;height:70px;border:5px solid #35536d;border-bottom:0;left:36px;top:-68px;background:rgba(255,255,255,.9)}
.volflask:after{content:"";position:absolute;width:52px;border-top:3px solid #d44d4d;left:31px;top:-24px}
.graduated{position:absolute;width:95px;height:220px;border:5px solid #3c5b74;border-radius:10px 10px 20px 20px;background:rgba(255,255,255,.78);bottom:80px;overflow:hidden}
.graduated:after{content:"";position:absolute;left:12px;top:16px;width:38px;height:170px;background:repeating-linear-gradient(to bottom,transparent 0,transparent 12px,#7e94aa 13px,#7e94aa 14px)}
.vliquid{position:absolute;left:0;right:0;bottom:0;height:18%;background:linear-gradient(#75bad8,#378db4);animation:vfill 5s ease-in-out infinite}
.vliquid.green{background:linear-gradient(#7bc8ac,#319071)} .vliquid.orange{background:linear-gradient(#f3be6b,#dc882c)}
@keyframes vfill{0%,12%{height:12%}50%,82%{height:72%}100%{height:30%}}
.micropip{position:absolute;width:230px;height:24px;background:linear-gradient(90deg,#c5d6e5,#f8fbfd);border:4px solid #45637b;border-radius:12px;transform:rotate(12deg);animation:vpipe 4.2s ease-in-out infinite;z-index:10}
.micropip:after{content:"";position:absolute;right:-38px;top:4px;border-left:40px solid #45637b;border-top:7px solid transparent;border-bottom:7px solid transparent}
@keyframes vpipe{0%,12%{transform:translate(-25px,-10px) rotate(12deg)}45%,75%{transform:translate(95px,40px) rotate(12deg)}100%{transform:translate(-25px,-10px) rotate(12deg)}}
.balance3{position:absolute;width:190px;height:90px;border:5px solid #465d72;border-radius:18px;background:#e9eef3;bottom:80px;box-shadow:0 8px 16px rgba(0,0,0,.12)}
.balance3:before{content:"⚖️";position:absolute;left:61px;top:-64px;font-size:4.2rem}
.stockbottle{position:absolute;width:130px;height:170px;border:5px solid #3c5870;border-radius:18px 18px 28px 28px;background:rgba(255,255,255,.8);bottom:80px;overflow:hidden}
.stockbottle:before{content:"";position:absolute;width:65px;height:34px;background:#37536c;left:27px;top:-1px;border-radius:8px}
.vlabel{position:absolute;padding:.55rem .8rem;border-radius:11px;background:white;border:1px solid #c9d7e4;box-shadow:0 4px 11px rgba(0,0,0,.08);font-weight:900;color:#173d6d;z-index:15}
.vstep{border:1px solid #cbd9e6;border-radius:16px;background:#f8fbfe;padding:1rem;margin:.6rem 0}
.vstep.done{background:#eef8f1;border-color:#b9d9c2}
.material-card{padding:.85rem;border:1px solid #d9e4ee;border-radius:14px;background:white;min-height:90px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,.06)}
.material-card b{display:block;color:#173d6d;margin-top:.25rem}

/* --- TOX-PREP 3.2 · scientific lab scene --- */
.lab31{position:relative;min-height:620px;border-radius:26px;border:1px solid #c7d8e8;
background:linear-gradient(180deg,#fcfeff 0%,#f4f9fd 72%,#dbe7f0 72%,#c9d7e3 100%);
overflow:hidden;margin:1rem 0 1.2rem;box-shadow:0 8px 22px rgba(25,60,95,.07)}
.lab31-title{position:absolute;left:30px;top:22px;font-size:1.45rem;font-weight:900;color:#0e3769}
.lab31-sub{position:absolute;left:30px;top:63px;color:#60758b;font-weight:650}
.station{position:absolute;bottom:86px;text-align:center;color:#173e6d;font-weight:900}
.stepcap{display:inline-block;background:#fff;border:1px solid #c8d8e6;border-radius:12px;padding:8px 13px;
box-shadow:0 5px 12px rgba(20,50,80,.08);margin-bottom:14px}
.arrow31{position:absolute;font-size:3.2rem;color:#86a8c5;top:315px;animation:arrowpulse 1.7s ease-in-out infinite}
@keyframes arrowpulse{50%{transform:translateX(10px);opacity:.55}}
.balance-body{width:190px;height:105px;border:5px solid #456079;border-radius:18px;background:linear-gradient(#f8fafc,#dce5ec);position:relative}
.balance-pan{position:absolute;width:120px;height:13px;background:#8598a8;border-radius:50%;left:31px;top:-18px}
.balance-screen{position:absolute;width:76px;height:34px;background:#cde7d7;border:3px solid #466075;border-radius:7px;left:53px;top:48px;
font:800 14px monospace;color:#173e55;display:flex;align-items:center;justify-content:center}
.weighboat{position:absolute;width:70px;height:20px;border:3px solid #7e91a2;border-radius:50%;left:58px;top:-34px;background:#fff}
.powder{position:absolute;width:45px;height:12px;border-radius:50%;background:#e7e1cc;left:70px;top:-31px;animation:powderfade 5.5s infinite}
@keyframes powderfade{0%,22%{opacity:1}35%,100%{opacity:.25}}
.beaker31{width:150px;height:170px;border:5px solid #49657d;border-top:0;border-radius:0 0 20px 20px;position:relative;background:rgba(255,255,255,.75);overflow:hidden}
.beaker31:before{content:"";position:absolute;left:18px;right:18px;top:30px;height:95px;background:repeating-linear-gradient(to bottom,transparent 0,transparent 18px,#a7b7c5 19px,#a7b7c5 20px);opacity:.65}
.liq31{position:absolute;left:0;right:0;bottom:0;height:45%;background:linear-gradient(#77bedc,#3d94ba);animation:mixliq 5.5s ease-in-out infinite}
@keyframes mixliq{0%,15%{height:22%;opacity:.75}38%,78%{height:55%;opacity:1}100%{height:48%}}
.stirrod{position:absolute;width:8px;height:155px;background:linear-gradient(90deg,#dceaf3,#91aabd);border-radius:5px;left:76px;top:-35px;transform:rotate(12deg);animation:stir 1.1s ease-in-out infinite alternate;z-index:4}
@keyframes stir{from{transform:translateX(-14px) rotate(10deg)}to{transform:translateX(14px) rotate(-8deg)}}
.washbottle{position:absolute;width:72px;height:90px;border:4px solid #4c687f;border-radius:14px 14px 22px 22px;background:rgba(255,255,255,.8);right:-65px;top:45px}
.washbottle:before{content:"";position:absolute;width:65px;height:8px;background:#4c687f;right:-45px;top:-18px;transform:rotate(-28deg);border-radius:8px}
.flask31{width:165px;height:170px;border:5px solid #405e77;border-radius:50% 50% 42% 42%;position:relative;background:rgba(255,255,255,.8);overflow:visible}
.flask31:before{content:"";position:absolute;width:52px;height:125px;border-left:5px solid #405e77;border-right:5px solid #405e77;left:52px;top:-116px;background:rgba(255,255,255,.82)}
.flask31:after{content:"";position:absolute;width:67px;border-top:3px solid #d94b4b;left:46px;top:-50px;z-index:8}
.flaskliq{position:absolute;left:5px;right:5px;bottom:5px;height:30%;border-radius:0 0 65px 65px;background:linear-gradient(#75c7ad,#379a79);animation:aforo 6s ease-in-out infinite}
@keyframes aforo{0%,18%{height:12%}50%{height:58%}72%,100%{height:84%}}
.drop31{position:absolute;width:11px;height:16px;border-radius:55% 55% 60% 60%;background:#5db4d6;left:76px;top:-88px;animation:drop31 1.4s linear infinite;z-index:10}
@keyframes drop31{0%{transform:translateY(0);opacity:0}25%{opacity:1}85%{transform:translateY(92px);opacity:1}100%{transform:translateY(102px);opacity:0}}
.meniscus-note{position:absolute;right:-42px;top:-69px;font-size:.78rem;background:#fff7df;border:1px solid #e6c777;border-radius:9px;padding:6px 8px;color:#6a5317;width:150px}
.transferline{position:absolute;width:115px;height:8px;background:#79b9d4;border-radius:10px;transform:rotate(-15deg);animation:transfer31 2.2s ease-in-out infinite}
@keyframes transfer31{0%,15%{width:20px;opacity:.1}50%{width:115px;opacity:1}100%{width:20px;opacity:.1}}
.labelbottle{width:120px;height:155px;border:5px solid #435f77;border-radius:15px 15px 25px 25px;background:#fdfefe;position:relative}
.labelbottle:before{content:"SOLUCIÓN\A % p/v\A Fecha • Grupo";white-space:pre;position:absolute;left:10px;right:10px;top:47px;background:#eef5fb;border:1px solid #bdd0e0;border-radius:6px;padding:8px 3px;font-size:.7rem;line-height:1.4}
.process31{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:.5rem 0 1rem}
.p31{padding:.72rem .45rem;text-align:center;border-radius:12px;background:#f7fbfe;border:1px solid #d2dfeb;color:#234c75;font-weight:800;font-size:.86rem}

/* --- TOX-PREP 3.2 shared scientific identity --- */
.master-scene{position:relative;min-height:600px;border-radius:26px;border:1px solid #c7d8e8;
background:linear-gradient(180deg,#fcfeff 0%,#f4f9fd 72%,#dbe7f0 72%,#c9d7e3 100%);
overflow:hidden;margin:1rem 0 1.15rem;box-shadow:0 8px 22px rgba(25,60,95,.07)}
.ms-title{position:absolute;left:30px;top:22px;font-size:1.42rem;font-weight:900;color:#0e3769}
.ms-sub{position:absolute;left:30px;top:63px;color:#60758b;font-weight:650}
.ms-station{position:absolute;bottom:88px;text-align:center;color:#173e6d;font-weight:900}
.ms-cap{display:inline-block;background:#fff;border:1px solid #c8d8e6;border-radius:12px;padding:8px 13px;
box-shadow:0 5px 12px rgba(20,50,80,.08);margin-bottom:14px}
.ms-arrow{position:absolute;font-size:3.2rem;color:#86a8c5;top:315px;animation:arrowpulse 1.7s ease-in-out infinite}
.ms-process{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin:.5rem 0 1rem}
.ms-step{padding:.72rem .45rem;text-align:center;border-radius:12px;background:#f7fbfe;border:1px solid #d2dfeb;color:#234c75;font-weight:800;font-size:.86rem}
.tube{width:88px;height:180px;border:5px solid #44627a;border-radius:10px 10px 28px 28px;background:rgba(255,255,255,.8);position:relative;overflow:hidden}
.tube .vliquid{height:45%}
.stock31{width:130px;height:170px;border:5px solid #3f5c74;border-radius:18px 18px 28px 28px;background:rgba(255,255,255,.82);position:relative;overflow:hidden}
.stock31:before{content:"";position:absolute;left:26px;top:-1px;width:68px;height:34px;background:#354f66;border-radius:8px}
.pearsonX{position:absolute;width:230px;height:12px;background:#5b89ad;border-radius:10px;transform-origin:left center;opacity:.72}
.target-circle{position:absolute;width:165px;height:165px;border-radius:50%;background:radial-gradient(circle,#ffe2ad 0%,#e9a24c 62%,#cf7f28 100%);
box-shadow:0 0 0 12px rgba(231,155,60,.12),0 10px 20px rgba(0,0,0,.10)}
.checkcard{position:absolute;padding:1rem 1.1rem;border-radius:16px;background:#fff;border:1px solid #c9d7e4;
box-shadow:0 5px 13px rgba(0,0,0,.08);font-weight:850;color:#173e6d;line-height:1.5}

/* --- Misión 3 · composición corregida --- */
.m3-scene{min-height:560px}
.m3-station{position:absolute;bottom:94px;text-align:center;color:#173e6d;font-weight:900}
.m3-cap{display:inline-block;background:#fff;border:1px solid #c8d8e6;border-radius:12px;padding:8px 13px;box-shadow:0 5px 12px rgba(20,50,80,.08);margin-bottom:16px}
.m3-cylinder{position:relative;margin:0 auto;width:82px;height:205px;border:5px solid #3c5b74;border-radius:9px 9px 18px 18px;background:rgba(255,255,255,.8);overflow:hidden}
.m3-cylinder:after{content:"";position:absolute;left:12px;top:18px;width:34px;height:158px;background:repeating-linear-gradient(to bottom,transparent 0,transparent 12px,#7e94aa 13px,#7e94aa 14px)}
.m3-cyl-liq{position:absolute;left:0;right:0;bottom:0;height:48%;background:linear-gradient(#f3be6b,#dc882c)}
.m3-pipette{position:relative;margin:72px auto 0;width:190px;height:20px;background:linear-gradient(90deg,#c5d6e5,#f8fbfd);border:4px solid #45637b;border-radius:12px;transform:rotate(10deg);animation:m3pipe 4.8s ease-in-out infinite}
.m3-pipette:after{content:"";position:absolute;right:-34px;top:3px;border-left:36px solid #45637b;border-top:7px solid transparent;border-bottom:7px solid transparent}
@keyframes m3pipe{0%,15%{transform:translate(-15px,-10px) rotate(10deg)}45%,70%{transform:translate(35px,18px) rotate(10deg)}100%{transform:translate(-15px,-10px) rotate(10deg)}}
.m3-flask{position:relative;margin:58px auto 0;width:128px;height:132px;border:5px solid #405e77;border-radius:50% 50% 42% 42%;background:rgba(255,255,255,.82)}
.m3-flask:before{content:"";position:absolute;width:40px;height:86px;border-left:5px solid #405e77;border-right:5px solid #405e77;left:39px;top:-80px;background:rgba(255,255,255,.84)}
.m3-flask:after{content:"";position:absolute;width:53px;border-top:3px solid #d94b4b;left:33px;top:-34px;z-index:8}
.m3-flask-liq{position:absolute;left:5px;right:5px;bottom:5px;height:72%;border-radius:0 0 52px 52px;background:linear-gradient(#75c7ad,#379a79);animation:m3fill 5s ease-in-out infinite}
@keyframes m3fill{0%,18%{height:25%}55%,100%{height:72%}}
.m3-drop{position:absolute;width:10px;height:14px;border-radius:55%;background:#5db4d6;left:59px;top:-62px;animation:drop31 1.4s linear infinite;z-index:10}
.m3-meniscus{position:absolute;left:50%;transform:translateX(-50%);top:-118px;width:160px;background:#fff7df;border:1px solid #e6c777;border-radius:10px;padding:7px 9px;color:#6a5317;font-size:.75rem;line-height:1.25;box-shadow:0 4px 10px rgba(0,0,0,.05)}
.m3-mix{position:relative;margin:52px auto 0;width:112px;height:142px;border:5px solid #405e77;border-radius:18px 18px 34px 34px;background:rgba(255,255,255,.82);overflow:hidden}
.m3-mix:before{content:"↻";position:absolute;z-index:4;left:34px;top:34px;font-size:2.8rem;color:#244a70;animation:m3spin 1.4s linear infinite}
.m3-mix-liq{position:absolute;left:4px;right:4px;bottom:4px;height:48%;border-radius:0 0 28px 28px;background:linear-gradient(#75c7ad,#379a79)}
@keyframes m3spin{to{transform:rotate(360deg)}}
.m3-arrow{position:absolute;font-size:2.8rem;color:#86a8c5;top:292px;animation:arrowpulse 1.7s ease-in-out infinite}

</style>
""", unsafe_allow_html=True)

DEFAULT={"started":False,"name":"","level":1,"score":0,"attempts":{},"solved":{},"feedback":{}}
for k,v in DEFAULT.items():
    if k not in st.session_state:
        st.session_state[k]=v.copy() if isinstance(v,dict) else v

TOTAL=10
TITLES={
1:"Unidades y seguridad del cálculo",
2:"% p/v · Solución hipertónica",
3:"% v/v · Preparación volumétrica",
4:"C₁V₁ = C₂V₂ · Azul de metileno",
5:"% p/v ↔ mg/mL",
6:"Diluciones seriadas en toxicología analítica",
7:"Cuadrado de Pearson",
8:"Corrección por pureza",
9:"Detecte el error de preparación",
10:"Código Tóxico · Estación veterinaria final"
}
MODULES={
"I · Fundamentos":[1],
"II · Preparación":[2,3],
"III · Diluciones":[4,5,6],
"IV · Mezclas":[7,8],
"V · Integración":[9,10]
}
MOD_BY_LEVEL={l:m for m,ls in MODULES.items() for l in ls}

G={
"% p/v":"Gramos de soluto contenidos en 100 mL de solución final.",
"% v/v":"Mililitros de un componente líquido contenidos en 100 mL de solución final.",
"mg/mL":"Miligramos de soluto contenidos en cada mililitro de solución.",
"C₁V₁=C₂V₂":"Relación de conservación para una dilución simple: concentración inicial × volumen tomado = concentración final × volumen final.",
"Factor de dilución":"Relación entre concentración inicial y final. En una dilución simple también puede expresarse como volumen final dividido entre la alícuota.",
"Dilución seriada":"Secuencia de diluciones en la que una alícuota de una dilución se usa para preparar la siguiente.",
"Cuadrado de Pearson":"Método aritmético para calcular la proporción de dos preparaciones de concentraciones diferentes necesaria para obtener una concentración intermedia.",
"Pureza":"Fracción del reactivo comercial que corresponde al compuesto de interés.",
"Rotulado":"Identificación de la preparación con nombre, concentración, fecha, responsable y demás datos requeridos por el contexto.",
"Azul de metileno":"En esta actividad se usa una solución madre al 1 % p/v (=10 mg/mL) para practicar diluciones. El ejercicio es formativo y no constituye una prescripción clínica.",
"Solución hipertónica":"Solución con tonicidad efectiva superior a la del fluido de referencia. Una concentración porcentual no sustituye la evaluación clínica de composición, tonicidad e indicación.",
"Volumen final":"Volumen total de la solución una vez terminada la preparación. No equivale necesariamente al volumen de solvente añadido."
}

ANIMATIONS={
1:["📏 Identifique las unidades","🔁 Convierta antes de calcular","🧮 Realice la operación","✅ Verifique magnitud y unidad"],
2:["⚖️ Pese el soluto","🥛 Disuelva en parte del solvente","⚗️ Transfiera al recipiente volumétrico","💧 Complete hasta volumen final","🔄 Homogeneice","🏷️ Rotule"],
3:["🧴 Mida el componente líquido","⚗️ Transfiera","💧 Complete hasta volumen final","🔄 Homogeneice","🏷️ Rotule"],
4:["🧴 Identifique C₁","🎯 Defina C₂ y V₂","🧮 Calcule V₁","🧪 Tome la alícuota","💧 Complete hasta V₂","🏷️ Rotule"],
5:["% p/v","➡️ g/100 mL","➡️ mg/100 mL","➡️ mg/mL"],
6:["🧪 Muestra original","➡️ 1ª dilución","➡️ 2ª dilución","📉 Calcule factor acumulado"],
7:["⬆️ Concentración alta","🎯 Concentración objetivo","⬇️ Concentración baja","✖️ Diferencias diagonales","📐 Obtenga proporción","🧪 Convierta a volumen"],
8:["🎯 Masa pura requerida","📄 Revise pureza","➗ Corrija por fracción de pureza","⚖️ Pese la masa corregida"],
9:["🧾 Lea el procedimiento","🧮 Revise el cálculo","⚗️ Revise el volumen final","🏷️ Revise rotulado"],
10:["🐾 Identifique el escenario veterinario","🧮 Calcule","⚗️ Prepare","✅ Verifique","🏷️ Rotule","🧠 Interprete"]
}

def show_animation(level):
    st.markdown('<div class="anim"><b>🎬 Preparación visual</b><br><span class="small">Observe la secuencia antes de resolver el desafío.</span></div>', unsafe_allow_html=True)
    cols=st.columns(len(ANIMATIONS[level]))
    for c,step in zip(cols,ANIMATIONS[level]):
        c.markdown(f'<div class="animstep">{step}</div>',unsafe_allow_html=True)
    if st.button("▶ Reproducir animación", key=f"anim_{level}"):
        holder=st.empty()
        for i,step in enumerate(ANIMATIONS[level],1):
            holder.info(f"Paso {i}/{len(ANIMATIONS[level])}: {step}")
            time.sleep(.45)
        holder.success("Secuencia completada. Ahora resuelva el ejercicio.")

def concept(names):
    with st.expander("📚 Consultar concepto"):
        for n in names:
            st.markdown(f"**{n}:** {G[n]}")

def submit(level, ok, good, hint):
    if st.session_state.solved.get(level): return
    a=st.session_state.attempts.get(level,0)+1
    st.session_state.attempts[level]=a
    if ok:
        factor=1 if a==1 else .7 if a==2 else .4
        p=round(10*factor)
        st.session_state.score+=p
        st.session_state.solved[level]=True
        st.session_state.feedback[level]=("ok",f"{good} **+{p} puntos.**")
    else:
        st.session_state.feedback[level]=("bad",hint)

def feedback(level):
    if level in st.session_state.feedback:
        k,t=st.session_state.feedback[level]
        (st.success if k=="ok" else st.warning)(("✅ " if k=="ok" else "💡 ")+t)

def mission(text):
    st.markdown(f'<div class="mission"><b>🎯 Situación veterinaria:</b> {text}</div>',unsafe_allow_html=True)

def key(text):
    st.markdown(f'<div class="key"><b>⭐ Idea clave:</b> {text}</div>',unsafe_allow_html=True)

def reset():
    for k,v in DEFAULT.items():
        st.session_state[k]=v.copy() if isinstance(v,dict) else v
    st.rerun()

def goto(level):
    st.session_state.level=level
    st.rerun()


GUIDES={
1:("Ejemplo: convertir 1,2 g a mg",["Identifique equivalencia","1 g = 1000 mg","Multiplique","1,2 × 1000","Resultado","1200 mg"]),
2:("Ejemplo: preparar 100 mL al 4 % p/v",["Interprete el %","4 g / 100 mL","Use el volumen final","100 mL","Resultado","4 g de soluto"]),
3:("Ejemplo: preparar 100 mL al 30 % v/v",["Interprete el %","30 mL / 100 mL","Use el volumen final","100 mL","Resultado","30 mL del componente"]),
4:("Ejemplo: diluir 2 % hasta 0,5 % y preparar 100 mL",["Fórmula","C₁V₁=C₂V₂","Sustituya","2·V₁=0,5·100","Resultado","V₁ = 25 mL"]),
5:("Ejemplo: convertir 2 % p/v a mg/mL",["Interprete","2 g / 100 mL","Convierta","2000 mg / 100 mL","Resultado","20 mg/mL"]),
6:("Ejemplo: una dilución 1:5 de 500 µg/mL",["Concentración inicial","500 µg/mL","Divida por FD","500 ÷ 5","Resultado","100 µg/mL"]),
7:("Ejemplo Pearson distinto: 15 % + 5 % → 10 %",["Diagonales","|10−5|=5","Otra diagonal","|15−10|=5","Resultado","Relación 1:1"]),
8:("Ejemplo: se necesitan 8 g puros con reactivo al 80 %",["Masa requerida","8 g","Corrija pureza","8 ÷ 0,80","Resultado","10 g"]),
9:("Ejemplo de revisión",["Objetivo","200 mL al 5 % p/v","Masa","10 g","Procedimiento","Completar hasta 200 mL finales"]),
10:("Ejemplo integrador: 1 % → 0,2 %, V₂=100 mL",["Fórmula","C₁V₁=C₂V₂","Sustituya","1·V₁=0,2·100","Resultado","V₁ = 20 mL"])
}

def calc_guide(level):
    title,vals=GUIDES[level]
    html=f'''<div class="calcguide">
      <h4>🧭 Ejemplo resuelto · Guía de cálculo</h4>
      <div class="small">{title}. Este ejemplo es diferente al ejercicio evaluado.</div>
      <div class="calcflow">
        <div class="calcstep"><b>{vals[0]}</b><div class="big">{vals[1]}</div></div>
        <div class="calcarrow">→</div>
        <div class="calcstep"><b>{vals[2]}</b><div class="big">{vals[3]}</div></div>
        <div class="calcarrow">→</div>
        <div class="calcstep"><b>{vals[4]}</b><div class="big">{vals[5]}</div></div>
      </div>
    </div>'''
    st.markdown(html,unsafe_allow_html=True)


MASS_FACTORS={"µg":1e-6,"mg":1e-3,"g":1.0,"kg":1000.0}
VOL_FACTORS={"µL":1e-3,"mL":1.0,"cL":10.0,"dL":100.0,"L":1000.0}

def unit_converter():
    st.markdown('<div class="converter-box"><h4>🔄 Convertidor interactivo de masa y volumen</h4><div class="small">Explore valores distintos al ejercicio. Esta herramienta no suma puntos.</div></div>', unsafe_allow_html=True)
    kind=st.radio("Tipo de conversión",["Masa","Volumen"],horizontal=True,key="conv_kind")
    factors=MASS_FACTORS if kind=="Masa" else VOL_FACTORS
    units=list(factors.keys())
    c1,c2,c3=st.columns([1.2,1,1])
    value=c1.number_input("Valor",min_value=0.0,value=1.0,step=.1,key="conv_val")
    default_from=2 if kind=="Masa" else 1
    default_to=1 if kind=="Masa" else 4
    from_u=c2.selectbox("Desde",units,index=default_from,key="conv_from")
    to_u=c3.selectbox("Hacia",units,index=default_to,key="conv_to")
    base=value*factors[from_u]
    result=base/factors[to_u]
    st.markdown(f'<div class="converter-result">{value:g} {from_u} = {result:g} {to_u}</div>',unsafe_allow_html=True)
    with st.expander("¿Cómo se obtuvo?"):
        if kind=="Masa":
            st.write(f"Paso 1: convertir a gramos: {value:g} {from_u} × {factors[from_u]:g} = {base:g} g.")
            st.write(f"Paso 2: convertir de gramos a {to_u}: {base:g} ÷ {factors[to_u]:g} = {result:g} {to_u}.")
        else:
            st.write(f"Paso 1: convertir a mililitros: {value:g} {from_u} × {factors[from_u]:g} = {base:g} mL.")
            st.write(f"Paso 2: convertir de mililitros a {to_u}: {base:g} ÷ {factors[to_u]:g} = {result:g} {to_u}.")

def lab_animation(level):
    if level==1:
        # Misión 1 conserva la animación especial de conversión de unidades.
        return

    if level==2:
        html="""<div class="scene">
        <div class="scene-title">🎬 Preparación de una solución % p/v</div>
        <div class="scene-sub">Pesar → disolver → transferir → aforar → homogeneizar → rotular</div>
        <div class="timeline"></div><div class="timeline-run"></div>
        <div class="stepdot" style="left:9%;top:88px">1</div>
        <div class="stage-label" style="left:5%;bottom:270px">⚖️ PESAR SOLUTO</div>
        <div class="balance" style="left:7%;bottom:80px"></div>
        <div class="pulse-arrow" style="left:29%;bottom:150px">➜</div>
        <div class="stepdot" style="left:40%;top:88px">2</div>
        <div class="glass" style="left:38%"><div class="sol fill"></div></div>
        <div class="pour-stream" style="left:43%;top:155px"></div>
        <div class="stage-label" style="left:35%;bottom:270px">🥛 DISOLVER</div>
        <div class="pulse-arrow" style="left:58%;bottom:150px">➜</div>
        <div class="stepdot" style="left:70%;top:88px">3</div>
        <div class="glass tall" style="right:12%"><div class="sol green fill"></div></div>
        <div class="drop2" style="right:17%;top:155px"></div>
        <div class="stir2" style="right:16%;bottom:115px">↻</div>
        <div class="stage-label" style="right:6%;bottom:310px">⚗️ AFORAR + HOMOGENEIZAR</div>
        </div>"""

    elif level==3:
        html="""<div class="scene">
        <div class="scene-title">🎬 Preparación de una solución % v/v</div>
        <div class="scene-sub">Medir el componente líquido → transferir → completar hasta el volumen final</div>
        <div class="timeline"></div><div class="timeline-run"></div>
        <div class="stepdot" style="left:8%;top:88px">1</div>
        <div class="pipette2" style="left:5%;top:175px"></div>
        <div class="stage-label" style="left:5%;bottom:95px">MEDIR VOLUMEN</div>
        <div class="pulse-arrow" style="left:34%;bottom:150px">➜</div>
        <div class="stepdot" style="left:47%;top:88px">2</div>
        <div class="glass" style="left:45%"><div class="sol orange fill"></div></div>
        <div class="drop2" style="left:50%;top:165px"></div>
        <div class="stage-label" style="left:41%;bottom:280px">TRANSFERIR</div>
        <div class="pulse-arrow" style="left:63%;bottom:150px">➜</div>
        <div class="stepdot" style="left:76%;top:88px">3</div>
        <div class="glass tall" style="right:9%"><div class="sol green fill"></div></div>
        <div class="pour-stream" style="right:15%;top:145px"></div>
        <div class="stir2" style="right:14%;bottom:120px">↻</div>
        <div class="stage-label" style="right:5%;bottom:315px">COMPLETAR VOLUMEN FINAL</div>
        </div>"""

    elif level in (4,5):
        html="""<div class="scene">
        <div class="scene-title">🎬 Dilución desde una solución madre</div>
        <div class="scene-sub">Tomar V₁ → transferir → completar hasta V₂ → homogeneizar</div>
        <div class="timeline"></div><div class="timeline-run"></div>
        <div class="glass" style="left:6%"><div class="sol drain"></div></div>
        <div class="stage-label" style="left:3%;bottom:285px">SOLUCIÓN MADRE</div>
        <div class="pipette2" style="left:24%;top:170px"></div>
        <div class="drop2" style="left:51%;top:215px"></div>
        <div class="stage-label" style="left:31%;bottom:305px">TOMAR V₁</div>
        <div class="pulse-arrow" style="left:52%;bottom:150px">➜</div>
        <div class="glass tall" style="right:12%"><div class="sol green fill"></div></div>
        <div class="pour-stream" style="right:18%;top:145px"></div>
        <div class="stir2" style="right:17%;bottom:120px">↻</div>
        <div class="stage-label" style="right:7%;bottom:325px">COMPLETAR HASTA V₂</div>
        </div>"""

    elif level==6:
        html="""<div class="scene">
        <div class="scene-title">🎬 Dilución seriada</div>
        <div class="scene-sub">Una alícuota de cada dilución se utiliza para preparar la siguiente</div>
        <div class="timeline"></div><div class="timeline-run"></div>
        <div class="glass" style="left:5%;width:105px;height:135px"><div class="sol drain"></div></div>
        <div class="stage-label" style="left:3%;bottom:260px">MUESTRA ORIGINAL</div>
        <div class="pipette2" style="left:18%;top:165px"></div>
        <div class="pulse-arrow" style="left:35%;bottom:145px">➜</div>
        <div class="glass" style="left:43%;width:105px;height:135px"><div class="sol green fill"></div></div>
        <div class="stage-label" style="left:40%;bottom:260px">1ª DILUCIÓN</div>
        <div class="pipette2" style="left:53%;top:190px;animation-delay:1.2s"></div>
        <div class="pulse-arrow" style="left:70%;bottom:145px">➜</div>
        <div class="glass" style="right:7%;width:105px;height:135px"><div class="sol orange fill"></div></div>
        <div class="stage-label" style="right:4%;bottom:260px">2ª DILUCIÓN</div>
        </div>"""

    elif level==7:
        html="""<div class="scene">
        <div class="scene-title">🎬 Cuadrado de Pearson · Mezcla de concentraciones</div>
        <div class="scene-sub">Las dos preparaciones convergen visualmente hacia una concentración objetivo</div>
        <div class="glass" style="left:6%"><div class="sol"></div></div>
        <div class="stage-label" style="left:3%;bottom:285px">CONCENTRACIÓN ALTA</div>
        <div class="glass" style="left:28%"><div class="sol green"></div></div>
        <div class="stage-label" style="left:25%;bottom:285px">CONCENTRACIÓN BAJA</div>
        <div class="mixbeam blue" style="left:38%;top:245px;transform:rotate(18deg)"></div>
        <div class="mixbeam green" style="left:38%;top:275px;transform:rotate(-18deg)"></div>
        <div class="mergecircle" style="right:18%;top:180px"></div>
        <div class="bubble" style="right:24%;top:225px"></div>
        <div class="bubble" style="right:20%;top:260px;animation-delay:.7s"></div>
        <div class="bubble" style="right:27%;top:290px;animation-delay:1.2s"></div>
        <div class="stir2" style="right:21%;top:225px">↻</div>
        <div class="stage-label" style="right:10%;bottom:110px">CONCENTRACIÓN OBJETIVO</div>
        </div>"""

    elif level==8:
        html="""<div class="scene">
        <div class="scene-title">🎬 Corrección por pureza</div>
        <div class="scene-sub">La masa comercial se corrige antes del pesaje</div>
        <div class="stage-label" style="left:6%;bottom:230px;font-size:1.1rem">MASA PURA REQUERIDA</div>
        <div class="pulse-arrow" style="left:33%;bottom:160px">➜</div>
        <div class="stage-label" style="left:45%;bottom:230px;font-size:1.1rem">÷ FRACCIÓN DE PUREZA</div>
        <div class="pulse-arrow" style="left:68%;bottom:160px">➜</div>
        <div class="balance" style="right:7%;bottom:80px"></div>
        <div class="stage-label" style="right:4%;bottom:240px">MASA A PESAR</div>
        </div>"""

    else:
        html="""<div class="scene">
        <div class="scene-title">🎬 Verificación final de la preparación</div>
        <div class="scene-sub">Calcular → preparar → verificar → homogeneizar → rotular</div>
        <div class="glass tall" style="left:8%"><div class="sol green fill"></div></div>
        <div class="stage-label" style="left:5%;bottom:320px">PREPARACIÓN</div>
        <div class="pulse-arrow" style="left:31%;bottom:155px">➜</div>
        <div class="stage-label" style="left:43%;bottom:235px;font-size:1.08rem">✓ CONCENTRACIÓN<br>✓ VOLUMEN FINAL<br>✓ UNIDADES</div>
        <div class="pulse-arrow" style="left:66%;bottom:155px">➜</div>
        <div class="stage-label" style="right:7%;bottom:225px;font-size:1.15rem">🏷️ ROTULAR<br>Y DOCUMENTAR</div>
        </div>"""

    st.markdown(html,unsafe_allow_html=True)



def mission2_master_scene():
    st.markdown("""
    <div class="lab31">
      <div class="lab31-title">🧪 Preparación gravimétrica–volumétrica · % p/v</div>
      <div class="lab31-sub">Secuencia técnica: pesar → disolver → transferir cuantitativamente → aforar → homogeneizar → rotular.</div>

      <div class="station" style="left:4%;width:200px">
        <div class="stepcap">1 · PESAR</div>
        <div class="balance-body"><div class="balance-pan"></div><div class="weighboat"></div><div class="powder"></div><div class="balance-screen">5.000 g</div></div>
      </div>

      <div class="arrow31" style="left:20%">➜</div>

      <div class="station" style="left:27%;width:170px">
        <div class="stepcap">2 · DISOLVER</div>
        <div class="beaker31"><div class="liq31"></div><div class="stirrod"></div></div>
        <div class="washbottle"></div>
      </div>

      <div class="arrow31" style="left:44%">➜</div>
      <div class="transferline" style="left:46%;top:390px"></div>

      <div class="station" style="left:54%;width:175px">
        <div class="stepcap">3 · AFORAR</div>
        <div class="flask31"><div class="flaskliq"></div><div class="drop31"></div><div class="meniscus-note">Ajustar el menisco a la línea de aforo.</div></div>
      </div>

      <div class="arrow31" style="left:72%">➜</div>

      <div class="station" style="right:5%;width:145px">
        <div class="stepcap">4 · ROTULAR</div>
        <div class="labelbottle"></div>
      </div>
    </div>

    <div class="process31">
      <div class="p31">⚖️ Pesar</div><div class="p31">🥛 Disolver</div><div class="p31">🚿 Transferir + lavar</div>
      <div class="p31">⚗️ Aforar</div><div class="p31">🔄 Homogeneizar</div><div class="p31">🏷️ Rotular</div>
    </div>
    """, unsafe_allow_html=True)

    st.info("📌 **Principio técnico:** en una preparación % p/v, el volumen indicado corresponde al **volumen final de la solución**, no al volumen de solvente que se agrega inicialmente.")


def master_scene(level):
    if level==2:
        return  # Misión 2 usa su escena maestra específica.

    if level==3:
        st.markdown("""
        <div class="master-scene m3-scene">
          <div class="ms-title">🧪 Preparación volumétrica · % v/v</div>
          <div class="ms-sub">Medir el componente líquido → transferir al matraz → añadir diluyente y aforar → homogeneizar.</div>
          <div class="m3-station" style="left:4%;width:150px"><div class="m3-cap">1 · MEDIR</div><div class="m3-cylinder"><div class="m3-cyl-liq"></div></div></div>
          <div class="m3-arrow" style="left:22%">➜</div>
          <div class="m3-station" style="left:29%;width:220px"><div class="m3-cap">2 · TRANSFERIR</div><div class="m3-pipette"></div></div>
          <div class="m3-arrow" style="left:48%">➜</div>
          <div class="m3-station" style="left:56%;width:190px"><div class="m3-cap">3 · AFORAR</div><div class="m3-flask"><div class="m3-flask-liq"></div><div class="m3-drop"></div><div class="m3-meniscus">Ajustar el menisco exactamente a la marca de aforo.</div></div></div>
          <div class="m3-arrow" style="left:76%">➜</div>
          <div class="m3-station" style="right:3%;width:150px"><div class="m3-cap">4 · HOMOGENEIZAR</div><div class="m3-mix"><div class="m3-mix-liq"></div></div></div>
        </div>
        <div class="ms-process"><div class="ms-step">🧪 Medir</div><div class="ms-step">💧 Transferir</div><div class="ms-step">🚿 Añadir diluyente</div><div class="ms-step">⚗️ Aforar</div><div class="ms-step">🔄 Homogeneizar</div><div class="ms-step">🏷️ Rotular y verificar</div></div>
        """,unsafe_allow_html=True)

    elif level in (4,5):
        st.markdown("""
        <div class="master-scene">
          <div class="ms-title">🧪 Dilución desde solución madre</div>
          <div class="ms-sub">Identificar C₁, C₂ y V₂ → tomar V₁ → transferir → aforar → homogeneizar.</div>
          <div class="ms-station" style="left:5%;width:145px"><div class="ms-cap">1 · C₁</div><div class="stock31"><div class="vliquid"></div></div></div>
          <div class="ms-arrow" style="left:22%">➜</div>
          <div class="ms-station" style="left:32%;width:210px"><div class="ms-cap">2 · TOMAR V₁</div><div class="micropip" style="left:-5px;top:70px"></div></div>
          <div class="ms-arrow" style="left:53%">➜</div>
          <div class="ms-station" style="right:13%;width:180px"><div class="ms-cap">3 · COMPLETAR V₂</div><div class="flask31"><div class="flaskliq"></div><div class="drop31"></div></div></div>
        </div>
        <div class="ms-process"><div class="ms-step">📌 Identificar C₁</div><div class="ms-step">🎯 Definir C₂</div><div class="ms-step">🧮 Calcular V₁</div><div class="ms-step">💧 Pipetear</div><div class="ms-step">⚗️ Aforar</div><div class="ms-step">🏷️ Rotular</div></div>
        """,unsafe_allow_html=True)

    elif level==6:
        st.markdown("""
        <div class="master-scene">
          <div class="ms-title">🧪 Dilución seriada</div>
          <div class="ms-sub">Cada tubo se prepara a partir de una alícuota de la dilución inmediatamente anterior.</div>
          <div class="ms-station" style="left:5%;width:110px"><div class="ms-cap">MUESTRA</div><div class="tube"><div class="vliquid"></div></div></div>
          <div class="ms-arrow" style="left:22%">➜</div>
          <div class="ms-station" style="left:36%;width:110px"><div class="ms-cap">1:10</div><div class="tube"><div class="vliquid green"></div></div></div>
          <div class="ms-arrow" style="left:53%">➜</div>
          <div class="ms-station" style="right:18%;width:110px"><div class="ms-cap">1:100</div><div class="tube"><div class="vliquid orange"></div></div></div>
        </div>
        <div class="ms-process"><div class="ms-step">🧪 Muestra</div><div class="ms-step">💧 Tomar alícuota</div><div class="ms-step">➕ Diluyente</div><div class="ms-step">🔄 Mezclar</div><div class="ms-step">💧 Nueva alícuota</div><div class="ms-step">📉 Factor acumulado</div></div>
        """,unsafe_allow_html=True)

    elif level==7:
        st.markdown("""
        <div class="master-scene">
          <div class="ms-title">🧪 Cuadrado de Pearson · Mezcla de concentraciones</div>
          <div class="ms-sub">Dos soluciones de distinta concentración se combinan en proporciones calculadas para alcanzar un objetivo.</div>
          <div class="ms-station" style="left:4%;width:140px"><div class="ms-cap">ALTA</div><div class="stock31"><div class="vliquid"></div></div></div>
          <div class="ms-station" style="left:24%;width:140px"><div class="ms-cap">BAJA</div><div class="stock31"><div class="vliquid green"></div></div></div>
          <div class="pearsonX" style="left:37%;top:240px;transform:rotate(18deg)"></div>
          <div class="pearsonX" style="left:37%;top:290px;transform:rotate(-18deg);background:#4fa888"></div>
          <div class="target-circle" style="right:18%;top:215px"></div>
          <div class="stir2" style="right:22%;top:250px">↻</div>
          <div class="vlabel" style="right:13%;bottom:105px">CONCENTRACIÓN OBJETIVO</div>
        </div>
        <div class="ms-process"><div class="ms-step">⬆️ Concentración alta</div><div class="ms-step">⬇️ Concentración baja</div><div class="ms-step">✖️ Diferencias diagonales</div><div class="ms-step">📐 Proporción</div><div class="ms-step">🧪 Convertir a volumen</div><div class="ms-step">✅ Verificar</div></div>
        """,unsafe_allow_html=True)

    elif level==8:
        st.markdown("""
        <div class="master-scene">
          <div class="ms-title">🧪 Corrección por pureza</div>
          <div class="ms-sub">La masa calculada debe corregirse cuando el reactivo comercial no es 100 % puro.</div>
          <div class="checkcard" style="left:6%;top:220px">MASA PURA<br>REQUERIDA</div>
          <div class="ms-arrow" style="left:29%">➜</div>
          <div class="checkcard" style="left:42%;top:220px">÷ FRACCIÓN<br>DE PUREZA</div>
          <div class="ms-arrow" style="left:64%">➜</div>
          <div class="balance3" style="right:7%;bottom:90px"></div>
          <div class="vlabel" style="right:4%;bottom:245px">MASA REAL A PESAR</div>
        </div>
        <div class="ms-process"><div class="ms-step">📄 Revisar pureza</div><div class="ms-step">🧮 Convertir % a fracción</div><div class="ms-step">➗ Corregir masa</div><div class="ms-step">⚖️ Pesar</div><div class="ms-step">🧾 Registrar</div><div class="ms-step">✅ Verificar</div></div>
        """,unsafe_allow_html=True)

    elif level in (9,10):
        st.markdown("""
        <div class="master-scene">
          <div class="ms-title">🧪 Control final de preparación</div>
          <div class="ms-sub">Una solución correcta exige cálculo, técnica, verificación y documentación.</div>
          <div class="ms-station" style="left:7%;width:170px"><div class="ms-cap">PREPARAR</div><div class="flask31"><div class="flaskliq"></div></div></div>
          <div class="ms-arrow" style="left:31%">➜</div>
          <div class="checkcard" style="left:43%;top:220px">✓ CONCENTRACIÓN<br>✓ VOLUMEN FINAL<br>✓ UNIDADES<br>✓ HOMOGENEIDAD</div>
          <div class="ms-arrow" style="left:67%">➜</div>
          <div class="labelbottle" style="position:absolute;right:8%;bottom:95px"></div>
        </div>
        <div class="ms-process"><div class="ms-step">🧮 Calcular</div><div class="ms-step">🧪 Preparar</div><div class="ms-step">✅ Verificar</div><div class="ms-step">🔄 Homogeneizar</div><div class="ms-step">🏷️ Rotular</div><div class="ms-step">🧠 Interpretar</div></div>
        """,unsafe_allow_html=True)

def virtual_lab_intro(level):
    if level not in (2,3,4):
        return

    if level==2:
        html="""<div class="virtual-lab">
        <div class="vtitle">🧪 Laboratorio virtual · % p/v</div>
        <div class="vsubtitle">Pesar el soluto, disolver, transferir al matraz y aforar hasta el volumen final.</div>
        <div class="balance3" style="left:6%"></div>
        <div class="vlabel" style="left:5%;bottom:290px">1 · BALANZA</div>
        <div class="beaker" style="left:34%"><div class="vliquid"></div></div>
        <div class="vlabel" style="left:32%;bottom:290px">2 · DISOLVER</div>
        <div class="volflask" style="right:14%"><div class="vliquid green"></div></div>
        <div class="vlabel" style="right:9%;bottom:315px">3 · MATRAZ VOLUMÉTRICO</div>
        <div class="vbench"></div></div>"""
    elif level==3:
        html="""<div class="virtual-lab">
        <div class="vtitle">🧪 Laboratorio virtual · % v/v</div>
        <div class="vsubtitle">Medir el componente líquido y completar hasta el volumen final en material volumétrico.</div>
        <div class="graduated" style="left:8%"><div class="vliquid orange"></div></div>
        <div class="vlabel" style="left:5%;bottom:330px">1 · PROBETA / PIPETA</div>
        <div class="micropip" style="left:29%;top:190px"></div>
        <div class="volflask" style="right:15%"><div class="vliquid green"></div></div>
        <div class="vlabel" style="right:10%;bottom:315px">2 · COMPLETAR HASTA AFORO</div>
        <div class="vbench"></div></div>"""
    else:
        html="""<div class="virtual-lab">
        <div class="vtitle">🧪 Laboratorio virtual · Dilución desde solución madre</div>
        <div class="vsubtitle">Identificar C₁, tomar V₁ con material adecuado y completar hasta V₂.</div>
        <div class="stockbottle" style="left:6%"><div class="vliquid"></div></div>
        <div class="vlabel" style="left:4%;bottom:300px">SOLUCIÓN MADRE</div>
        <div class="micropip" style="left:28%;top:185px"></div>
        <div class="vlabel" style="left:34%;bottom:310px">TOMAR V₁</div>
        <div class="volflask" style="right:14%"><div class="vliquid green"></div></div>
        <div class="vlabel" style="right:8%;bottom:315px">COMPLETAR HASTA V₂</div>
        <div class="vbench"></div></div>"""
    st.markdown(html,unsafe_allow_html=True)

def material_selector(level):
    st.subheader("🧰 Selección de material")
    materials=["Balanza","Vaso de precipitados","Probeta","Pipeta","Matraz volumétrico"]
    icons={"Balanza":"⚖️","Vaso de precipitados":"🥛","Probeta":"🧪","Pipeta":"💧","Matraz volumétrico":"⚗️"}
    cols=st.columns(len(materials))
    for c,m in zip(cols,materials):
        c.markdown(f'<div class="material-card">{icons[m]}<b>{m}</b></div>',unsafe_allow_html=True)

    if level==2:
        expected={"Balanza","Vaso de precipitados","Matraz volumétrico"}
        prompt="Seleccione el material mínimo apropiado para pesar, disolver y ajustar el volumen final."
    elif level==3:
        expected={"Pipeta","Matraz volumétrico"}
        prompt="Seleccione el material apropiado para medir el componente líquido y ajustar el volumen final."
    else:
        expected={"Pipeta","Matraz volumétrico"}
        prompt="Seleccione el material apropiado para tomar V₁ y preparar el volumen final V₂."

    selected=st.multiselect(prompt,materials,key=f"materials_{level}")
    correct=set(selected)==expected
    if selected:
        if correct:
            st.success("✅ Selección de material adecuada.")
        else:
            st.info("💡 Revise si necesita medir masa, tomar una alícuota o ajustar un volumen final.")
    return correct

def interactive_steps(level):
    st.subheader("🕹️ Simulación paso a paso")
    if level==2:
        steps=["Pesar el soluto","Disolver en parte del solvente","Transferir al matraz volumétrico","Completar hasta el aforo","Homogeneizar y rotular"]
    elif level==3:
        steps=["Medir el componente líquido","Transferir al material volumétrico","Completar hasta el volumen final","Homogeneizar y rotular"]
    else:
        steps=["Identificar C₁, C₂ y V₂","Calcular V₁","Tomar V₁ con pipeta","Transferir al matraz","Completar hasta V₂","Homogeneizar y rotular"]

    if f"vstep_{level}" not in st.session_state:
        st.session_state[f"vstep_{level}"]=0

    idx=st.session_state[f"vstep_{level}"]
    for i,s in enumerate(steps):
        cls="vstep done" if i<idx else "vstep"
        mark="✅" if i<idx else "○"
        st.markdown(f'<div class="{cls}"><b>{mark} Paso {i+1}</b> · {s}</div>',unsafe_allow_html=True)

    c1,c2=st.columns(2)
    if c1.button("Ejecutar siguiente paso",key=f"next_vstep_{level}",disabled=idx>=len(steps)):
        st.session_state[f"vstep_{level}"]=min(idx+1,len(steps))
        st.rerun()
    if c2.button("Reiniciar simulación",key=f"reset_vstep_{level}"):
        st.session_state[f"vstep_{level}"]=0
        st.rerun()

    return st.session_state[f"vstep_{level}"]>=len(steps)

def module_nav():
    st.subheader("🧭 Navegación por módulos")

    module_icons=["🧠","🧪","💧","⚗️","🐾"]

    with st.container(key="module_nav_container"):
        cols=st.columns(5)
        for col,(icon,(mod,levels)) in zip(cols,zip(module_icons,MODULES.items())):
            done=sum(1 for l in levels if st.session_state.solved.get(l))
            label=f"{icon}  {mod}  ·  {done}/{len(levels)} completadas"
            if col.button(label,use_container_width=True,key=f"module_btn_{levels[0]}"):
                st.session_state.level=levels[0]
                st.rerun()

    current=MOD_BY_LEVEL[st.session_state.level]
    st.caption(f"Módulo actual: **{current}**")

    roman=current.split("·")[0].strip()
    keymap={"I":"mission_nav_I","II":"mission_nav_II","III":"mission_nav_III","IV":"mission_nav_IV","V":"mission_nav_V"}
    container_key=keymap.get(roman,"mission_nav_I")

    with st.container(key=container_key):
        subcols=st.columns(len(MODULES[current]))
        for col,l in zip(subcols,MODULES[current]):
            state="✓" if st.session_state.solved.get(l) else "●" if st.session_state.level==l else "○"
            if col.button(
                f"{state} Misión {l} · {TITLES[l]}",
                use_container_width=True,
                key=f"go_{l}"
            ):
                st.session_state.level=l
                st.rerun()

def prev_next():
    a,b,_=st.columns([1,1,5])
    if a.button("← Anterior",disabled=st.session_state.level==1):
        goto(st.session_state.level-1)
    if b.button("Siguiente →",disabled=not st.session_state.solved.get(st.session_state.level) or st.session_state.level==TOTAL):
        goto(st.session_state.level+1)

if not st.session_state.started:
    st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 3.2</h1><p>Simulador veterinario de soluciones, diluciones y cálculos aplicados a Toxicología</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="route">INTERPRETAR → CALCULAR → PREPARAR → VERIFICAR → ROTULAR → CONTEXTO TOXICOLÓGICO</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,(m,ls) in zip(cols,MODULES.items()):
        c.markdown(f'<div class="modulebox"><b>{m}</b><br><span class="small">Misiones {", ".join(map(str,ls))}</span></div>',unsafe_allow_html=True)
    st.info("Los escenarios son educativos y están orientados a medicina veterinaria y toxicología. No constituyen protocolos terapéuticos ni sustituyen evaluación clínica, fichas técnicas o normativa institucional.")
    name=st.text_input("Nombre del estudiante o equipo")
    if st.button("Entrar al laboratorio",type="primary",use_container_width=True):
        if name.strip():
            st.session_state.name=name.strip()
            st.session_state.started=True
            st.rerun()
        else:
            st.warning("Escriba un nombre.")
    st.stop()

st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 3.2</h1><p>Laboratorio virtual veterinario de preparación aplicada a Toxicología</p></div>',unsafe_allow_html=True)
c1,c2,c3=st.columns([5,1,1])
c1.progress(st.session_state.level/TOTAL,text=f"Misión {st.session_state.level}/{TOTAL}")
c2.metric("Puntaje",f"{st.session_state.score}/100")
c3.button("Reiniciar",on_click=reset)
module_nav()
L=st.session_state.level
st.markdown(f'<span class="badge">{MOD_BY_LEVEL[L]}</span>',unsafe_allow_html=True)
st.header(f"Misión {L} · {TITLES[L]}")
lab_animation(L)
calc_guide(L)
if L==1:
    unit_converter()
if L==2:
    mission2_master_scene()
    material_ok=material_selector(L)
    simulation_ok=interactive_steps(L)
elif L in (3,4):
    master_scene(L)
    material_ok=material_selector(L)
    simulation_ok=interactive_steps(L)
elif L>=5:
    master_scene(L)
    material_ok=True
    simulation_ok=True
else:
    material_ok=True
    simulation_ok=True

if L==1:
    mission("En un laboratorio veterinario debe preparar una solución de trabajo. Antes de pesar o pipetear, convierta correctamente 2,5 g a mg y 750 µL a mL. Use el convertidor para practicar con otros valores.")
    a=st.number_input("2,5 g = ¿mg?",0.0,step=100.0,key="1a")
    b=st.number_input("750 µL = ¿mL?",0.0,step=.05,key="1b")
    if st.button("Comprobar",key="b1"):
        submit(1,math.isclose(a,2500) and math.isclose(b,.75),"2,5 g = **2500 mg** y 750 µL = **0,75 mL**.","Use 1000 mg = 1 g y 1000 µL = 1 mL.")
    feedback(1); key("Una conversión incorrecta puede invalidar toda la preparación."); prev_next()

elif L==2:
    mission("En una práctica de toxicología clínica veterinaria se solicita preparar 250 mL de NaCl al 7,5 % p/v como ejemplo de una solución hipertónica. Calcule la masa requerida y seleccione el procedimiento correcto.")
    concept(["% p/v","Solución hipertónica","Volumen final"])
    st.markdown('<div class="formula">7,5 % p/v = 7,5 g / 100 mL de solución final</div>',unsafe_allow_html=True)
    a=st.number_input("Masa de NaCl (g)",0.0,step=.25,key="2a")
    p=st.radio("Procedimiento:",["Agregar 250 mL de agua al soluto.","Disolver en un volumen menor y completar hasta 250 mL de solución final."],index=None,key="2b")
    if st.button("Comprobar",key="b2",disabled=not (material_ok and simulation_ok)):
        submit(2,math.isclose(a,18.75,abs_tol=.01) and p and p.startswith("Disolver"),"Se requieren **18,75 g**; el volumen debe ajustarse hasta 250 mL de solución final.","Use 7,5/100 × 250 y recuerde que % p/v usa volumen final.")
    feedback(2); key("% p/v se refiere al volumen final, no al volumen de solvente añadido."); prev_next()

elif L==3:
    mission("En un servicio veterinario se requiere preparar 200 mL de una solución líquida al 25 % v/v para una práctica de formulación. Calcule el volumen del componente líquido y elija el procedimiento conceptual correcto.")
    concept(["% v/v","Volumen final"])
    a=st.number_input("Volumen del componente líquido (mL)",0.0,step=1.0,key="3a")
    p=st.radio("Procedimiento:",["Tomar el volumen calculado y completar hasta 200 mL finales.","Añadir 200 mL de solvente al volumen calculado."],index=None,key="3b")
    if st.button("Comprobar",key="b3",disabled=not (material_ok and simulation_ok)):
        submit(3,math.isclose(a,50) and p and p.startswith("Tomar"),"25 % de 200 mL = **50 mL**; se completa hasta 200 mL finales.","25/100 × 200.")
    feedback(3); key("En % v/v el denominador corresponde al volumen final de la preparación."); prev_next()

elif L==4:
    mission("En una práctica de toxicología veterinaria se dispone de azul de metileno al 1 % p/v (**10 mg/mL**) y se requiere preparar 100 mL al 0,1 % p/v (**1 mg/mL**). Calcule el volumen de solución madre.")
    concept(["C₁V₁=C₂V₂","Azul de metileno","Volumen final"])
    st.markdown('<div class="formula"><b>Solución madre:</b> 1 % p/v = 10 mg/mL &nbsp; → &nbsp; <b>Objetivo:</b> 0,1 % p/v = 1 mg/mL &nbsp; | &nbsp; V₂ = 100 mL</div>',unsafe_allow_html=True)
    check=st.number_input("Antes de diluir: 1 % p/v equivale a ¿mg/mL?",0.0,step=1.0,key="4c")
    a=st.number_input("V₁ de solución madre (mL)",0.0,step=1.0,key="4a")
    p=st.radio("Luego:",["Agregar 100 mL de diluyente.","Completar la preparación hasta un volumen final de 100 mL."],index=None,key="4b")
    if st.button("Comprobar",key="b4",disabled=not (material_ok and simulation_ok)):
        submit(4,math.isclose(check,10) and math.isclose(a,10) and p and p.startswith("Completar"),"1 % = **10 mg/mL**. V₁=(0,1×100)/1 = **10 mL**; luego se completa hasta 100 mL finales.","Primero convierta 1 % p/v a mg/mL. Después use C₁V₁=C₂V₂.")
    feedback(4); key("La misma dilución puede expresarse como 1 % → 0,1 % o 10 mg/mL → 1 mg/mL."); prev_next()

elif L==5:
    mission("Antes de calcular un volumen administrable o preparar una dilución, un estudiante debe convertir las concentraciones de azul de metileno de % p/v a mg/mL.")
    concept(["% p/v","mg/mL"])
    st.markdown('<div class="formula">1 % p/v = 1 g/100 mL → 1000 mg/100 mL → 10 mg/mL</div>',unsafe_allow_html=True)
    g1=st.number_input("Paso 1: 1 g = ¿mg?",0.0,step=100.0,key="5g")
    a=st.number_input("1 % p/v = ¿mg/mL?",0.0,step=1.0,key="5a")
    b=st.number_input("0,1 % p/v = ¿mg/mL?",0.0,step=.1,key="5b")
    if st.button("Comprobar",key="b5"):
        submit(5,math.isclose(g1,1000) and math.isclose(a,10) and math.isclose(b,1),"1 g = **1000 mg**; 1 % = **10 mg/mL** y 0,1 % = **1 mg/mL**.","Recuerde que % p/v significa g/100 mL y que 1 g = 1000 mg.")
    feedback(5); key("Regla útil: para soluciones expresadas como % p/v, multiplicar el porcentaje por 10 da mg/mL."); prev_next()

elif L==6:
    mission("Una muestra veterinaria contiene un analito a 1000 µg/mL. Para llevarla al intervalo de trabajo del método se realizan dos diluciones consecutivas 1:10: primero se toma 1 mL y se completa hasta 10 mL; luego se toma 1 mL de esa dilución y nuevamente se completa hasta 10 mL.")
    concept(["Dilución seriada","Factor de dilución","Volumen final"])
    st.markdown('<div class="formula">1000 µg/mL → 1ª dilución 1:10 → ? → 2ª dilución 1:10 → ?</div>',unsafe_allow_html=True)
    c1=st.number_input("Concentración después de la primera dilución (µg/mL)",0.0,step=10.0,key="6a")
    c2=st.number_input("Concentración después de la segunda dilución (µg/mL)",0.0,step=1.0,key="6b")
    fd=st.radio("Factor de dilución acumulado respecto a la muestra original:",["1:10","1:20","1:100","1:1000"],index=None,key="6c")
    why=st.radio("¿Por qué puede ser útil diluir una muestra en toxicología analítica?",["Para llevar la concentración al intervalo de trabajo del método.","Porque toda muestra debe diluirse obligatoriamente.","Para eliminar químicamente el tóxico."],index=None,key="6d")
    if st.button("Comprobar",key="b6"):
        ok=math.isclose(c1,100) and math.isclose(c2,10) and fd=="1:100" and why=="Para llevar la concentración al intervalo de trabajo del método."
        submit(6,ok,"Primera dilución: **100 µg/mL**. Segunda: **10 µg/mL**. Factor acumulado: **1:100**.","Cada etapa divide la concentración por 10; los factores sucesivos se multiplican.")
    feedback(6); key("Una dilución 1:10 en este ejercicio significa 1 parte de muestra llevada a 10 partes de volumen final."); prev_next()

elif L==7:
    mission("Seleccione un escenario de fluidoterapia veterinaria para aplicar el cuadrado de Pearson. El objetivo es comprender cómo ajustar una concentración, no establecer un protocolo terapéutico.")

    concept(["Cuadrado de Pearson","Solución hipertónica","Volumen final"])

    mode=st.radio(
        "¿Qué desea preparar?",
        [
            "🔵 Escenario A · Disminuir NaCl 0,9 % hasta 0,7 % (ejercicio de solución hipotónica)",
            "🔴 Escenario B · Obtener NaCl 7,5 % mezclando NaCl 20 % y NaCl 0,9 % (ejercicio de solución hipertónica)"
        ],
        index=None,
        key="7mode"
    )

    if mode:
        if mode.startswith("🔵"):
            high, low, target, total = 0.9, 0.0, 0.7, 300.0
            high_name="NaCl 0,9 %"
            low_name="Diluyente 0 % NaCl"
            final_name="NaCl 0,7 %"
            expected_hi_parts=0.7
            expected_lo_parts=0.2
            expected_hi_vol=233.33
            expected_lo_vol=66.67
            physiol="Hipotónica respecto a NaCl 0,9 %"
            note="Para fines aritméticos, el diluyente se representa como 0 % NaCl. Este escenario es educativo y no indica que deba administrarse agua estéril por vía intravenosa."
        else:
            high, low, target, total = 20.0, 0.9, 7.5, 500.0
            high_name="NaCl 20 %"
            low_name="NaCl 0,9 %"
            final_name="NaCl 7,5 %"
            expected_hi_parts=6.6
            expected_lo_parts=12.5
            expected_hi_vol=172.77
            expected_lo_vol=327.23
            physiol="Hipertónica respecto a NaCl 0,9 %"
            note="El ejercicio utiliza concentraciones habituales como referencia académica. La preparación y uso clínico reales dependen de productos autorizados, protocolos, especie y estado del paciente."

        st.info(note)

        st.markdown(f"""
        <div class="pearson-wrap">
          <div class="pearson-title">🎬 Cuadrado de Pearson · Construcción visual</div>
          <div class="pearson-grid">
            <div class="pearson-box"><span>Concentración alta</span><strong>{high:g} %</strong><span>{high_name}</span></div>
            <div class="arrowbig">↘</div>
            <div class="pearson-box"><span>Diferencia diagonal</span><strong>|{target:g} − {low:g}|</strong><span>partes de la solución alta</span></div>

            <div class="arrowbig">↗</div>
            <div class="pearson-center"><span>Objetivo</span><strong>{target:g} %</strong><span>{final_name}</span></div>
            <div class="arrowbig">↘</div>

            <div class="pearson-box"><span>Concentración baja</span><strong>{low:g} %</strong><span>{low_name}</span></div>
            <div class="arrowbig">↗</div>
            <div class="pearson-box"><span>Diferencia diagonal</span><strong>|{high:g} − {target:g}|</strong><span>partes de la solución baja</span></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶ Reproducir Pearson paso a paso", key="pearson_anim"):
            ph=st.empty()
            steps=[
                f"1. Coloque la concentración alta: {high:g} %.",
                f"2. Coloque la concentración objetivo en el centro: {target:g} %.",
                f"3. Coloque la concentración baja: {low:g} %.",
                f"4. Reste diagonalmente en valor absoluto: |{target:g} − {low:g}| = {expected_hi_parts:g}.",
                f"5. Reste la otra diagonal: |{high:g} − {target:g}| = {expected_lo_parts:g}.",
                f"6. La proporción es {expected_hi_parts:g} partes de {high_name} por {expected_lo_parts:g} partes de {low_name}.",
                f"7. Convierta esa proporción al volumen final requerido: {total:g} mL."
            ]
            for s in steps:
                ph.info(s)
                time.sleep(.65)
            ph.success("Animación completada. Ahora construya usted el resultado.")

        st.subheader("Paso 1 · Construya el cuadrado")
        c1,c2=st.columns(2)
        hi_parts=c1.number_input(f"Partes de {high_name}",min_value=0.0,step=.1,key="7a")
        lo_parts=c2.number_input(f"Partes de {low_name}",min_value=0.0,step=.1,key="7b")

        st.subheader("Paso 2 · Convierta las partes a volumen")
        st.caption(f"Volumen final requerido: {total:g} mL")
        c3,c4=st.columns(2)
        vhi=c3.number_input(f"Volumen de {high_name} (mL)",min_value=0.0,step=1.0,key="7c")
        vlo=c4.number_input(f"Volumen de {low_name} (mL)",min_value=0.0,step=1.0,key="7d")

        st.subheader("Paso 3 · Verifique e interprete")
        verify=st.number_input("Concentración final calculada (%)",min_value=0.0,step=.1,key="7e")
        interpretation=st.radio(
            "Respecto a NaCl 0,9 %, la preparación final se clasifica en este ejercicio como:",
            ["Hipotónica","Isotónica","Hipertónica"],
            index=None,
            key="7f"
        )

        correct_interp="Hipotónica" if target<0.9 else "Hipertónica" if target>0.9 else "Isotónica"

        if st.button("Comprobar",key="b7"):
            ok=(
                math.isclose(hi_parts,expected_hi_parts,abs_tol=.05) and
                math.isclose(lo_parts,expected_lo_parts,abs_tol=.05) and
                math.isclose(vhi,expected_hi_vol,abs_tol=.6) and
                math.isclose(vlo,expected_lo_vol,abs_tol=.6) and
                math.isclose(verify,target,abs_tol=.05) and
                interpretation==correct_interp
            )
            if mode.startswith("🔵"):
                good=f"Pearson: **0,7 partes de NaCl 0,9 % + 0,2 partes de diluyente**. Para 300 mL: aproximadamente **233,3 mL + 66,7 mL**. La preparación final es **hipotónica** respecto a NaCl 0,9 %."
                hint="Calcule |0,7−0| y |0,9−0,7|. Luego reparta 300 mL según 0,7:0,2."
            else:
                good=f"Pearson: **6,6 partes de NaCl 20 % + 12,5 partes de NaCl 0,9 %**. Para 500 mL: aproximadamente **172,8 mL + 327,2 mL**. La preparación final es **hipertónica** respecto a NaCl 0,9 %."
                hint="Calcule |7,5−0,9| y |20−7,5|. Luego reparta 500 mL según 6,6:12,5."
            submit(7,ok,good,hint)

        feedback(7)

        if st.session_state.solved.get(7):
            st.markdown(f'<div class="resultbig">Resultado verificado: {final_name} · {physiol}</div>',unsafe_allow_html=True)

        key("El cuadrado de Pearson primero determina una proporción. Después esa proporción se transforma en volúmenes y finalmente se verifica la concentración obtenida.")
    else:
        st.info("Seleccione uno de los dos escenarios para comenzar.")

    prev_next()

elif L==8:
    mission("Para preparar un reactivo de laboratorio veterinario se requieren 10 g de compuesto puro, pero el reactivo comercial tiene 80 % de pureza. Calcule la masa que debe pesarse.")
    concept(["Pureza"])
    a=st.number_input("Masa a pesar (g)",0.0,step=.1,key="8a")
    if st.button("Comprobar",key="b8"):
        submit(8,math.isclose(a,12.5,abs_tol=.01),"10/0,80 = **12,5 g**.","Divida la masa pura requerida entre la fracción de pureza.")
    feedback(8); key("La pureza declarada puede requerir corrección de la masa pesada."); prev_next()

elif L==9:
    mission("Un interno escribe en la bitácora: «Para preparar 500 mL al 5 % p/v, peso 25 g del soluto y agrego 500 mL de agua». Evalúe el procedimiento.")
    concept(["% p/v","Volumen final","Rotulado"])
    a=st.radio("Seleccione:",["Todo es correcto.","La masa es correcta, pero debe completar hasta 500 mL de solución final.","La masa correcta es 5 g.","El único error es no indicar la especie del paciente."],index=None,key="9a")
    if st.button("Comprobar",key="b9"):
        submit(9,a and a.startswith("La masa es correcta"),"**25 g** es correcto; el error consiste en confundir volumen de solvente con volumen final de solución.","Calcule 5 g/100 mL × 500 mL y revise qué representa el volumen del denominador.")
    feedback(9); key("Un resultado numérico correcto no garantiza un procedimiento de preparación correcto."); prev_next()

elif L==10:
    mission("CÓDIGO TÓXICO: llega una muestra de un perro con sospecha de exposición a un tóxico. Para el procedimiento analítico se necesita preparar 250 mL de una solución de trabajo al 0,2 % p/v a partir de una solución madre al 2 % p/v. Calcule, prepare y verifique.")
    concept(["C₁V₁=C₂V₂","% p/v","mg/mL","Rotulado","Volumen final"])
    st.markdown('<div class="formula">C₁ = 2 % &nbsp; | &nbsp; C₂ = 0,2 % &nbsp; | &nbsp; V₂ = 250 mL</div>',unsafe_allow_html=True)
    v=st.number_input("Volumen de solución madre (mL)",0.0,step=1.0,key="10a")
    seq=st.radio("Secuencia:",["Tomar 25 mL de la madre → completar hasta 250 mL → homogeneizar → rotular.","Tomar 25 mL → agregar 250 mL de diluyente → usar sin rotular.","Tomar 250 mL de la madre → agregar 25 mL de diluyente."],index=None,key="10b")
    c=st.number_input("Concentración final expresada en mg/mL",0.0,step=.1,key="10c")
    label=st.multiselect("Seleccione los elementos básicos del rótulo:",["Nombre de la solución","Concentración","Fecha/preparador","Color del paciente","Condiciones/información adicional según protocolo"],key="10d")
    if st.button("Finalizar estación",key="b10"):
        ok=math.isclose(v,25) and seq and seq.startswith("Tomar 25 mL de la madre") and math.isclose(c,2) and all(x in label for x in ["Nombre de la solución","Concentración","Fecha/preparador"])
        submit(10,ok,"V₁ = **25 mL**; 0,2 % p/v = **2 mg/mL**. La preparación se completa hasta 250 mL, se homogeneiza y se rotula adecuadamente.","Use C₁V₁=C₂V₂, convierta 0,2 g/100 mL a mg/mL y revise el rotulado.")
    feedback(10); key("La competencia final integra cálculo, procedimiento, verificación de unidades, rotulado y contexto veterinario.")
    if st.session_state.solved.get(10):
        st.divider()
        st.subheader("🏁 Perfil final")
        st.metric("Puntaje global",f"{st.session_state.score}/100")
        first=sum(1 for x in range(1,11) if st.session_state.attempts.get(x)==1)
        st.metric("Misiones al primer intento",f"{first}/10")
        if st.session_state.score>=85: st.success("Desempeño sólido en preparación y cálculos aplicados.")
        elif st.session_state.score>=70: st.info("Buen desempeño. Revise las misiones que requirieron más de un intento.")
        else: st.warning("Conviene reforzar conversiones, porcentajes, diluciones y volumen final.")
        st.button("Repetir laboratorio",on_click=reset,type="primary")

st.divider()
st.caption("TOX-PREP 3.2 · Recurso educativo para medicina veterinaria y toxicología. No sustituye protocolos clínicos, fichas técnicas, evaluación del paciente ni normativa institucional.")
