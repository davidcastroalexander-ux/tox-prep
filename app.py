import math
import time
import streamlit as st
import pandas as pd

st.set_page_config(page_title="TOX-PREP 2.1", page_icon="⚗️", layout="wide")

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

def module_nav():
    st.subheader("🧭 Navegación por módulos")
    cols=st.columns(5)
    for col,(mod,levels) in zip(cols,MODULES.items()):
        label=f"{mod}\n" + " · ".join([f"{'✓' if st.session_state.solved.get(l) else '●' if st.session_state.level==l else '○'} M{l}" for l in levels])
        if col.button(label,use_container_width=True,key=f"mod_{mod}"):
            goto(levels[0])
    current=MOD_BY_LEVEL[st.session_state.level]
    st.caption(f"Módulo actual: **{current}**")
    subcols=st.columns(len(MODULES[current]))
    for col,l in zip(subcols,MODULES[current]):
        state="✓" if st.session_state.solved.get(l) else "●" if st.session_state.level==l else "○"
        if col.button(f"{state} Misión {l} · {TITLES[l]}",use_container_width=True,key=f"go_{l}"):
            goto(l)

def prev_next():
    a,b,_=st.columns([1,1,5])
    if a.button("← Anterior",disabled=st.session_state.level==1):
        goto(st.session_state.level-1)
    if b.button("Siguiente →",disabled=not st.session_state.solved.get(st.session_state.level) or st.session_state.level==TOTAL):
        goto(st.session_state.level+1)

if not st.session_state.started:
    st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 2.1</h1><p>Simulador veterinario de soluciones, diluciones y cálculos aplicados a Toxicología</p></div>',unsafe_allow_html=True)
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

st.markdown('<div class="hero"><h1>⚗️ TOX-PREP 2.1</h1><p>Laboratorio virtual veterinario de preparación aplicada a Toxicología</p></div>',unsafe_allow_html=True)
c1,c2,c3=st.columns([5,1,1])
c1.progress(st.session_state.level/TOTAL,text=f"Misión {st.session_state.level}/{TOTAL}")
c2.metric("Puntaje",f"{st.session_state.score}/100")
c3.button("Reiniciar",on_click=reset)
module_nav()
L=st.session_state.level
st.markdown(f'<span class="badge">{MOD_BY_LEVEL[L]}</span>',unsafe_allow_html=True)
st.header(f"Misión {L} · {TITLES[L]}")
show_animation(L)

if L==1:
    mission("En un laboratorio veterinario debe preparar una solución de trabajo. Antes de iniciar, convierta 2,5 g a mg y 750 µL a mL.")
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
st.caption("TOX-PREP 2.1 · Recurso educativo para medicina veterinaria y toxicología. No sustituye protocolos clínicos, fichas técnicas, evaluación del paciente ni normativa institucional.")
