# 🛠️ Game Dev Toolkit - Python & Automation Scripts

> **Contexto:** Conjunto de ferramentas desenvolvidas para automatizar o pipeline de criação de assets e level design do meu jogo de navegador (Poke Stream).

## 📖 Sobre o Repositório e a Metodologia GenAI
Durante o desenvolvimento de um jogo Full Stack, percebi que tarefas manuais (como baixar 1000 sprites, renomear arquivos ou mapear coordenadas) consumiam muito tempo.

Para resolver isso, atuei como **Arquiteto de Soluções**, definindo a lógica necessária para cada gargalo e utilizando **GenAI (Inteligência Artificial Generativa)** para acelerar a codificação das ferramentas.

* **Meu Papel:** Identificação do problema, definição dos requisitos (ex: "O script precisa ler a pasta X e centralizar a imagem num canvas Y") e validação dos resultados.
* **Papel da IA:** Geração da sintaxe em Python/JS, criação de interfaces gráficas (GUI) com CustomTkinter e otimização de algoritmos.

---

## 🧰 Ferramentas de Processamento de Imagem (Assets Pipeline)

### 1. Canvas Scaler (`canvascale.py`)
**Problema:** Os sprites originais possuem tamanhos variados (ex: um Caterpie é 30x30px, um Onix é 150x150px), o que quebrava o layout CSS.
**Solução:**
* Script que processa GIFs em lote.
* Cria um "canvas" transparente padrão (250x210px).
* Centraliza automaticamente o sprite original dentro dessa área segura.
* **Tech:** Python, Pillow (PIL), Threading (para não travar a UI).

### 2. Pixel Scan & Offset Detector (`pixelscan.py`)
**Problema:** Ao posicionar os sprites na batalha, alguns pareciam "flutuar" ou "afundar" no chão.
**Solução:**
* Analisa pixel a pixel cada frame do GIF.
* Detecta automaticamente a coordenada Y do pixel mais baixo (o "pé" do sprite).
* Permite visualização e exportação desses dados para Excel (XLSX) para serem usados no ajuste de posicionamento no jogo.
* **Tech:** CustomTkinter, OpenPyXL, ImageSequence.

### 3. Resolution Analyst (`resolutionanalyst.py`)
**Problema:** Necessidade de entender a variância de tamanho dos assets para definir o layout da UI.
**Solução:**
* Analisa uma pasta inteira de imagens/GIFs.
* Identifica os extremos: Maior Largura/Altura e Menor Largura/Altura.
* Exibe visualmente os "vencedores" e lida com empates.

### 4. Sprite Scraper (`alldownloadimage.py`)
**Função:** Bot de Web Scraping que automatiza o download de milhares de sprites (ex: variações Shiny/Back) diretamente de repositórios públicos, salvando-os organizadamente.
* **Tech:** Requests, BeautifulSoup4.

---

## 🗺️ Ferramentas de Level Design

### 5. Map Maker (`mapeador.html`)
**Problema:** Escrever coordenadas de mapa (arrays PHP) manualmente era propenso a erros e lento.
**Solução:**
* Ferramenta visual baseada em browser (HTML5/JS).
* Carrega a imagem do mapa do jogo.
* Permite clicar nos "slots" (grid 50x50) para definir propriedades (Água, Terra, Floresta, Pokéstop).
* **Output:** Gera automaticamente o código PHP de configuração (`['c' => 10, 'r' => 5, 'type' => 'water']`) pronto para copiar e colar no Backend.

---

## 📂 Utilitários de Arquivos

* **Batch Renamer (`changename.py`):** Renomeação em massa de arquivos adicionando sufixos (ex: padronizar estados de sprites `_attack`, `_idle`). Possui função "Desfazer" (Undo).
* **File Lister (`listname.py`):** Mapeia recursivamente diretórios de assets e exporta os caminhos relativos para Excel, facilitando a inserção em Banco de Dados.

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.12
* **Interface Gráfica (GUI):** CustomTkinter (Modern UI)
* **Manipulação de Imagem:** Pillow (PIL)
* **Dados:** OpenPyXL (Excel), BeautifulSoup4 (Web Scraping)
* **Web:** HTML5, CSS3, Vanilla JS

---
*Este repositório demonstra minha capacidade de criar soluções ("DevTools") para otimizar o ciclo de desenvolvimento de software.*
