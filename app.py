import math
import time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="TOX-PREP 2.4", page_icon="⚗️", layout="wide")

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
        html="""<div class="convstage">
        <div class="convtitle">🎬 Conversión visual de unidades</div>
        <div class="scale-row">
          <div class="scale-unit">µg</div><div class="scale-unit">mg</div><div class="scale-unit active">g</div>
          <div class="scale-unit">kg</div><div class="scale-unit">µL</div><div class="scale-unit">mL</div><div class="scale-unit">L</div>
        </div>
        <div class="conv-arrow"></div><div class="conv-marker"></div>
        <div class="conv-label">La masa y el volumen se convierten por separado. Observe el desplazamiento entre órdenes de magnitud y verifique siempre la unidad final.</div>
        <div class="conv-lab"></div>
        <div class="conv-badge" style="left:7%;bottom:160px">MASA · µg ↔ mg ↔ g ↔ kg</div>
        <div class="conv-beaker"></div>
        <div class="conv-badge" style="right:6%;bottom:175px">VOLUMEN · µL ↔ mL ↔ L</div>
        </div>"""
    elif level==2:
        html='''<div class="labstage"><div class="labtitle">🎬 Preparación % p/v</div>
        <div class="balance" style="left:6%"></div><div class="labeltag" style="left:5%;bottom:180px">1 · PESAR</div>
        <div class="arrowmove" style="left:29%;bottom:120px">➜</div>
        <div class="flask" style="left:43%"><div class="liquid"></div></div>
        <div class="drop" style="left:49%"></div><div class="labeltag" style="left:41%;bottom:220px">2 · DISOLVER</div>
        <div class="arrowmove" style="left:62%;bottom:120px">➜</div>
        <div class="flask" style="right:8%"><div class="liquid green"></div></div>
        <div class="labeltag" style="right:5%;bottom:220px">3 · AFORAR + ROTULAR</div><div class="bench"></div></div>'''
    elif level==3:
        html='''<div class="labstage"><div class="labtitle">🎬 Preparación % v/v</div>
        <div class="pipette" style="left:7%;top:130px"></div><div class="labeltag" style="left:8%;bottom:100px">MEDIR VOLUMEN</div>
        <div class="arrowmove" style="left:37%;bottom:125px">➜</div>
        <div class="flask" style="left:49%"><div class="liquid orange"></div></div><div class="drop" style="left:55%"></div>
        <div class="arrowmove" style="left:68%;bottom:125px">➜</div><div class="labeltag" style="right:4%;bottom:115px;font-size:1.15rem">COMPLETAR<br>VOLUMEN FINAL</div><div class="bench"></div></div>'''
    elif level in (4,5):
        html='''<div class="labstage"><div class="labtitle">🎬 Dilución desde solución madre</div>
        <div class="flask" style="left:7%"><div class="liquid"></div></div><div class="labeltag" style="left:5%;bottom:220px">SOLUCIÓN MADRE</div>
        <div class="pipette" style="left:29%;top:135px"></div><div class="arrowmove" style="left:51%;bottom:125px">➜</div>
        <div class="flask" style="right:14%"><div class="liquid green"></div></div><div class="drop" style="right:18%"></div>
        <div class="labeltag" style="right:8%;bottom:220px">SOLUCIÓN DILUIDA</div><div class="stir" style="right:17%;bottom:105px">↻</div><div class="bench"></div></div>'''
    elif level==6:
        html='''<div class="labstage"><div class="labtitle">🎬 Dilución seriada</div>
        <div class="flask" style="left:5%;width:85px;height:115px"><div class="liquid"></div></div>
        <div class="arrowmove" style="left:23%;bottom:110px">➜</div><div class="flask" style="left:38%;width:85px;height:115px"><div class="liquid green"></div></div>
        <div class="arrowmove" style="left:56%;bottom:110px">➜</div><div class="flask" style="right:15%;width:85px;height:115px"><div class="liquid orange"></div></div>
        <div class="labeltag" style="left:3%;bottom:200px">MUESTRA</div><div class="labeltag" style="left:35%;bottom:200px">1ª DILUCIÓN</div>
        <div class="labeltag" style="right:10%;bottom:200px">2ª DILUCIÓN</div><div class="bench"></div></div>'''
    elif level==7:
        html='''<div class="labstage"><div class="labtitle">🎬 Pearson: dos concentraciones convergen en un objetivo</div>
        <div class="flask" style="left:7%"><div class="liquid"></div></div><div class="labeltag" style="left:4%;bottom:220px">CONCENTRACIÓN ALTA</div>
        <div class="flask" style="left:31%"><div class="liquid green"></div></div><div class="labeltag" style="left:29%;bottom:220px">CONCENTRACIÓN BAJA</div>
        <div class="arrowmove" style="left:53%;bottom:125px">➜</div><div class="flask" style="right:12%;width:135px;height:165px"><div class="liquid orange"></div></div>
        <div class="labeltag" style="right:7%;bottom:245px">CONCENTRACIÓN OBJETIVO</div><div class="stir" style="right:17%;bottom:105px">↻</div><div class="bench"></div></div>'''
    elif level==8:
        html='''<div class="labstage"><div class="labtitle">🎬 Corrección por pureza antes de pesar</div>
        <div class="labeltag" style="left:8%;bottom:180px;font-size:1.25rem">MASA PURA<br>REQUERIDA</div>
        <div class="arrowmove" style="left:36%;bottom:130px">➜</div><div class="labeltag" style="left:48%;bottom:175px;font-size:1.2rem">÷ FRACCIÓN<br>DE PUREZA</div>
        <div class="arrowmove" style="left:68%;bottom:130px">➜</div><div class="balance" style="right:7%"></div><div class="bench"></div></div>'''
    else:
        html='''<div class="labstage"><div class="labtitle">🎬 Verificar antes de usar</div>
        <div class="flask" style="left:8%"><div class="liquid green"></div></div><div class="labeltag" style="left:5%;bottom:220px">PREPARAR</div>
        <div class="arrowmove" style="left:34%;bottom:125px">➜</div><div class="labeltag" style="left:46%;bottom:165px;font-size:1.2rem">✓ CÁLCULO<br>✓ VOLUMEN<br>✓ UNIDADES</div>
        <div class="arrowmove" style="left:66%;bottom:125px">➜</div><div class="labeltag" style="right:6%;bottom:150px;font-size:1.2rem">🏷 ROTULAR</div><div class="bench"></div></div>'''
    st.markdown(html,unsafe_allow_html=True)

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
    st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 2.4</h1><p>Simulador veterinario de soluciones, diluciones y cálculos aplicados a Toxicología</p></div>',unsafe_allow_html=True)
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

st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 2.4</h1><p>Laboratorio virtual veterinario de preparación aplicada a Toxicología</p></div>',unsafe_allow_html=True)
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
    if st.button("Comprobar",key="b2"):
        submit(2,math.isclose(a,18.75,abs_tol=.01) and p and p.startswith("Disolver"),"Se requieren **18,75 g**; el volumen debe ajustarse hasta 250 mL de solución final.","Use 7,5/100 × 250 y recuerde que % p/v usa volumen final.")
    feedback(2); key("% p/v se refiere al volumen final, no al volumen de solvente añadido."); prev_next()

elif L==3:
    mission("En un servicio veterinario se requiere preparar 200 mL de una solución líquida al 25 % v/v para una práctica de formulación. Calcule el volumen del componente líquido y elija el procedimiento conceptual correcto.")
    concept(["% v/v","Volumen final"])
    a=st.number_input("Volumen del componente líquido (mL)",0.0,step=1.0,key="3a")
    p=st.radio("Procedimiento:",["Tomar el volumen calculado y completar hasta 200 mL finales.","Añadir 200 mL de solvente al volumen calculado."],index=None,key="3b")
    if st.button("Comprobar",key="b3"):
        submit(3,math.isclose(a,50) and p and p.startswith("Tomar"),"25 % de 200 mL = **50 mL**; se completa hasta 200 mL finales.","25/100 × 200.")
    feedback(3); key("En % v/v el denominador corresponde al volumen final de la preparación."); prev_next()

elif L==4:
    mission("En una práctica de toxicología veterinaria se dispone de azul de metileno al 1 % p/v (**10 mg/mL**) y se requiere preparar 100 mL al 0,1 % p/v (**1 mg/mL**). Calcule el volumen de solución madre.")
    concept(["C₁V₁=C₂V₂","Azul de metileno","Volumen final"])
    st.markdown('<div class="formula"><b>Solución madre:</b> 1 % p/v = 10 mg/mL &nbsp; → &nbsp; <b>Objetivo:</b> 0,1 % p/v = 1 mg/mL &nbsp; | &nbsp; V₂ = 100 mL</div>',unsafe_allow_html=True)
    check=st.number_input("Antes de diluir: 1 % p/v equivale a ¿mg/mL?",0.0,step=1.0,key="4c")
    a=st.number_input("V₁ de solución madre (mL)",0.0,step=1.0,key="4a")
    p=st.radio("Luego:",["Agregar 100 mL de diluyente.","Completar la preparación hasta un volumen final de 100 mL."],index=None,key="4b")
    if st.button("Comprobar",key="b4"):
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
st.caption("TOX-PREP 2.4 · Recurso educativo para medicina veterinaria y toxicología. No sustituye protocolos clínicos, fichas técnicas, evaluación del paciente ni normativa institucional.")
