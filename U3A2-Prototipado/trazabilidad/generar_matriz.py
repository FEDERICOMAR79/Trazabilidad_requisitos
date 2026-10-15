#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera la matriz de trazabilidad de los cambios aprobados.

Entradas (relativas a este archivo):
  cambios_aprobados.json   decisiones del CCB y artefactos de cada RFC aprobada
  ../../Backlog/Product_backlog_ReqView.csv   backlog: valida que cada HU/RNF exista
  ../prototipo/index.html  código del prototipo: se leen las marcas  @trace HU-xx

Salidas: Matriz_trazabilidad.csv y Matriz_trazabilidad.md
Uso:  python3 generar_matriz.py
"""
import csv, json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                # carpeta U3A2-Prototipado
BACKLOG = RAIZ.parent / "Backlog" / "Product_backlog_ReqView.csv"


def cargar_backlog():
    ids, n_hu, n_rnf = {}, 0, 0
    with open(BACKLOG, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["type"] == "User Story":
                n_hu += 1; k = "HU-%02d" % n_hu
            else:
                n_rnf += 1; k = "RNF-%02d" % n_rnf
            ids[k] = r["heading"]
    return ids


def cargar_codigo():
    """Lee las marcas @trace del prototipo. Devuelve {requisito: [elementos]}."""
    txt = (RAIZ / "prototipo" / "index.html").read_text(encoding="utf-8")
    patron = re.compile(r"/\*\s*@trace\s+([A-Z0-9 ,\-]+?)\s*(?:\|\s*([^*]+?))?\s*\*/\s*(?:function\s+(\w+)|const\s+(\w+))?")
    por_req = {}
    for m in patron.finditer(txt):
        reqs = re.findall(r"(?:HU|RNF)-\d{2}", m.group(1))
        nombre = (m.group(2) or m.group(3) or m.group(4) or "(sin nombre)").strip()
        for r in reqs:
            por_req.setdefault(r, [])
            if nombre not in por_req[r]:
                por_req[r].append(nombre)
    return por_req


def main():
    datos = json.loads((AQUI / "cambios_aprobados.json").read_text(encoding="utf-8"))
    backlog = cargar_backlog()
    codigo = cargar_codigo()
    errores = []
    filas = []
    for c in datos["cambios_aprobados"]:
        for r in c["requisitos"]:
            if r not in backlog:
                errores.append("%s cita %s, que no existe en el backlog" % (c["rfc"], r))
        for campo in ("tc", "modulos", "docs"):
            if not c[campo]:
                errores.append("%s no tiene %s" % (c["rfc"], campo))
        elementos = sorted({e for r in c["requisitos"] for e in codigo.get(r, [])})
        filas.append(dict(
            rfc=c["rfc"], titulo=c["titulo"], origen=c["origen"], decision=c["decision"], plazo=c["plazo"],
            requisitos="; ".join("%s %s" % (r, backlog.get(r, "?")) for r in c["requisitos"]),
            tc="; ".join(c["tc"]), modulos="; ".join(c["modulos"]), docs="; ".join(c["docs"]),
            prototipo="; ".join(elementos) or "—", responsable=c["responsable"], estado=c["estado"]))
    if errores:
        print("ERRORES DE CONSISTENCIA:"); [print(" -", e) for e in errores]; sys.exit(1)

    cols = ["rfc", "titulo", "origen", "decision", "plazo", "requisitos", "tc", "modulos", "docs", "prototipo", "responsable", "estado"]
    enc = ["RFC", "Título", "Origen del cambio", "Decisión del CCB", "Plazo", "Requisitos afectados", "Casos de prueba", "Módulos de código", "Documentación", "Elementos del prototipo (leídos del código)", "Responsable", "Estado"]
    with open(AQUI / "Matriz_trazabilidad.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f); w.writerow(enc); [w.writerow([fila[c] for c in cols]) for fila in filas]

    # vista inversa: requisito -> RFC aprobadas
    inv = {}
    for c in datos["cambios_aprobados"]:
        for r in c["requisitos"]:
            inv.setdefault(r, []).append(c["rfc"])
    orden = sorted(inv, key=lambda k: (k.startswith("RNF"), k))
    md = ["# Matriz de trazabilidad de cambios aprobados", "",
          "Proyecto: %s. Reunión del CCB: %s. Generada por `generar_matriz.py` a partir de `cambios_aprobados.json`, el backlog y las marcas `@trace` del prototipo." % (datos["proyecto"], datos["fecha_ccb"]), "",
          "## Vista 1. De la RFC a sus artefactos", "",
          "| RFC | Decisión | Plazo | Requisitos | Casos de prueba | Módulos | Documentación | Prototipo (código) |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for fila, c in zip(filas, datos["cambios_aprobados"]):
        md.append("| **%s** %s | %s | %s | %s | %s | %s | %s | %s |" % (
            fila["rfc"], fila["titulo"], fila["decision"], fila["plazo"], ", ".join(c["requisitos"]),
            "<br>".join(c["tc"]), "<br>".join(c["modulos"]), "<br>".join(c["docs"]), fila["prototipo"].replace("; ", "<br>")))
    md += ["", "## Vista 2. Del requisito a las RFC aprobadas", "", "| Requisito | Título en el backlog | RFC aprobadas que lo cambian | Elementos del prototipo que lo implementan |", "| --- | --- | --- | --- |"]
    for r in orden:
        md.append("| %s | %s | %s | %s |" % (r, backlog[r], ", ".join(inv[r]), ", ".join(codigo.get(r, [])) or "—"))
    md += ["", "## RFC que no se aprobaron", "", "| RFC | Decisión | Votos | Motivo |", "| --- | --- | --- | --- |"]
    for o in datos["no_aprobados"]:
        md.append("| %s %s | %s | %s | %s |" % (o["rfc"], o["titulo"], o["decision"], o["votos"], o["motivo"]))
    (AQUI / "Matriz_trazabilidad.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("OK: %d RFC aprobadas, %d requisitos distintos, %d requisitos con código en el prototipo" % (len(filas), len(inv), sum(1 for r in inv if r in codigo)))


if __name__ == "__main__":
    main()
