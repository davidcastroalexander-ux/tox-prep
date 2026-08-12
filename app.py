import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="TOX-PREP",page_icon="⚗️",layout="wide")
st.markdown("""<style>
.block-container{max-width:1400px;padding-top:1.4rem}.hero{padding:1.4rem 1.7rem;border:1px solid #d8e3ef;border-radius:22px;background:linear-gradient(135deg,#fff,#f2f7fc)}.hero h1{color:#12315e;margin:0;font-size:2.6rem}.hero p{color:#52637b;margin:.3rem 0}.route{padding:1rem;margin:.9rem 0;border-radius:14px;background:#edf5fb;text-align:center;color:#173d6d;font-weight:800}.card{padding:1rem;border:1px solid #dde6ef;border-radius:14px;background:white;min-height:110px}.mission{padding:1rem;border:1px solid #dbe5ee;border-radius:14px;margin:.8rem 0}.formula{padding:.9rem;border:1px solid #dfe7ef;border-radius:12px;background:#f5f8fb;text-align:center;font-size:1.1rem}.key{padding:.9rem;border:1px solid #ead79e;border-radius:12px;background:#fffaf0;margin-top:.7rem}.badge{display:inline-block;background:#eaf2fb;color:#173e78;padding:.25rem .7rem;border-radius:999px;font-weight:800}</style>""",unsafe_allow_html=True)

DEFAULT={"started":False,"name":"","level":1,"score":0,"attempts":{},"solved":{},"feedback":{}}
for k,v in DEFAULT.items():
    if k not in st.session_state: st.session_state[k]=v.copy() if isinstance(v,dict) else v
TOTAL=10
TITLES={1:"Unidades antes de preparar",2:"% p/v · Solución hipertónica",3:"% v/v · Preparación volumétrica",4:"C₁V₁=C₂V₂ · Azul de metileno",5:"% ↔ mg/mL",6:"Diluciones seriadas",7:"Cuadrado de Pearson",8:"Corrección por pureza",9:"Encuentra el error",10:"Código Tóxico · Estación final"}
MOD={1:"I · Fundamentos",2:"II · Preparación",3:"II · Preparación",4:"III · Diluciones",5:"III · Diluciones",6:"III · Diluciones",7:"IV · Mezclas",8:"IV · Mezclas",9:"V · Procedimiento",10:"V · Integración"}
G={"% p/v":"Gramos de soluto contenidos en 100 mL de solución final.","% v/v":"Mililitros de un componente líquido contenidos en 100 mL de solución final.","C₁V₁=C₂V₂":"Relación de conservación para una dilución simple: concentración inicial × volumen tomado = concentración final × volumen final.","Factor de dilución":"Relación entre concentración inicial y final; en una dilución simple también puede expresarse mediante volumen final/alícuota.","Cuadrado de Pearson":"Método aritmético para obtener proporciones de dos preparaciones de concentraciones diferentes con las que se busca una concentración intermedia.","Pureza":"Fracción del reactivo comercial que corresponde al compuesto de interés.","Rotulado":"Identificación de la preparación con nombre, concentración y demás información requerida por el contexto.","Azul de metileno":"Agente con aplicaciones toxicológicas específicas y también riesgos y contraindicaciones. Aquí se usa para practicar cálculos de dilución, no como prescripción.","Solución hipertónica":"Solución con mayor tonicidad efectiva que el fluido de referencia. La concentración porcentual no sustituye la evaluación clínica de composición, tonicidad e indicación."}

def concept(ns):
    with st.expander("📚 Consultar concepto"):
        for n in ns: st.markdown(f"**{n}:** {G[n]}")
def submit(l,ok,good,hint):
    if st.session_state.solved.get(l): return
    a=st.session_state.attempts.get(l,0)+1; st.session_state.attempts[l]=a
    if ok:
        f=1 if a==1 else .7 if a==2 else .4; p=round(10*f)
        st.session_state.score+=p; st.session_state.solved[l]=True; st.session_state.feedback[l]=("ok",f"{good} **+{p} puntos.**")
    else: st.session_state.feedback[l]=("bad",hint)
def feedback(l):
    if l in st.session_state.feedback:
        k,t=st.session_state.feedback[l]; (st.success if k=="ok" else st.warning)(("✅ " if k=="ok" else "💡 ")+t)
def nav():
    a,b,_=st.columns([1,1,5])
    if a.button("← Anterior",disabled=st.session_state.level==1): st.session_state.level-=1; st.rerun()
    if b.button("Siguiente →",disabled=not st.session_state.solved.get(st.session_state.level) or st.session_state.level==TOTAL): st.session_state.level+=1; st.rerun()
def mission(t): st.markdown(f'<div class="mission"><b>🎯 Situación:</b> {t}</div>',unsafe_allow_html=True)
def key(t): st.markdown(f'<div class="key"><b>⭐ Idea clave:</b> {t}</div>',unsafe_allow_html=True)
def reset():
    for k,v in DEFAULT.items(): st.session_state[k]=v.copy() if isinstance(v,dict) else v
    st.rerun()

if not st.session_state.started:
    st.markdown('<div class="hero"><h1>⚗️ TOX-PREP</h1><p>Simulador de soluciones y diluciones aplicadas a Toxicología</p></div>',unsafe_allow_html=True)
    st.markdown('<div class="route">INTERPRETAR → CALCULAR → PREPARAR → VERIFICAR → ROTULAR → CONTEXTO TOXICOLÓGICO</div>',unsafe_allow_html=True)
    cols=st.columns(5)
    for c,x in zip(cols,[("I","Fundamentos"),("II","Preparación"),("III","Diluciones"),("IV","Mezclas"),("V","Integración")]): c.markdown(f'<div class="card"><b>Módulo {x[0]}</b><br><b>{x[1]}</b></div>',unsafe_allow_html=True)
    st.info("Escenarios **educativos**: las sustancias y concentraciones se emplean para enseñar cálculos y técnica de preparación, no como protocolos terapéuticos.")
    name=st.text_input("Nombre del estudiante o equipo")
    if st.button("Entrar al laboratorio",type="primary",use_container_width=True):
        if name.strip(): st.session_state.name=name.strip(); st.session_state.started=True; st.rerun()
        else: st.warning("Escriba un nombre.")
    st.stop()

st.markdown('<div class="hero"><h1>⚗️ TOX-PREP</h1><p>Laboratorio virtual de preparación aplicada a Toxicología</p></div>',unsafe_allow_html=True)
c1,c2,c3=st.columns([5,1,1]); c1.progress(st.session_state.level/TOTAL,text=f"Misión {st.session_state.level}/{TOTAL} · {MOD[st.session_state.level]}"); c2.metric("Puntaje",f"{st.session_state.score}/100"); c3.button("Reiniciar",on_click=reset)
L=st.session_state.level; st.markdown(f'<span class="badge">{MOD[L]}</span>',unsafe_allow_html=True); st.header(f"Misión {L} · {TITLES[L]}")

if L==1:
    mission("Convierta 2,5 g a mg y 750 µL a mL antes de iniciar una preparación.")
    a=st.number_input("2,5 g = ¿mg?",0.0,step=100.0); b=st.number_input("750 µL = ¿mL?",0.0,step=.05)
    if st.button("Comprobar"): submit(1,math.isclose(a,2500) and math.isclose(b,.75),"2,5 g = **2500 mg**; 750 µL = **0,75 mL**.","Use 1000 mg = 1 g y 1000 µL = 1 mL.")
    feedback(1); key("Una conversión incorrecta puede invalidar toda la preparación."); nav()
elif L==2:
    mission("Como ejercicio de formulación, prepare 250 mL de NaCl al 7,5 % p/v. Calcule la masa necesaria.")
    concept(["% p/v","Solución hipertónica"]); st.markdown('<div class="formula">7,5 % p/v = 7,5 g / 100 mL de solución final</div>',unsafe_allow_html=True)
    a=st.number_input("NaCl (g)",0.0,step=.25); p=st.radio("Procedimiento:",["Agregar exactamente 250 mL de agua.","Disolver y completar hasta 250 mL de solución final."],index=None)
    if st.button("Comprobar"): submit(2,math.isclose(a,18.75,abs_tol=.01) and p and p.startswith("Disolver"),"Se requieren **18,75 g** y se completa hasta 250 mL finales.","Use 7,5/100 × 250 y distinga solvente de volumen final.")
    feedback(2); key("% p/v utiliza el volumen final de la solución."); nav()
elif L==3:
    mission("Prepare 200 mL al 25 % v/v a partir de un componente líquido puro, como ejercicio volumétrico.")
    concept(["% v/v"]); a=st.number_input("Volumen del componente (mL)",0.0,step=1.0)
    p=st.radio("Procedimiento:",["Tomar el volumen calculado y completar hasta 200 mL finales.","Añadir 200 mL de solvente."],index=None)
    if st.button("Comprobar"): submit(3,math.isclose(a,50) and p and p.startswith("Tomar"),"25 % de 200 = **50 mL**; complete hasta 200 mL finales.","25/100 × 200.")
    feedback(3); key("En % v/v, el denominador es el volumen final."); nav()
elif L==4:
    mission("Ejercicio de dilución: azul de metileno al 1 % → preparar 100 mL al 0,1 %. ¿Qué volumen de solución madre se requiere?")
    concept(["C₁V₁=C₂V₂","Azul de metileno"]); st.markdown('<div class="formula">C₁V₁ = C₂V₂</div>',unsafe_allow_html=True)
    a=st.number_input("V₁ (mL)",0.0,step=1.0); p=st.radio("Luego:",["Agregar 100 mL de diluyente.","Completar hasta un volumen final de 100 mL."],index=None)
    if st.button("Comprobar"): submit(4,math.isclose(a,10) and p and p.startswith("Completar"),"V₁ = **10 mL**; complete hasta 100 mL finales.","V₁=(0,1×100)/1.")
    feedback(4); key("V₂ en C₁V₁=C₂V₂ es el volumen final."); nav()
elif L==5:
    mission("Convierta 1 % p/v y 0,1 % p/v a mg/mL.")
    concept(["% p/v"]); a=st.number_input("1 % = mg/mL",0.0,step=1.0); b=st.number_input("0,1 % = mg/mL",0.0,step=.1)
    if st.button("Comprobar"): submit(5,math.isclose(a,10) and math.isclose(b,1),"**10 mg/mL** y **1 mg/mL**, respectivamente.","1 g/100 mL = 1000 mg/100 mL.")
    feedback(5); key("La conversión de % a mg/mL permite verificar compatibilidad de unidades."); nav()
elif L==6:
    mission("Realiza una dilución 1:10 y repite el mismo paso con la solución obtenida. ¿Factor acumulado?")
    concept(["Factor de dilución"]); a=st.radio("Seleccione:",["1:10","1:20","1:100","1:1000"],index=None)
    if st.button("Comprobar"): submit(6,a=="1:100","1:10 × 1:10 = **1:100**.","Multiplique los factores sucesivos.")
    feedback(6); key("Los factores de una serie se multiplican."); nav()
elif L==7:
    mission("Cuadrado de Pearson: mezcle preparaciones al 20 % y 5 % para obtener 10 %. Determine las partes.")
    concept(["Cuadrado de Pearson"]); st.code("20 %  \\     /  5 partes\n       10 %\n 5 %  /     \\ 10 partes")
    a=st.number_input("Partes de 20 %",0.0,step=1.0); b=st.number_input("Partes de 5 %",0.0,step=1.0)
    if st.button("Comprobar"): submit(7,math.isclose(a,5) and math.isclose(b,10),"**5 partes de 20 % + 10 partes de 5 %**, relación 1:2.","Reste diagonalmente: 10−5 y 20−10.")
    feedback(7); key("Pearson entrega proporciones; luego deben convertirse a cantidades según el problema."); nav()
elif L==8:
    mission("Se requieren 10 g de compuesto puro y el reactivo disponible declara 80 % de pureza. Calcule la masa a pesar.")
    concept(["Pureza"]); a=st.number_input("Masa (g)",0.0,step=.1)
    if st.button("Comprobar"): submit(8,math.isclose(a,12.5,abs_tol=.01),"10/0,80 = **12,5 g**.","Divida la masa pura requerida entre 0,80.")
    feedback(8); key("La pureza del reactivo puede requerir corrección de la masa."); nav()
elif L==9:
    mission("«Para preparar 500 mL al 5 % p/v, peso 25 g y agrego 500 mL de agua». Encuentre el error.")
    concept(["% p/v"]); a=st.radio("Seleccione:",["Todo es correcto.","La masa es correcta, pero debe completar hasta 500 mL de solución final.","La masa correcta es 5 g."],index=None)
    if st.button("Comprobar"): submit(9,a and a.startswith("La masa es correcta"),"La masa **25 g** es correcta; el error es confundir volumen de solvente con volumen final.","5 g/100 mL × 500 mL = 25 g.")
    feedback(9); key("Un cálculo correcto no garantiza un procedimiento correcto."); nav()
elif L==10:
    mission("CÓDIGO TÓXICO: solución madre 2 % p/v → preparar 250 mL al 0,2 % p/v. Calcule, seleccione procedimiento y verifique mg/mL.")
    concept(["C₁V₁=C₂V₂","% p/v","Rotulado"]); v=st.number_input("Solución madre (mL)",0.0,step=1.0)
    p=st.radio("Secuencia:",["Tomar 25 mL → completar hasta 250 mL → homogeneizar → rotular.","Tomar 25 mL → agregar 250 mL de diluyente → usar sin rotular."],index=None)
    c=st.number_input("0,2 % p/v = ¿mg/mL?",0.0,step=.1)
    if st.button("Finalizar estación"): submit(10,math.isclose(v,25) and p and p.startswith("Tomar 25 mL → completar") and math.isclose(c,2),"V₁ = **25 mL** y 0,2 % = **2 mg/mL**. Secuencia correcta.","Use C₁V₁=C₂V₂ y convierta 0,2 g/100 mL.")
    feedback(10); key("La competencia integra cálculo, procedimiento, verificación y rotulado.")
    if st.session_state.solved.get(10):
        st.divider(); st.subheader("🏁 Resultado"); st.metric("Puntaje",f"{st.session_state.score}/100")
        st.button("Repetir laboratorio",on_click=reset,type="primary")

st.divider(); st.caption("TOX-PREP · Recurso educativo. No sustituye protocolos clínicos, fichas técnicas, evaluación del paciente ni normativa institucional.")
