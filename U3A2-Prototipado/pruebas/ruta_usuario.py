# Mide acciones y tiempo de las 4 tareas del protocolo con el prototipo real (ruta directa, sin ayuda).
import json, os, time
from playwright.sync_api import sync_playwright
AQUI = os.path.dirname(os.path.abspath(__file__))
URL = "file://" + os.path.join(AQUI, "..", "prototipo", "index.html"); out = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_context(viewport={"width":1100,"height":800}).new_page()
    def tarea(k, f):
        pg.goto(URL); pg.evaluate("localStorage.clear()"); pg.reload(); pg.wait_for_selector("nav a")
        n = [0]; t = time.time(); f(n); out[k] = dict(acciones=n[0], ms=int((time.time()-t)*1000))
    def c(sel, n, **k): pg.locator(sel).first.click(**k); n[0] += 1
    def T1(n):
        c("tbody tr:nth-child(1) a.btn", n); pg.wait_for_selector("#esc"); c("tr.rec button", n); pg.wait_for_selector("dialog[open]"); c("#ok", n); pg.wait_for_selector("#toast:visible")
    def T2(n):
        c("tbody tr:nth-child(2) a.btn", n); pg.wait_for_selector("#esc"); pg.locator("tbody tr button").last.click(); n[0]+=1
        pg.wait_for_selector("#motivo"); pg.fill("#motivo","Descanso reglamentario"); n[0]+=1; c("#ok", n); pg.wait_for_selector("#toast:visible")
    def T3(n):
        pg.select_option("#rol","tripulante"); n[0]+=1; pg.select_option("#quien","T2:p"); n[0]+=1
        c("nav a:has-text('Todos')", n); pg.wait_for_selector("table"); c("tbody tr:nth-child(4) a.btn", n); pg.wait_for_selector("h2")
        assert "Meteorología prevista" in pg.locator("main").inner_text()
    def T4(n):
        pg.select_option("#rol","admin"); n[0]+=1; pg.wait_for_selector("#fres"); pg.select_option("#re","E2"); n[0]+=1
        pg.fill("#rv","90"); n[0]+=1; pg.fill("#rf","2026-10-10"); n[0]+=1; c("button[type=submit]", n); pg.wait_for_selector("#toast:visible")
    for k,f in (("T1",T1),("T2",T2),("T3",T3),("T4",T4)): tarea(k,f)
    b.close()
json.dump(out, open(os.path.join(AQUI, "ruta_usuario.json"),"w"), indent=1); print(out)
