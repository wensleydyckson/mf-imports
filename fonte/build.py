# -*- coding: utf-8 -*-
"""Gera site/index.html (versao autonoma) a partir de caderno.html."""
import io, os, shutil

RAIZ  = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(RAIZ, "caderno.html")
SITE  = os.path.join(RAIZ, "site")
OUT   = os.path.join(SITE, "index.html")
FONTE = os.path.join(SITE, "fonte")

src = io.open(SRC, encoding="utf-8").read()

# --- 1. separa cabecalho (title/fonts/style) do corpo -----------------------
marca = '<div class="app">'
i = src.index(marca)
cabeca, corpo = src[:i].rstrip(), src[i:].rstrip()

# --- 2. download nativo no lugar da capability de downloads ----------------
antigo = """  let dl = null;
  try { dl = await window.claude.use("downloads"); } catch (e) { dl = null; }
  if (!dl) { mostrarTexto(nome, conteudo); return; }
  try {
    await dl.save({ filename: nome, data: conteudo });
    if (tipo === "json") marcarBackup();
    toast("Arquivo salvo.");
  } catch (e) {
    if (e && e.code === "declined") return;
    mostrarTexto(nome, conteudo);
  }"""
novo = """  try {
    const mime = tipo === "json" ? "application/json" : "text/csv;charset=utf-8";
    const url = URL.createObjectURL(new Blob([conteudo], { type: mime }));
    const a = document.createElement("a");
    a.href = url; a.download = nome; a.rel = "noopener"; a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    setTimeout(function(){ URL.revokeObjectURL(url); a.remove(); }, 5000);
    if (tipo === "json") marcarBackup();
    toast("Arquivo gerado. Procure em Downloads / Arquivos.");
  } catch (e) {
    mostrarTexto(nome, conteudo);
  }"""
assert antigo in corpo, "bloco de download nao encontrado"
corpo = corpo.replace(antigo, novo, 1)

# --- 3. registra o service worker -----------------------------------------
alvo = 'if (window.claude && typeof window.claude.use === "function") iniciarNuvem();'
assert alvo in corpo, "linha de boot nao encontrada"
corpo = corpo.replace(alvo, alvo + """

if ("serviceWorker" in navigator && location.protocol.indexOf("http") === 0) {
  temSW = true;
  /* updateViaCache "none": o proprio sw.js nunca vem do cache do navegador,
     senao o iPhone descobre a versao nova tarde demais. */
  window.addEventListener("load", function(){
    navigator.serviceWorker.register("sw.js", { updateViaCache: "none" })
      .then(function(reg){ if (reg) reg.update().catch(function(){}); })
      .catch(function(){});
  });
  navigator.serviceWorker.addEventListener("controllerchange", function(){
    if (recarregandoPorAtualizacao) return;
    recarregandoPorAtualizacao = true;
    location.reload();
  });
  /* Toda vez que ela volta para o app, checa se saiu versao nova. */
  document.addEventListener("visibilitychange", function(){
    if (!document.hidden) verificarAtualizacao(true);
  });
}""", 1)

# --- 4. monta o documento --------------------------------------------------
HEAD = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="MF Imports - perfumes arabes originais. Controle de compras, vendas parceladas, estoque e cobrancas.">
<meta name="theme-color" content="#0A0908">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<meta name="apple-mobile-web-app-title" content="MF Imports">
<meta name="format-detection" content="telephone=no">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" href="favicon.png" sizes="32x32">
<link rel="icon" href="icon-192.png" sizes="192x192">
<style>
:root{color-scheme:dark}
*{-webkit-tap-highlight-color:transparent}
html,body{margin:0;padding:0}
img{max-width:100%}
[hidden]{display:none!important}
</style>
"""

doc = HEAD + cabeca + "\n</head>\n<body>\n" + corpo + "\n</body>\n</html>\n"

io.open(OUT, "w", encoding="utf-8", newline="\n").write(doc)
print("index.html:", len(doc), "bytes")

# A fonte tambem entra no repositorio, para que nada viva so fora do git.
# Sao copias geradas: edite sempre os originais na raiz do projeto.
os.makedirs(FONTE, exist_ok=True)
for nome in ("caderno.html", "build.py", "CLAUDE.md"):
    origem = os.path.join(RAIZ, nome)
    if os.path.exists(origem):
        shutil.copyfile(origem, os.path.join(FONTE, nome))
        print("fonte:", nome)

io.open(os.path.join(FONTE, "LEIA-ME.md"), "w", encoding="utf-8", newline="\n").write(
    "# Fonte\n\n"
    "Copias geradas pelo `build.py` a cada publicacao, para que nada viva so fora\n"
    "do controle de versao. **Nao edite nada aqui**: os originais ficam na raiz do\n"
    "projeto, um nivel acima de `site/`.\n\n"
    "- `caderno.html` - a fonte unica do app. Gera o `site/index.html`.\n"
    "- `build.py` - o gerador.\n"
    "- `CLAUDE.md` - como mexer no projeto.\n")
