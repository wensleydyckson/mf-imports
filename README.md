# Caderno MF Imports

App de controle de compras, vendas parceladas, estoque e cobranças, feito para
rodar no iPhone. É um site estático: um único `index.html`, sem servidor, sem
banco de dados, sem custo.

**Os dados ficam salvos no próprio aparelho**, no navegador em que o app é
aberto. Não vão para lugar nenhum e não sincronizam entre celular e computador.
Por isso o backup importa — veja o final deste arquivo.

---

## Publicar no GitHub Pages

### Caminho A — pelo site do GitHub, sem linha de comando

1. Entre em <https://github.com> e crie uma conta, se ainda não tiver.
2. Clique em **New repository** (ou <https://github.com/new>).
   - **Repository name:** `mf-imports`
   - Deixe em **Public** (o GitHub Pages gratuito só publica repositório público).
   - Não marque nenhuma opção de inicialização. Clique em **Create repository**.
3. Na tela seguinte, clique em **uploading an existing file**.
4. Arraste para lá **todos os arquivos desta pasta**:

   ```
   index.html
   manifest.webmanifest
   sw.js
   favicon.png
   icon-192.png
   icon-512.png
   apple-touch-icon.png
   logo.png
   .nojekyll
   README.md
   ```

   > `logo.png` (1024px) é o logo dela recortado e limpo, guardado aqui como
   > arquivo da marca. O app não depende dele — a imagem já vai embutida no
   > `index.html` —, mas serve para posts, etiqueta e o que mais precisar.

   > O `.nojekyll` costuma ficar escondido no Explorer do Windows. Em
   > **Exibir → Mostrar → Itens ocultos** ele aparece. Se não conseguir enviar,
   > tudo bem: o app funciona sem ele.

5. Clique em **Commit changes**.
6. Vá em **Settings → Pages** (menu da esquerda).
   - **Source:** `Deploy from a branch`
   - **Branch:** `main` e pasta `/ (root)` → **Save**.
7. Espere de 1 a 3 minutos e recarregue a página. O endereço aparece no topo:

   ```
   https://SEU-USUARIO.github.io/mf-imports/
   ```

Esse é o link para mandar no WhatsApp dela.

### Caminho B — pela linha de comando

Esta pasta já é um repositório Git com o primeiro commit feito. Crie o
repositório vazio no GitHub (passo 2 acima) e depois, aqui dentro:

```bash
git remote add origin https://github.com/SEU-USUARIO/mf-imports.git
git push -u origin main
```

Depois faça o passo 6 (**Settings → Pages**).

---

## Instalar no iPhone

Tem que ser no **Safari** — no iPhone o Chrome não instala app na tela de início.

1. Abrir o link no Safari.
2. Botão de **compartilhar** (o quadrado com a seta pra cima, na barra de baixo).
3. Rolar e tocar em **Adicionar à Tela de Início**.
4. Nome: **MF Imports** → **Adicionar**.

Vira um ícone igual a qualquer outro app, abre em tela cheia e funciona mesmo
sem internet.

---

## Publicar uma versão nova

> O `index.html` é **gerado**. Não edite ele: a fonte é o `caderno.html`, que
> fica um nível acima desta pasta e tem cópia versionada em [`fonte/`](fonte/).
> O [`fonte/CLAUDE.md`](fonte/CLAUDE.md) explica o projeto inteiro.

1. Edite o `caderno.html` e suba o `VERSAO` dentro dele (`AAAA.MM.DD-n`).
2. Suba o cache no `sw.js`:

   ```js
   const CACHE = "mf-imports-v8";   →   const CACHE = "mf-imports-v9";
   ```

   Sem isso, quem já instalou continua vendo a versão antiga, porque o app
   guarda uma cópia local para funcionar offline.
3. Rode `python build.py` na raiz do projeto e dê `git push` aqui dentro.

Para conferir se chegou (o GitHub leva 1 a 3 minutos), abra o app, vá em
**Mais** e veja se o número da versão bate.

---

## Backup

Como os dados moram só no aparelho, **backup não é opcional**. O app ajuda de
três formas, em **Mais → Backup e exportação**:

- **Enviar backup agora** — um toque abre a folha de compartilhamento do iPhone.
  Dá para mandar no WhatsApp, por e-mail ou salvar nos Arquivos / iCloud Drive.
  É o caminho mais rápido: mande para si mesmo uma vez por mês.
- **Lembrete automático** — passados 30 dias sem backup, aparece um aviso
  vermelho na tela de Resumo até ela fazer.
- **Cópia do início do dia** — o app guarda sozinho como tudo estava antes da
  primeira alteração de cada dia. Desfaz uma importação errada ou algo apagado
  sem querer. Não substitui o backup: essa cópia mora no mesmo aparelho e some
  junto com ele.

E as exportações de sempre:

| Arquivo | Serve para |
|---|---|
| Planilha de vendas (CSV) | Abrir no Excel / Google Sheets, mandar para o contador |
| Planilha de parcelas (CSV) | Conferir o que está a receber e a pagar |
| Backup completo (JSON) | Restaurar tudo, inclusive num celular novo |

O JSON é o que importa: guarde uma cópia por mês no e-mail ou no Google Drive.
Para restaurar, abra o arquivo, copie o conteúdo e cole em
**Mais → Backup → Restaurar backup**.

Apagar o histórico do Safari com a opção "dados de sites" limpa os dados do app.
Trocar de celular sem backup também perde tudo.
