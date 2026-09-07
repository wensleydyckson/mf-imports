# Caderno MF Imports

App de controle para a **MF Imports**, revenda informal de perfumes árabes:
compras no distribuidor, vendas parceladas, estoque, contas a receber e a pagar.
A dona usa no iPhone, instalado na tela de início. Idioma: **português do
Brasil**, em toda a interface, nos comentários e nos commits.

## As duas versões

O mesmo app é publicado em dois lugares, a partir de **uma única fonte**:

| Onde | O quê | Para quem |
|---|---|---|
| `caderno.html` → **Artifact da Claude** | publicado direto | testes rápidos e histórico de versões |
| `caderno.html` → `build.py` → `site/index.html` → **GitHub Pages** | <https://wensleydyckson.github.io/mf-imports/> | é este que ela usa |

**`site/index.html` é gerado. Nunca edite esse arquivo** — a próxima build
apaga a alteração. Edite `caderno.html` e rode `python build.py`.

`site/fonte/` guarda cópias de `caderno.html`, `build.py` e `CLAUDE.md`, criadas
pela build a cada publicação, só para que a fonte não viva fora do git. Também
não se edita nada lá.

## O que a build faz

`build.py` lê `caderno.html` e produz o site autônomo:

1. Separa cabeçalho e corpo e embrulha num documento HTML completo, com as
   metatags de PWA (`apple-mobile-web-app-*`, manifest, ícones).
2. Troca o download via capability da Claude por um download nativo com Blob.
3. Injeta o registro do service worker, com `updateViaCache: "none"`,
   `update()` no load e a cada `visibilitychange`, e reload no
   `controllerchange`.
4. Copia a fonte para `site/fonte/`.

## Publicar

Sempre os quatro passos, na ordem:

1. Editar `caderno.html`.
2. Subir `VERSAO` em `caderno.html` (formato `AAAA.MM.DD-n`).
3. Subir `CACHE` em `site/sw.js` (`mf-imports-vN` → `vN+1`).
4. `python build.py`, publicar o Artifact, e `git push` dentro de `site/`.

**Pular o passo 3 é o erro clássico**: quem já instalou continua recebendo a
versão antiga e parece que o deploy não saiu.

O `gh` está instalado em `C:\cloudflared\gh\bin`, **fora do PATH**, já
autenticado como `wensleydyckson`. Use assim:

```bash
export PATH="/c/cloudflared/gh/bin:$PATH"
```

Depois de publicar, confirme que chegou de verdade — o build do Pages demora
1–3 minutos:

```bash
curl -s -L "https://wensleydyckson.github.io/mf-imports/sw.js?x=$RANDOM" | grep -o 'mf-imports-v[0-9]*'
```

## Como os dados são guardados

Tudo no **`localStorage` do aparelho**. Não há servidor nem banco na nuvem.

| Chave | Conteúdo |
|---|---|
| `mf_imports_v1` | os dados: `produtos`, `clientes`, `fornecedores`, `compras`, `vendas` |
| `mf_imports_snap` | como estava no início do dia, para desfazer estrago |
| `mf_imports_cfg` | por aparelho: data do último backup, exemplos escondidos |

O código de sincronia com o `db` da Claude existe e funciona no Artifact; no
site ele fica inerte, porque `window.claude` não existe lá.

**Banco na nuvem foi oferecido em 07/09/2026 e adiado** — resolveria backup
automático, multi-aparelho e acompanhamento à distância de uma vez. Não
reproponha sem motivo novo; os gatilhos são ela querer usar em mais de um
aparelho, ou ele querer acompanhar de longe.

## Regras do domínio

**O celular é a identidade do cliente.** Ninguém nessa clientela quer dar CPF.
`normTel()` normaliza (tira o 55, guarda só os dígitos), então `(11) 96666-5555`
e `11966665555` caem na mesma ficha. É obrigatório na venda, com DDD. Nome não
identifica: um apelido digitado às pressas **não** sobrescreve um nome já
cadastrado — só completa quando o guardado é um placeholder.

**Cada venda é uma Ordem de Compra** numerada (`OC-0001`). Vendas anteriores à
numeração ganham OC em ordem de data, uma vez só.

**Cartão de crédito na venda é à vista** — ela recebe de uma vez. Só
promissória entra em contas a receber. Há um botão para o caso raro de a
maquininha depositar parcelado. Na compra, cartão continua parcelado, porque aí
ela paga mesmo mês a mês.

**Precedência do custo**, nessa ordem: compra registrada (média ponderada) →
custo da ficha do perfume → último custo gravado numa venda. A ficha avisa qual
está valendo.

**Perfume nasce da compra**, ou de "Outro perfume (digitar)" na venda. Não
existe cadastro avulso: o botão do Estoque é *Nova compra*.

## Armadilhas que já custaram caro

Todas apareceram só no iPhone real. Teste em navegador de desktop não pega
nenhuma delas.

- **`confirm()` nativo não aparece em app instalado.** Todo botão destrutivo
  virava um toque morto, sem erro. Use `perguntar()`, o diálogo próprio que
  devolve promessa. Não reintroduza `confirm()`.
- **Número truncado.** `.item-s` tem `text-overflow: ellipsis`. Não ponha
  valores em texto corrido: use as colunas (`.precos`). Foi o que fez o custo
  "sumir" do estoque quando a marca era longa.
- **Dados de exemplo parecendo reais.** O app mostra demonstração quando não há
  cadastro. Isso confundiu o próprio dono, que achou o app quebrado. Hoje o
  aviso é evidente e dispensável em *Começar do zero*; **Mais** mostra a
  contagem real.
- **O iOS segura a versão antiga.** Por isso `VERSAO` aparece em **Mais** e
  existe *Buscar versão nova*, que limpa cache e service worker sem tocar nos
  dados. Ao investigar "não subiu", peça primeiro o número da versão.
- **`datalist` é ruim no Safari do iPhone.** Perfume e afins usam `<select>`.
- **Ouvintes acumulados.** `abrirSheet()` troca o corpo por um clone vazio; sem
  isso os ouvintes da tela anterior brigavam pelo mesmo clique.
- **Escapes `\uXXXX`** aparecem literais no arquivo em alguns trechos. São
  válidos dentro de string JS. Ao casar texto num patch, confira se o arquivo
  guarda o escape ou o acento.

## Como testar

O app é um arquivo só, sem framework nem build de JS. Para exercitar:

```bash
python -c "import io;s=io.open('caderno.html',encoding='utf-8').read();i=s.index('<script>')+8;j=s.rindex('</script>');io.open('app.js','w',encoding='utf-8',newline='\n').write(s[i:j])"
node --check app.js
```

Depois suba o site (`.claude/launch.json` tem a configuração `site`, que serve
`site/` na porta 4173) e dirija a página por script, com `window.confirm`
neutralizado para simular o app instalado:

```js
window.confirm = () => undefined;
```

Confira sempre na **largura de 375px**, que é onde os problemas de layout
aparecem.
