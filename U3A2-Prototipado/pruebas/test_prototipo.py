"""Pruebas automáticas del prototipo (Playwright + Chromium). Uso: python3 test_prototipo.py
Escribe resultados_pruebas.json y las capturas en capturas/."""
import json, sys, os
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
URL = "file://" + os.path.join(AQUI, "..", "prototipo", "index.html")
CAP = os.path.join(AQUI, "capturas")
res = []
REQ={'P01': 'HU-08', 'P02': 'HU-07', 'P03': 'HU-07', 'P04': 'HU-08', 'P05': 'HU-08', 'P06': 'HU-08', 'P07': 'HU-08', 'P08': 'HU-08', 'P09': 'RNF-02', 'P10': 'HU-07', 'P11': 'HU-07', 'P12': 'HU-07', 'P13': 'HU-08', 'P14': 'HU-08', 'P15': 'HU-04', 'P16': 'HU-04', 'P17': 'RNF-01', 'P18': 'HU-05', 'P19': 'Caso: consulta de escenarios', 'P20': 'Caso: consulta de escenarios', 'P21': 'HU-06', 'P22': 'HU-06', 'P23': 'HU-07', 'P24': 'RNF-06', 'P25': 'RNF-06', 'P26': '—', 'P27': '—', 'P28': '—', 'P29': 'RNF-06', 'P30': '—'}
def rec(i, nombre, ok, detalle=""):
    res.append(dict(id=i, req=REQ.get(i,"—"), nombre=nombre, ok=bool(ok), detalle=detalle)); print(("OK  " if ok else "FALLA"), i, nombre, detalle)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome") if os.path.exists("/opt/pw-browsers/chromium-1194/chrome-linux/chrome") else p.chromium.launch()
    ctx = b.new_context(viewport={"width": 1100, "height": 800})
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(URL); pg.wait_for_selector("table")
    rec("P01", "Operador ve la lista de 6 vuelos", pg.locator("tbody tr").count() == 6, str(pg.locator("tbody tr").count()))
    pg.screenshot(path=CAP + "/01_vuelos.png")
    # V101
    pg.goto(URL + "#/vuelo/V101"); pg.wait_for_selector("#esc")
    sug = pg.locator(".box.hl b").inner_text()
    rec("P02", "Se muestra escenario sugerido y ranking", "Sugerido" in sug and pg.locator("tbody tr").count() == 5, sug)
    rec("P03", "Exactamente una tripulación marcada Recomendada (sin empate)", pg.locator(".chip.on").count() == 1)
    top_row = pg.locator("tr.rec").first.inner_text()
    pg.screenshot(path=CAP + "/02_vuelo_ranking.png", full_page=True)
    # asignar la recomendada
    pg.locator("tr.rec button").first.click(); pg.wait_for_selector("dialog[open]")
    rec("P04", "Asignar la recomendada no pide motivo", pg.locator("#motivo").count() == 0)
    pg.screenshot(path=CAP + "/03_confirmar.png")
    pg.click("#ok"); pg.wait_for_selector("#toast:visible")
    rec("P05", "Confirmación muestra aviso de notificación", "notificará" in pg.locator("#toast").inner_text())
    pg.wait_for_selector("table")
    estado = pg.locator("tbody tr").nth(0).inner_text()
    rec("P06", "El vuelo pasa a Asignado en la lista", "Asignado" in estado, estado.replace("\n", " | "))
    # no top sin motivo
    pg.goto(URL + "#/vuelo/V102"); pg.wait_for_selector("#esc")
    btns = pg.locator("tbody tr button"); n = btns.count()
    btns.nth(n - 1).click(); pg.wait_for_selector("dialog[open]")
    rec("P07", "Elegir una tripulación que no es la de mayor puntuación exige motivo", pg.locator("#motivo").count() == 1)
    pg.click("#ok")
    rec("P08", "Sin motivo se bloquea con mensaje de error", "motivo" in pg.locator("#merr").inner_text().lower() and pg.locator("dialog[open]").count() == 1, pg.locator("#merr").inner_text())
    pg.screenshot(path=CAP + "/04_motivo_error.png")
    pg.fill("#motivo", "Descanso reglamentario de la tripulación recomendada"); pg.click("#ok"); pg.wait_for_selector("#toast:visible")
    pg.goto(URL + "#/auditoria"); pg.wait_for_selector("table")
    rec("P09", "El historial registra las 2 asignaciones con su motivo", pg.locator("tbody tr").count() == 2 and "Descanso" in pg.locator("tbody").inner_text())
    # empate E3
    pg.goto(URL + "#/vuelo/V104"); pg.wait_for_selector("#esc")
    rec("P10", "Con empate en la puntuación más alta se avisa al operador", pg.locator(".warn").filter(has_text="Empate").count() == 1, pg.locator(".box.hl b").inner_text())
    rec("P11", "En empate hay más de una tripulación marcada Recomendada", pg.locator(".chip.on").count() == 2, str(pg.locator(".chip.on").count()))
    pg.screenshot(path=CAP + "/05_empate.png", full_page=True)
    # cambiar escenario manualmente
    pg.select_option("#esc", "E1"); pg.wait_for_timeout(100)
    rec("P12", "El operador puede cambiar el escenario y el ranking se recalcula", "Puntuación en E1" in pg.locator("thead").inner_text())
    # reasignación V106
    pg.goto(URL + "#/vuelo/V106"); pg.wait_for_selector("#esc")
    rec("P13", "Un vuelo ya asignado avisa que se registrará como reasignación", pg.locator(".warn").filter(has_text="reasignación").count() == 1)
    # persistencia
    pg.reload(); pg.goto(URL + "#/vuelos"); pg.wait_for_selector("table")
    rec("P14", "La asignación persiste al recargar", "Asignado" in pg.locator("tbody tr").nth(0).inner_text())
    # rol tripulante
    pg.select_option("#rol", "tripulante"); pg.wait_for_selector("table, .box")
    pg.select_option("#quien", "T2:p")
    mis = pg.locator("tbody tr").count()
    rec("P15", "Piloto de T2 ve sus vuelos asignados (V106 y el asignado en la prueba)", mis >= 1, str(mis))
    pg.screenshot(path=CAP + "/06_mis_vuelos.png")
    pg.select_option("#quien", "T1:p")
    t1 = pg.locator("tbody tr").count(); t1txt = pg.locator("main").inner_text()
    rec("P16", "Un piloto sin vuelos asignados ve el mensaje vacío y ninguna fila", t1 == 0 and "No tienes vuelos asignados" in t1txt, "filas: %d" % t1)
    pg.goto(URL + "#/vuelos"); pg.wait_for_timeout(200)
    rec("P17", "Un piloto no accede a la pantalla del operador (RNF-01)", "#/vuelos" not in pg.url or pg.locator("h2").inner_text().startswith("Mis vuelos"), pg.url.split("#")[1])
    pg.goto(URL + "#/todos"); pg.wait_for_selector("table"); pg.locator("tbody a").nth(3).click(); pg.wait_for_selector("h2")
    rec("P18", "Un piloto consulta las características de cualquier vuelo", "Meteorología prevista" in pg.locator("main").inner_text())
    pg.goto(URL + "#/evaluacion"); pg.wait_for_selector("table")
    rec("P19", "El piloto ve su puntuación por escenario", "Mi puntuación" in pg.locator("thead").inner_text())
    pg.select_option("#quien", "T1:c"); pg.wait_for_timeout(100)
    rec("P20", "El copiloto ve los escenarios sin puntuación", "Mi puntuación" not in pg.locator("thead").inner_text())
    # admin
    pg.select_option("#rol", "admin"); pg.wait_for_selector("#fres")
    pg.fill("#rv", "150"); pg.fill("#rf", "2026-10-10"); pg.click("button[type=submit]")
    rec("P21", "Resultado fuera de 0–100 se rechaza con mensaje", "entre 0 y 100" in pg.locator("#rerr").inner_text())
    pg.select_option("#rp", "T5"); pg.select_option("#re", "E3"); pg.fill("#rv", "95"); pg.fill("#rf", "2026-10-10"); pg.click("button[type=submit]")
    pg.wait_for_selector("#toast:visible"); pg.wait_for_selector("#fres")
    rec("P22", "El resultado nuevo queda vigente y el anterior en el historial", "82" in pg.locator("ul").inner_text() and "95" in pg.locator("table").first.inner_text())
    pg.screenshot(path=CAP + "/07_admin.png", full_page=True)
    # el ranking cambió: T5 ahora 95 en E3 -> recomendada en V104
    pg.select_option("#rol", "operador"); pg.goto(URL + "#/vuelo/V104"); pg.wait_for_selector("#esc")
    rec("P23", "El ranking del operador refleja el resultado nuevo (sin empate)", pg.locator(".chip.on").count() == 1 and "Camilo" in pg.locator("tr.rec").inner_text())
    # teclado
    pg.goto(URL + "#/vuelo/V105"); pg.wait_for_selector("#esc")
    pg.locator("tr.rec button").first.focus(); pg.keyboard.press("Enter"); pg.wait_for_selector("dialog[open]")
    pg.keyboard.press("Escape"); pg.wait_for_timeout(100)
    rec("P24", "Se puede abrir y cerrar la confirmación solo con teclado", pg.locator("dialog[open]").count() == 0)
    # móvil
    m = b.new_context(viewport={"width": 375, "height": 740}); mp = m.new_page(); mp.goto(URL + "#/vuelo/V101"); mp.wait_for_selector("#esc")
    over = mp.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    rec("P25", "En móvil (375 px) la página no se desborda horizontalmente", over <= 0, "desborde %d px" % over)
    mp.screenshot(path=CAP + "/08_movil.png", full_page=True)
    # persistencia entre roles / reset
    pg.click("#reset"); pg.click("#rok"); pg.goto(URL + "#/vuelos"); pg.wait_for_selector("table")
    rec("P26", "Restablecer datos devuelve el estado inicial", pg.locator("tbody tr").filter(has_text="Sin asignar").count() == 5)
    pg.click("#reset"); vis = pg.locator("dialog[open]").count(); pg.click("#rno")
    rec("P28", "Restablecer datos pide confirmación antes de borrar", vis == 1)
    mp.goto(URL + "#/vuelo/V101"); mp.wait_for_selector("#esc")
    bx = mp.locator("tr.rec button").first.bounding_box()
    rec("P29", "En móvil el botón Asignar es visible sin desplazar horizontalmente", bx is not None and bx["x"] + bx["width"] <= 375, str(bx))
    dec = mp.evaluate("getComputedStyle(document.querySelector('a.btn')).textDecorationLine") if mp.locator("a.btn").count() else "none"
    mp.goto(URL + "#/vuelos"); mp.wait_for_selector("table")
    dec = mp.evaluate("getComputedStyle(document.querySelector('a.btn')).textDecorationLine")
    rec("P30", "Los enlaces con apariencia de botón no se ven subrayados", dec == "none", dec)
    rec("P27", "Sin errores de consola ni excepciones", len(errs) == 0, "; ".join(errs)[:200])
    b.close()
res.sort(key=lambda r: r["id"])
json.dump(res, open(os.path.join(AQUI, "resultados_pruebas.json"), "w"), ensure_ascii=False, indent=1)
print(sum(r["ok"] for r in res), "/", len(res))
