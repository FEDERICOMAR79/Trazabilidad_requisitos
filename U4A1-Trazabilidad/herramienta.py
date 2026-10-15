#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Herramienta de trazabilidad del proyecto Tripulaciones (TRI).

Lee las fuentes del repositorio y genera, sin editar nada a mano:
  - la tabla de metadatos del README (catálogo de artefactos),
  - la matriz de trazabilidad Matriz_trazabilidad.xlsx,
  - la auditoría Auditoria_trazabilidad.md.

Fuentes (todas dentro del repositorio):
  Backlog/Product_backlog.reqw                           requisitos (HU y RNF) y su prioridad (archivo de ReqView)
  U3A2-Prototipado/prototipo/index.html                  código: marcas  @trace HU-xx  sobre cada función
  U3A2-Prototipado/pruebas/resultados_pruebas.json       resultado de cada prueba y el requisito que verifica
  U3A2-Prototipado/trazabilidad/cambios_aprobados.json   decisiones del CCB y artefactos de cada RFC
  U4A1-Trazabilidad/necesidades.json                     necesidades del Vision Board y relación con los requisitos
  U4A1-Trazabilidad/catalogo_artefactos.json             metadatos de cada artefacto
  git                              si cada artefacto está bajo control de versiones

Uso (desde la raíz del repositorio, con los cambios ya agregados a git):
  python3 U4A1-Trazabilidad/herramienta.py todo        # catálogo + matriz + auditoría
  python3 U4A1-Trazabilidad/herramienta.py catalogo    # solo valida y actualiza el README
  python3 U4A1-Trazabilidad/herramienta.py matriz      # solo la matriz xlsx
  python3 U4A1-Trazabilidad/herramienta.py auditoria   # solo la auditoría
Requiere: Python 3.9+ y openpyxl (pip install openpyxl).
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent          # U4A1-Trazabilidad
RAIZ = AQUI.parent                               # raíz del repositorio
U3A2 = RAIZ / "U3A2-Prototipado"
BACKLOG = RAIZ / "Backlog" / "Product_backlog.reqw"
PROTOTIPO = U3A2 / "prototipo" / "index.html"
RESULTADOS = U3A2 / "pruebas" / "resultados_pruebas.json"
CAMBIOS = U3A2 / "trazabilidad" / "cambios_aprobados.json"
CAMPOS_META = ["id", "version", "estado_final", "autor", "fecha_cierre", "relacionados"]  # mínimo exigido
PRIO = {"High": "Alta", "Medium": "Media", "Low": "Baja"}
GENERADOS = {"U4A1-Trazabilidad/Matriz_trazabilidad.xlsx", "U3A2-Prototipado/trazabilidad/Matriz_trazabilidad.md",
             "U3A2-Prototipado/trazabilidad/Matriz_trazabilidad.csv", "U4A1-Trazabilidad/Auditoria_trazabilidad.md"}  # salidas de esta herramienta: pueden no existir aún
MARCA_INI, MARCA_FIN = "<!-- METADATOS:INICIO -->", "<!-- METADATOS:FIN -->"


def _json(ruta):
    return json.loads(Path(ruta).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- lectura de fuentes
def nodos_reqw(lista):
    """Recorre los nodos de un documento ReqView en orden, sin los eliminados."""
    for n in lista:
        if n.get("deleted"):
            continue
        yield n
        yield from nodos_reqw(n.get("children", []))


def cargar_backlog():
    """Lee el backlog desde el archivo de ReqView (.reqw). HU = historias, RNF = restricciones, en orden de documento."""
    doc = next(x for x in _json(BACKLOG)["documents"] if x["id"] == "NEEDS")
    reqs, n_hu, n_rnf = {}, 0, 0
    for r in nodos_reqw(doc["data"]):
        if r.get("type") not in ("STORY", "CON"):
            continue
        if r["type"] == "STORY":
            n_hu += 1; k = "HU-%02d" % n_hu
        else:
            n_rnf += 1; k = "RNF-%02d" % n_rnf
        reqs[k] = dict(id=k, titulo=r["heading"], tipo="Funcional" if k.startswith("HU") else "Restricción",
                       actor=r["asAn"], prioridad=PRIO.get(r["priority"], r["priority"]),
                       criterios=len(re.findall(r"<li>", r.get("acceptanceCriteria", ""))))
    return reqs


def cargar_codigo():
    """Devuelve (requisito -> [elementos], vistas sin marca). Lee las marcas @trace del prototipo."""
    txt = PROTOTIPO.read_text(encoding="utf-8")
    patron = re.compile(r"/\*\s*@trace\s+([A-Z0-9 ,\-]+?)\s*(?:\|\s*([^*]+?))?\s*\*/\s*(?:function\s+(\w+)|const\s+(\w+))?")
    por_req = {}
    for m in patron.finditer(txt):
        nombre = (m.group(2) or m.group(3) or m.group(4) or "(sin nombre)").strip()
        for r in re.findall(r"(?:HU|RNF)-\d{2}", m.group(1)):
            lst = por_req.setdefault(r, [])
            if nombre not in lst:
                lst.append(nombre)
    con_marca = {m.group(3) for m in patron.finditer(txt) if m.group(3)}
    vistas = set(re.findall(r"function\s+(v[A-Z]\w*)\s*\(", txt))
    return por_req, sorted(vistas - con_marca)


def cargar_pruebas():
    res = _json(RESULTADOS)
    por_req = {}
    for t in res:
        por_req.setdefault(t["req"], []).append(t)
    return res, por_req


def git_estado(ruta):
    """True si el archivo (o carpeta) está en git: confirmado o ya agregado al índice."""
    try:
        out = subprocess.run(["git", "ls-files", "--", str(ruta)], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
        return bool(out.strip())
    except Exception:
        return False


# ---------------------------------------------------------------- modelo común
def modelo():
    backlog = cargar_backlog()
    codigo, vistas_sin_marca = cargar_codigo()
    pruebas, pruebas_por_req = cargar_pruebas()
    nec = _json(AQUI / "necesidades.json")
    cambios = _json(CAMBIOS)
    cat = _json(AQUI / "catalogo_artefactos.json")
    fecha_matriz = next(a["fecha_cierre"] for a in cat["artefactos"] if a["id"] == "TRI-MTZ-007")
    nec_de = {}
    for n in nec["necesidades"]:
        for r in n["requisitos"]:
            nec_de.setdefault(r, []).append(n["id"])
    rfc_de = {}
    for c in cambios["cambios_aprobados"]:
        for r in c["requisitos"]:
            rfc_de.setdefault(r, []).append(c["rfc"])
    filas = []
    for k, r in backlog.items():
        pr = pruebas_por_req.get(k, [])
        ok = sum(1 for t in pr if t["ok"])
        cod = codigo.get(k, [])
        if cod and pr and ok == len(pr):
            estado = "Verificado"
        elif cod:
            estado = "Implementado"
        else:
            estado = "Aprobado"
        resultado = "Sin prueba" if not pr else ("Pasado %d/%d" % (ok, len(pr)) if ok == len(pr) else "Falló %d/%d" % (len(pr) - ok, len(pr)))
        nota = nec["notas_requisitos"].get(k) or nec["fuera_de_alcance_prototipo"].get(k, "")
        filas.append(dict(r, necesidades=nec_de.get(k, []), codigo=cod, pruebas=[t["id"] for t in pr], resultado=resultado,
                          estado=estado, rfc=rfc_de.get(k, []), nota=nota, fuera=k in nec["fuera_de_alcance_prototipo"]))
    return dict(backlog=backlog, codigo=codigo, vistas_sin_marca=vistas_sin_marca, pruebas=pruebas, nec=nec, cambios=cambios,
                cat=cat, filas=filas, fecha=fecha_matriz)


# ---------------------------------------------------------------- catálogo y metadatos
def validar_catalogo(m):
    errores, avisos = [], []
    ids = {a["id"] for a in m["cat"]["artefactos"]}
    for a in m["cat"]["artefactos"]:
        for c in CAMPOS_META:
            v = a.get(c)
            if v in (None, "", []):
                errores.append("%s: falta el metadato «%s»" % (a["id"], c))
        if not (a.get("autor") or a.get("revisor")):
            errores.append("%s: sin autor ni revisor" % a["id"])
        for rel in a.get("relacionados", []):
            if rel not in ids:
                errores.append("%s: artefacto relacionado inexistente (%s)" % (a["id"], rel))
        for ruta in a["rutas"]:
            if ruta in GENERADOS:
                continue
            if not (RAIZ / ruta).exists():
                errores.append("%s: no existe el archivo %s" % (a["id"], ruta))
            elif not git_estado(ruta):
                avisos.append("%s: %s no está en git (agrégalo con git add)" % (a["id"], ruta))
    return errores, avisos


def fecha_corta(iso):
    y, mth, d = iso.split("-")
    return "%s/%s/%s" % (d, mth, y)


def tabla_metadatos(m):
    f = ["| ID | Artefacto | Tipo | Versión | Estado final | Autor o revisor | Fecha de cierre | Artefactos relacionados |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for a in m["cat"]["artefactos"]:
        arch = " · ".join("[%s](%s)" % (Path(r).name if not Path(r).is_dir() else Path(r).name + "/", r) for r in a["rutas"][:2])
        extra = " (+%d)" % (len(a["rutas"]) - 2) if len(a["rutas"]) > 2 else ""
        persona = "%s (autor); revisor: %s" % (a["autor"], a["revisor"])
        f.append("| %s | %s%s | %s | %s | %s | %s | %s | %s |" % (a["id"], arch, extra, a["tipo"], a["version"], a["estado_final"],
                 persona, fecha_corta(a["fecha_cierre"]), ", ".join(a["relacionados"])))
    return "\n".join(f)


def actualizar_readme(m):
    ruta = RAIZ / "README.md"
    txt = ruta.read_text(encoding="utf-8")
    if MARCA_INI not in txt or MARCA_FIN not in txt:
        print("AVISO: el README no tiene las marcas %s / %s; no se actualizó." % (MARCA_INI, MARCA_FIN)); return
    antes, resto = txt.split(MARCA_INI, 1)
    _, despues = resto.split(MARCA_FIN, 1)
    ruta.write_text(antes + MARCA_INI + "\n" + tabla_metadatos(m) + "\n" + MARCA_FIN + despues, encoding="utf-8")
    print("README: tabla de metadatos actualizada (%d artefactos)" % len(m["cat"]["artefactos"]))


def cmd_catalogo(m):
    errores, avisos = validar_catalogo(m)
    for a in avisos: print("AVISO:", a)
    if errores:
        print("ERRORES DE METADATOS:"); [print(" -", e) for e in errores]; sys.exit(1)
    print("Metadatos completos en %d artefactos." % len(m["cat"]["artefactos"]))
    actualizar_readme(m)


# ---------------------------------------------------------------- auditoría
SEV_ORDEN = {"Alto": 0, "Medio": 1, "Bajo": 2}


def hallazgos(m):
    h = []
    def add(tipo, elemento, detalle, sev, estado, resp, accion):
        h.append(dict(tipo=tipo, elemento=elemento, detalle=detalle, severidad=sev, estado=estado, responsable=resp, accion=accion))
    reqs = m["backlog"]
    for n in m["nec"]["necesidades"]:
        for r in n["requisitos"]:
            if r not in reqs:
                add("Necesidad → requisito", n["id"], "Cita %s, que no existe en el backlog." % r, "Alto", "Abierto", "Analista de requisitos", "Corregir la relación en necesidades.json.")
        if not n["requisitos"]:
            add("Necesidad → requisito", n["id"], "La necesidad no tiene ningún requisito.", "Alto", "Abierto", "Analista de requisitos", "Derivar al menos un requisito.")
    for f in m["filas"]:
        k = f["id"]
        if not f["necesidades"]:
            add("Requisito → necesidad", k, "El requisito no responde a ninguna necesidad.", "Alto", "Abierto", "Analista de requisitos", "Relacionarlo con una necesidad o retirarlo.")
        if not f["codigo"]:
            just = f["nota"] if f["fuera"] else ""
            sev = "Medio" if f["prioridad"] == "Alta" else "Bajo"
            add("Requisito → código", "%s %s" % (k, f["titulo"]), "Sin código en el prototipo. %s" % just if just else "Sin código en el prototipo.",
                sev, "Aceptado (fuera de alcance)" if f["fuera"] else "Abierto", "Product Owner",
                "Planificar su construcción tras el prototipo." if f["fuera"] else "Implementarlo o justificar su exclusión.")
        elif not f["pruebas"]:
            add("Requisito → prueba", k, "Tiene código pero ninguna prueba.", "Alto", "Abierto", "QA Lead", "Escribir pruebas.")
        elif not f["resultado"].startswith("Pasado"):
            add("Prueba → resultado", k, "Hay pruebas fallidas: %s." % f["resultado"], "Alto", "Abierto", "QA Lead", "Corregir y repetir.")
    for v in m["vistas_sin_marca"]:
        add("Código → requisito", v, "La función %s del prototipo no tiene marca @trace: implementa una pantalla sin requisito en el backlog "
            "(consulta de escenarios y evaluación del piloto, que el caso describe)." % v, "Medio", "Abierto", "Analista de requisitos",
            "Agregar una historia de usuario al backlog para la consulta de escenarios y marcar la función.")
    sin_req = [t["id"] for t in m["pruebas"] if not re.match(r"(HU|RNF)-\d\d", t["req"])]
    if sin_req:
        add("Prueba → requisito", ", ".join(sin_req), "Pruebas sin requisito del backlog: consulta de escenarios (P19, P20) y pruebas "
            "transversales de defectos y calidad (P26 a P28, P30).", "Bajo", "Abierto", "QA Lead", "Relacionar P19 y P20 con la historia nueva; las demás quedan como pruebas de regresión.")
    for c in m["cambios"]["cambios_aprobados"]:
        for r in c["requisitos"]:
            if r not in reqs:
                add("RFC → requisito", c["rfc"], "Cita %s, que no existe en el backlog." % r, "Alto", "Abierto", "Analista de requisitos", "Corregir la RFC.")
        ejecutados = {t["id"] for t in m["pruebas"]}
        sin = [t.split(" ")[0] for t in c["tc"] if t.split(" ")[0] not in ejecutados]
        if sin:
            add("RFC → prueba", c["rfc"], "%d casos de prueba propuestos sin implementar (%s)." % (len(sin), ", ".join(sin)),
                "Alto" if c["prioridad"] == "Crítica" else "Medio", "Abierto", "QA Lead", "Escribirlos al construir el cambio. Plazo: %s." % c["plazo"])
    errores, avisos = validar_catalogo(m)
    for e in errores:
        add("Metadatos", e.split(":")[0], e, "Medio", "Abierto", "Autor", "Completar el metadato en catalogo_artefactos.json.")
    for a in avisos:
        add("Control de versiones", a.split(":")[0], a, "Medio", "Abierto", "Autor", "Agregar el archivo a git y confirmar el cambio.")
    for x in m["nec"]["hallazgos_manuales"]:
        add(x["tipo"], x["id"], x["detalle"], x["severidad"], x["estado"], x["responsable"], x["accion"])
    h.sort(key=lambda x: (SEV_ORDEN[x["severidad"]], x["estado"].startswith(("Cerrado", "Aceptado")), x["tipo"]))
    for i, x in enumerate(h, 1):
        x["id"] = "AUD-%02d" % i
    return h


def cadena(m):
    """Resumen de la cadena necesidad → requisito → prueba → código → resultado."""
    out = []
    for f in m["filas"]:
        out.append(dict(id=f["id"], necesidad=bool(f["necesidades"]), prueba=bool(f["pruebas"]), codigo=bool(f["codigo"]),
                        resultado=f["resultado"].startswith("Pasado"), completa=bool(f["necesidades"] and f["pruebas"] and f["codigo"] and f["resultado"].startswith("Pasado"))))
    return out


def cmd_auditoria(m):
    h = hallazgos(m)
    ch = cadena(m)
    comp = [c["id"] for c in ch if c["completa"]]
    abiertos = [x for x in h if not x["estado"].startswith(("Cerrado", "Aceptado"))]
    mk = lambda b: "✓" if b else "✗"
    md = ["# Auditoría de trazabilidad end-to-end", "",
          "Generada por `U4A1-Trazabilidad/herramienta.py auditoria`. Fecha de la matriz: %s." % fecha_corta(m["fecha"]), "",
          "Cadena auditada: **necesidad de negocio → requisito → caso de prueba → código → resultado**.", "",
          "## Resultado", "",
          "- Requisitos auditados: %d (HU y RNF del backlog)." % len(ch),
          "- Con la cadena completa: **%d de %d** (%s)." % (len(comp), len(ch), ", ".join(comp)),
          "- Hallazgos: %d en total; %d abiertos o por resolver, %d cerrados o aceptados." % (len(h), len(abiertos), len(h) - len(abiertos)),
          "- Severidad de los abiertos: %s." % ", ".join("%d %s" % (sum(1 for x in abiertos if x["severidad"] == s), s.lower()) for s in ("Alto", "Medio", "Bajo")), "",
          "## Cadena por requisito", "",
          "| Requisito | Necesidad | Prueba | Código | Resultado | Cadena completa |", "| --- | --- | --- | --- | --- | --- |"]
    for c in ch:
        md.append("| %s | %s | %s | %s | %s | %s |" % (c["id"], mk(c["necesidad"]), mk(c["prueba"]), mk(c["codigo"]), mk(c["resultado"]), "Sí" if c["completa"] else "No"))
    md += ["", "## Hallazgos", "", "| ID | Tipo de ruptura | Elemento | Detalle | Severidad | Estado | Responsable | Acción |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for x in h:
        md.append("| %s | %s | %s | %s | %s | %s | %s | %s |" % (x["id"], x["tipo"], x["elemento"], x["detalle"].replace("|", "/"), x["severidad"], x["estado"], x["responsable"], x["accion"]))
    (AQUI / "Auditoria_trazabilidad.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("Auditoría: %d requisitos, cadena completa en %d, %d hallazgos (%d abiertos)." % (len(ch), len(comp), len(h), len(abiertos)))
    return h


# ---------------------------------------------------------------- matriz xlsx
def cmd_matriz(m, h=None):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter as L
    h = h if h is not None else hallazgos(m)
    wb = Workbook()
    AZUL = PatternFill("solid", fgColor="1F3864"); GRIS = PatternFill("solid", fgColor="F2F2F2")
    VERDE = PatternFill("solid", fgColor="E2EFDA"); AMAR = PatternFill("solid", fgColor="FFF2CC"); ROJO = PatternFill("solid", fgColor="FCE4D6")
    fino = Side(style="thin", color="BFBFBF"); borde = Border(left=fino, right=fino, top=fino, bottom=fino)

    def hoja(nombre, titulo, cols, filas, anchos, primera=False, fila_enc=3):
        ws = wb.active if primera else wb.create_sheet()
        ws.title = nombre
        ws["A1"] = titulo; ws["A1"].font = Font(bold=True, size=14, color="1F3864")
        for j, c in enumerate(cols, 1):
            x = ws.cell(row=fila_enc, column=j, value=c); x.font = Font(bold=True, color="FFFFFF"); x.fill = AZUL
            x.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); x.border = borde
        for i, fila in enumerate(filas, fila_enc + 1):
            for j, v in enumerate(fila, 1):
                x = ws.cell(row=i, column=j, value=v); x.alignment = Alignment(wrap_text=True, vertical="top"); x.border = borde
        for j, w in enumerate(anchos, 1):
            ws.column_dimensions[L(j)].width = w
        ws.freeze_panes = ws.cell(row=fila_enc + 1, column=3)
        ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        return ws

    # Instrucciones
    ws = wb.active; ws.title = "Instrucciones"
    txt = ["MATRIZ DE TRAZABILIDAD DE REQUISITOS — Proyecto Tripulaciones (TRI-MTZ-007)",
           "Generada automáticamente por U4A1-Trazabilidad/herramienta.py. No se edita a mano: se cambian las fuentes y se vuelve a generar.", "",
           "Fuentes: backlog (Backlog/Product_backlog.reqw), código (marcas @trace en U3A2-Prototipado/prototipo/index.html), pruebas (U3A2-Prototipado/pruebas/resultados_pruebas.json),",
           "necesidades (trazabilidad/necesidades.json), decisiones del CCB (trazabilidad/cambios_aprobados.json) y catálogo (trazabilidad/catalogo_artefactos.json).", "",
           "Hojas: Matriz principal · Trazabilidad visual (requisito × artefacto) · Resumen y métricas · Registro de RFCs · Catálogo de artefactos · Auditoría.", "",
           "Estados: Verificado = tiene código y todas sus pruebas pasan · Implementado = tiene código sin pruebas · Aprobado = está en el backlog, sin construir en el prototipo.",
           "Para regenerar:  python3 U4A1-Trazabilidad/herramienta.py todo"]
    for i, t in enumerate(txt, 1):
        ws.cell(row=i, column=1, value=t)
    ws["A1"].font = Font(bold=True, size=14, color="1F3864"); ws.column_dimensions["A"].width = 150

    # Matriz principal
    cols = ["ID Requisito", "Título del requisito", "Tipo", "ID Necesidad de negocio", "Actor / stakeholder", "Prioridad", "Versión del backlog",
            "Criterios de aceptación (n)", "Código (funciones con @trace)", "Implementación", "ID Casos de prueba", "Resultado prueba", "Fecha última prueba",
            "Estado actual", "RFC aprobadas asociadas", "Última actualización", "Notas / observaciones"]
    fecha_prueba = next(a["fecha_cierre"] for a in m["cat"]["artefactos"] if a["id"] == "TRI-PRU-004")
    filas = [[f["id"], f["titulo"], f["tipo"], ", ".join(f["necesidades"]), f["actor"], f["prioridad"], "TRI-PBL-001 v1.0", f["criterios"] or "—",
              ", ".join(f["codigo"]) or "—", "Prototipo v0.2" if f["codigo"] else "Pendiente", ", ".join(f["pruebas"]) or "—", f["resultado"],
              fecha_prueba if f["pruebas"] else "—", f["estado"], ", ".join(f["rfc"]) or "—", m["fecha"], f["nota"] or ""] for f in m["filas"]]
    ws = hoja("Matriz principal", "MATRIZ DE TRAZABILIDAD DE REQUISITOS — Hoja principal", cols, filas,
              [11, 38, 12, 16, 22, 10, 16, 12, 36, 14, 26, 14, 14, 14, 24, 14, 50], fila_enc=3)
    n = len(filas); ult = 3 + n
    for i in range(4, ult + 1):
        e = ws.cell(row=i, column=14); e.fill = VERDE if e.value == "Verificado" else (AMAR if e.value == "Implementado" else GRIS)
        r = ws.cell(row=i, column=12)
        if str(r.value).startswith("Falló"): r.fill = ROJO
    ws.row_dimensions[3].height = 45

    # Trazabilidad visual
    elementos = sorted({e for f in m["filas"] for e in f["codigo"]})
    necs = [x["id"] for x in m["nec"]["necesidades"]]
    cols = ["ID Req.", "Título"] + necs + elementos + ["Pruebas (n)", "RFC aprobadas (n)"]
    filas = []
    for f in m["filas"]:
        filas.append([f["id"], f["titulo"][:40]] + ["✓" if x in f["necesidades"] else "" for x in necs] + ["✓" if x in f["codigo"] else "" for x in elementos]
                     + [len(f["pruebas"]), len(f["rfc"])])
    ws = hoja("Trazabilidad visual", "TRAZABILIDAD VISUAL — Requisitos × Necesidades × Código", cols, filas, [10, 36] + [9] * len(necs) + [14] * len(elementos) + [11, 14])
    ws.row_dimensions[3].height = 60
    for j in range(3, 3 + len(necs) + len(elementos)):
        ws.cell(row=3, column=j).alignment = Alignment(text_rotation=90, horizontal="center", vertical="bottom")
    fila_cob = 4 + n + 1
    ws.cell(row=fila_cob, column=1, value="Cobertura (%)").font = Font(bold=True)
    for j in range(3, 3 + len(necs) + len(elementos)):
        c = L(j)
        x = ws.cell(row=fila_cob, column=j, value='=COUNTIF(%s4:%s%d,"✓")/%d' % (c, c, 3 + n, n)); x.number_format = "0%"

    # Resumen y métricas (fórmulas sobre la matriz principal)
    ws = wb.create_sheet("Resumen y métricas")
    ws["A1"] = "RESUMEN Y MÉTRICAS — Dashboard de trazabilidad"; ws["A1"].font = Font(bold=True, size=14, color="1F3864")
    ws["A2"] = "Se calculan con fórmulas sobre la hoja «Matriz principal»."
    P = "'Matriz principal'!"
    rng = lambda col: "%s%s4:%s%d" % (P, col, col, ult)
    rot = [("Total requisitos", "=COUNTA(%s)" % rng("A")), ("Verificados", '=COUNTIF(%s,"Verificado")' % rng("N")),
           ("Implementados sin verificar", '=COUNTIF(%s,"Implementado")' % rng("N")), ("Aprobados, sin construir", '=COUNTIF(%s,"Aprobado")' % rng("N")),
           ("Con pruebas fallidas", '=COUNTIF(%s,"Falló*")' % rng("L")), ("Sin prueba", '=COUNTIF(%s,"Sin prueba")' % rng("L")),
           ("Con necesidad asociada", '=COUNTIF(%s,"NEG*")' % rng("D")), ("Con código", '=COUNTIF(%s,"<>—")' % rng("I")),
           ("Alta prioridad", '=COUNTIF(%s,"Alta")' % rng("F")), ("Media prioridad", '=COUNTIF(%s,"Media")' % rng("F")), ("Baja prioridad", '=COUNTIF(%s,"Baja")' % rng("F")),
           ("Alta prioridad verificada", '=COUNTIFS(%s,"Alta",%s,"Verificado")' % (rng("F"), rng("N")))]
    for i, (k, v) in enumerate(rot, 4):
        a = ws.cell(row=i, column=1, value=k); a.font = Font(bold=True); a.border = borde
        b = ws.cell(row=i, column=2, value=v); b.border = borde
    for fila, (k, v) in ((16, ("Cobertura de código (%)", "=B11/B4")), (17, ("Cobertura de pruebas (%)", "=1-B9/B4"))):
        ws.cell(row=fila, column=1, value=k).font = Font(bold=True); x = ws.cell(row=fila, column=2, value=v); x.number_format = "0%"
    abiertos = sum(1 for x in h if not x["estado"].startswith(("Cerrado", "Aceptado")))
    ws["A18"] = "Hallazgos de auditoría abiertos"; ws["A18"].font = Font(bold=True); ws["B18"] = abiertos
    ws.column_dimensions["A"].width = 40; ws.column_dimensions["B"].width = 14
    # alertas de cobertura (lista fija calculada por el script)
    r0 = 21
    ws.cell(row=r0 - 1, column=1, value="ALERTAS — requisitos aprobados sin código en el prototipo").font = Font(bold=True)
    for j, c in enumerate(["ID Req.", "Título", "Prioridad", "Motivo"], 1):
        x = ws.cell(row=r0, column=j, value=c); x.font = Font(bold=True, color="FFFFFF"); x.fill = AZUL
    for i, f in enumerate([f for f in m["filas"] if not f["codigo"]], r0 + 1):
        for j, v in enumerate([f["id"], f["titulo"], f["prioridad"], f["nota"]], 1):
            ws.cell(row=i, column=j, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["C"].width = 12; ws.column_dimensions["D"].width = 80

    # Registro de RFCs
    cols = ["ID RFC", "Título del cambio", "Origen", "Prioridad", "Requisito(s) afectados", "Casos de prueba propuestos", "Decisión del CCB", "Votos", "Plazo", "Responsable", "Estado"]
    filas = []
    for c in m["cambios"]["cambios_aprobados"]:
        filas.append([c["rfc"], c["titulo"], c["origen"], c["prioridad"], ", ".join(c["requisitos"]), ", ".join(t.split(" ")[0] for t in c["tc"]),
                      c["decision"], c["votos"], c["plazo"], c["responsable"], c["estado"]])
    for o in m["cambios"]["no_aprobados"]:
        filas.append([o["rfc"], o["titulo"], "", "", "", "", o["decision"], o["votos"], "", "", o["motivo"]])
    hoja("Registro de RFCs", "REGISTRO DE SOLICITUDES DE CAMBIO (RFC) — CCB del %s" % m["cambios"]["fecha_ccb"], cols, filas, [10, 40, 30, 10, 26, 34, 14, 26, 32, 14, 50])

    # Catálogo
    cols = ["ID Artefacto", "Nombre", "Tipo", "Versión", "Estado final", "Autor", "Revisor", "Fecha de cierre", "Artefactos relacionados", "Archivos", "En git"]
    filas = [[a["id"], a["nombre"], a["tipo"], a["version"], a["estado_final"], a["autor"], a["revisor"], a["fecha_cierre"], ", ".join(a["relacionados"]),
              "\n".join(a["rutas"]), "Sí" if all(git_estado(r) for r in a["rutas"]) else "No"] for a in m["cat"]["artefactos"]]
    hoja("Catálogo de artefactos", "CATÁLOGO DE ARTEFACTOS — metadatos", cols, filas, [13, 30, 26, 9, 40, 18, 20, 14, 36, 55, 8])

    # Auditoría
    cols = ["ID", "Tipo de ruptura", "Elemento", "Detalle", "Estado", "Severidad", "Responsable", "Acción"]
    filas = [[x["id"], x["tipo"], x["elemento"], x["detalle"], x["estado"], x["severidad"], x["responsable"], x["accion"]] for x in h]
    ws = hoja("Auditoría", "AUDITORÍA DE TRAZABILIDAD END-TO-END", cols, filas, [9, 22, 30, 70, 24, 11, 22, 55])
    for i in range(4, 4 + len(h)):
        s = ws.cell(row=i, column=6); s.fill = ROJO if s.value == "Alto" else (AMAR if s.value == "Medio" else GRIS)
    for w in wb.worksheets:
        w.page_setup.orientation = "landscape"; w.page_setup.fitToWidth = 1; w.page_setup.fitToHeight = 0
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(AQUI / "Matriz_trazabilidad.xlsx")
    print("Matriz: Matriz_trazabilidad.xlsx (%d requisitos, %d hallazgos)" % (len(m["filas"]), len(h)))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("comando", choices=["todo", "catalogo", "matriz", "auditoria"])
    a = p.parse_args()
    m = modelo()
    if a.comando in ("todo", "catalogo"):
        cmd_catalogo(m)
    h = None
    if a.comando in ("todo", "auditoria"):
        h = cmd_auditoria(m)
    if a.comando in ("todo", "matriz"):
        cmd_matriz(m, h)
        subprocess.run([sys.executable, str(U3A2 / "trazabilidad" / "generar_matriz.py")], check=True)  # matriz de cambios aprobados (csv y md)


if __name__ == "__main__":
    main()
