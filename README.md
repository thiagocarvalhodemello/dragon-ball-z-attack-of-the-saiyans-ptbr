# Dragon Ball Z: Attack of the Saiyans — Tradução Português do Brasil (PT-BR)

[![GitHub Releases](https://img.shields.io/github/v/release/thiagocarvalhodemello/dragon-ball-z-attack-of-the-saiyans-ptbr?style=flat-square)](https://github.com/thiagocarvalhodemello/dragon-ball-z-attack-of-the-saiyans-ptbr/releases)
[![Platform](https://img.shields.io/badge/platform-Nintendo%20DS-red.svg?style=flat-square)](#)
[![Language](https://img.shields.io/badge/language-Portugu%C3%AAs%20(PT--BR)-green.svg?style=flat-square)](#)

Guia completo de análise técnica, documentação do projeto de tradução e instruções detalhadas para aplicação de patch no jogo **Dragon Ball Z: Attack of the Saiyans** (*Dragon Ball Kai: Saiyan Invasion*), lançado para o **Nintendo DS** em 2009 e desenvolvido pela conceituada **Monolith Soft**.

---

## 📋 Sumário
1. [Análise Técnica do Jogo e da ROM](#1-análise-técnica-do-jogo-e-da-rom)
   - [Arquitetura do Motor (Monolith Soft)](#arquitetura-do-motor-monolith-soft)
   - [Sistema de Arquivos NitroFS](#sistema-de-arquivos-nitrofs)
   - [Estrutura de Scripts e Diálogos (.sb)](#estrutura-de-scripts-e-diálogos-sb)
   - [Banco de Dados de Batalha (BDAT)](#banco-de-dados-de-batalha-bdat)
   - [Mapas e Eventos de Campo (.map)](#mapas-e-eventos-de-campo-map)
   - [Tipografia e Fontes (.fnt)](#tipografia-e-fontes-fnt)
   - [Interface Gráfica e Menus (.img / .chr / .a)](#interface-gráfica-e-menus-img--chr--a)
   - [Análise Regional: USA (BRPE) vs Europa (BRPP)](#análise-regional-usa-brpe-vs-europa-brpp)
2. [Escopo e Progresso da Tradução](#2-escopo-e-progresso-da-tradução)
3. [Arquivos de Patch Disponíveis](#3-arquivos-de-patch-disponíveis)
4. [Tabela de Hashes e Verificação de Integridade](#4-tabela-de-hashes-e-verificação-de-integridade)
5. [Como Aplicar o Patch (3 Métodos)](#5-como-aplicar-o-patch-3-métodos)
   - [Método 1: Aplicador Automático em Python (Recomendado)](#método-1-aplicador-automático-em-python-recomendado)
   - [Método 2: Patcher Online no Navegador (Rom Patcher JS)](#método-2-patcher-online-no-navegador-rom-patcher-js)
   - [Método 3: Ferramentas Desktop (Floating IPS / FLIPS / UniPatcher)](#método-3-ferramentas-desktop-floating-ips--flips--unipatcher)
6. [Instruções de Emulação e Flashcards](#6-instruções-de-emulação-e-flashcards)
7. [Solução de Problemas (Troubleshooting)](#7-solução-de-problemas-troubleshooting)
8. [Créditos e Agradecimentos](#8-créditos-e-agradecimentos)

---

## 1. Análise Técnica do Jogo e da ROM

### Arquitetura do Motor (Monolith Soft)
Desenvolvido pela Monolith Soft (famosa por *Xenoblade Chronicles*, *Baten Kaitos* e *Soma Bringer*), *Dragon Ball Z: Attack of the Saiyans* é um RPG por turnos de ritmo dinâmico que utiliza uma versão refinada do motor proprietário para Nintendo DS da desenvolvedora. O jogo opera em uma resolução nativa de 256×192 pixels por tela e gerencia eventos, combate e áudio através de subsistemas modulares.

### Sistema de Arquivos NitroFS
O arquivo de ROM (.nds) segue o padrão **NitroFS** (Nitro File System) composto por:
* **Cabeçalho da ROM (0x000..0x200):** Contém títulos, identificadores de região, ponteiros ARM9/ARM7 e a soma de checagem do cabeçalho (CRC16 em `0x15E`).
* **FAT (File Allocation Table):** Localizada a partir de `0x0E6200`, armazena pares de endereços de início e término (`uint32 start`, `uint32 end`) para os 7.010 arquivos do jogo.
* **FNT (File Name Table):** Localizada a partir de `0x0CE600`, organiza os diretórios hierárquicos e associa cada nome de arquivo a um índice sequencial na FAT.

### Estrutura de Scripts e Diálogos (.sb)
Os arquivos de script com extensão `.sb` controlam o fluxo de enredo, cutscenes, caixas de diálogo e comandos de ação dos personagens.
* **Assinatura:** Iniciam com o cabeçalho binário `SB  \x01\x00\x01\x00`.
* **Tabela de Seções:** Possui ponteiros de deslocamento para tabelas de bytecode, tabelas de variáveis e blocos de strings.
* **Códigos de Controle de Texto:**
  * `<p>`: Início de parágrafo / nova caixa de texto.
  * `<k>`: Aguarda toque de botão pelo jogador para continuar.
  * `<n>`: Quebra de linha manual.
  * `<c X>`: Alteração dinâmica da paleta de cores da fonte.
* **Repontamento:** Como as frases em português brasileiro exigem geralmente 15% a 30% mais caracteres que em inglês, os scripts expandidos foram realocados no espaço de padding final da ROM (`0x7000000+`), atualizando a tabela FAT de cada arquivo sem quebrar a integridade das chamadas.

### Banco de Dados de Batalha (BDAT)
O arquivo `btl/bdat/*/bdat.bin` armazena todos os parâmetros estruturados de batalha utilizando o formato binário proprietário **BDAT** da Monolith Soft:
* Nomes, multiplicadores de dano e custo de Ki/AP de habilidades especiais (Kamehameha, Masenko, Galick Gun, Spirit Ball).
* Nomes, efeitos e probabilidades de itens consumíveis e equipamentos.
* Estatísticas, parâmetros de chefes (Raditz, Nappa, Vegeta, Broly secreto) e mensagens de status do sistema.

### Mapas e Eventos de Campo (.map)
Os mapas do mundo e áreas exploráveis (`fld/map/C**/*_9999*.map`) combinam dados geométricos de colisão, posicionamento de baús e tabelas de identificação de NPCs locais e diálogos contextuais.

### Tipografia e Fontes (.fnt)
O jogo utiliza tabelas de fontes de largura variável (VWF) em `latin0.fnt` e `latin1.fnt`. Essas fontes foram mapeadas para permitir a correta renderização de todos os caracteres acentuados próprios da língua portuguesa (á, é, í, ó, ú, â, ê, ô, ã, õ, ç, Á, É, Í, Ó, Ú, Â, Ê, Ô, Ã, Õ, Ç).

### Interface Gráfica e Menus (.img / .chr / .a)
* **`.img` / `.chr`:** Arquivos de tiles gráficos e paletas do menu de itens, tela de status, árvores de habilidades, números de dano (`dmgnum.chr`) e botões de comando.
* **`.a`:** Arquivos de animação gráfica comprimida (como `sp_cloth_*.a`).
* **Telas de Capítulos:** Imagens gráficas que exibem o nome de cada episódio ao iniciar novas partes da história.

### Análise Regional: USA (BRPE) vs Europa (BRPP)
Existe uma diferença crucial entre as versões comercializadas no Ocidente:
1. **Versão Americana (`BRPE`):** Utiliza exclusivamente os recursos identificados pelo sufixo `us` (`script/US/`, `btl/bdat/US/bdat.bin`, `fld/map/*_9999us.map`, `menu/icon/*_us.img`).
2. **Versão Europeia (`BRPP`):** Multi-idiomas (Inglês, Francês, Alemão, Espanhol, Italiano). Contém tanto diretórios `US` quanto `EN`. Quando o console está configurado em inglês, a ROM europeia requisita preferencialmente os arquivos de sufixo `en` (`script/EN/`, `btl/bdat/EN/bdat.bin`, `menu/icon/*_en.img`).
3. **Solução Implementada neste Projeto:**
   * Fornecimento do patch oficial para a versão USA (`DBZ_Attack_of_the_Saiyans_PTBR.bps`).
   * Criação do patch específico para a versão Europeia (`DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps`), que espelha todas as modificações traduzidas tanto para os índices `US` quanto `EN` e recalcula o CRC16 de cabeçalho (`0x15E`), garantindo funcionamento pleno independente da região da ROM do usuário.

---

## 2. Escopo e Progresso da Tradução

| Componente | Progresso | Detalhes |
| :--- | :---: | :--- |
| **História Principal e Cutscenes** | **100%** | Todos os diálogos da trama original traduzidos e adaptados |
| **NPCs e Diálogos de Campo** | **100%** | Todas as interações com cidadãos, mestres e personagens secundários |
| **Missões Secundárias e Objetivos** | **100%** | Diário de missões, tarefas de busca e objetivos de mapa |
| **Itens, Acessórios e Consumíveis** | **100%** | Descrições completas, efeitos e nomes localizados |
| **Habilidades, Técnicas e Ultimates** | **100%** | Ataques individuais e Combos Sparking / Blast Combos |
| **Inimigos, Chefes e Bestiário** | **100%** | Nomes de monstros, soldados de Freeza, Saiyajins e chefes opcionais |
| **Menus em Texto e Telas de Status** | **100%** | Equipamento, árvore de pontos AP, cápsulas e tutoriais |
| **Interface Gráfica e Ícones** | **100%** | Botões, títulos de menu e imagens gráficas traduzidas |
| **Cartões de Título dos Capítulos** | **100%** | Telas de transição de episódio adaptadas |

---

## 3. Arquivos de Patch Disponíveis

No diretório do projeto, você encontrará os seguintes patches no formato moderno **BPS** (*Beat Patch System*):

* **`DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps`**
  * **Destinado a:** ROM Europeia (`Dragon Ball Z - Attack of the Saiyans (Europe) (En,Fr,De,Es,It).nds`).
  * **Base CRC32:** `4E8C3E1B`
  * **ROM Traduzida Resultante:** `Dragon Ball Z - Attack of the Saiyans (EUR) (PT-BR).nds` (CRC32: `7A2AA658`).

* **`DBZ_Attack_of_the_Saiyans_PTBR.bps`**
  * **Destinado a:** ROM Americana (`Dragon Ball Z - Attack of the Saiyans (USA) (En,Fr).nds`).
  * **Base CRC32:** `A9F0B8F9`
  * **ROM Traduzida Resultante:** `Dragon Ball Z - Attack of the Saiyans (USA) (PT-BR).nds` (CRC32: `28E6DC1E`).

---

## 4. Tabela de Hashes e Verificação de Integridade

Utilize esta tabela para confirmar que seus arquivos originais e traduzidos estão 100% íntegros:

### ROMs Originais (Base)
| Região | Nome Padrão do Arquivo | Tamanho | CRC32 | MD5 |
| :--- | :--- | :---: | :---: | :--- |
| **Europa** | `Dragon Ball Z - Attack of the Saiyans.nds` | 134.217.728 bytes | `4E8C3E1B` | `b6d67064618109c4edf675f3275b87db` |
| **USA** | `Dragon Ball Z - Attack of the Saiyans (USA) (En,Fr).nds` | 134.217.728 bytes | `A9F0B8F9` | `9c83a44ca1880d813eeb1c968dc6931f` |

### Arquivos de Patch (.bps)
| Patch | Tamanho | CRC32 | MD5 |
| :--- | :---: | :---: | :--- |
| `DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps` | 11.146.255 bytes | `2144DF1C` | `1675d5f9f03df9fbc6164a213278e60d` |
| `DBZ_Attack_of_the_Saiyans_PTBR.bps` | 3.966.119 bytes | `2144DF1C` | `d36d9a747c119c84da2148e527c22ec2` |

### ROMs Finais Traduzidas (PT-BR)
| Versão | Tamanho | CRC32 | MD5 | SHA-256 |
| :--- | :---: | :---: | :--- | :--- |
| **EUR Patched** | 134.217.728 bytes | `7A2AA658` | `d7cf6ee65920cf334ad29d5a4c843556` | `2419be4115821639dabe512b71a5b99d214f37adff277c0f1630cf2ed606c936` |
| **USA Patched** | 134.217.728 bytes | `28E6DC1E` | `6a0a40dde7c553710588f7ffe21cf236` | `0f1c3e1567dc437d106a1705c3160d5cd7b6401d09d65b4deb6318ad204dd29f` |

---

## 5. Como Aplicar o Patch (3 Métodos)

### Método 1: Aplicador Automático em Python (Recomendado)
O projeto inclui o script [`apply_patch.py`](file:///C:/Development/roms-nds/Dragon%20Ball%20Z%20-%20Attack%20of%20the%20Saiyans/apply_patch.py) que identifica automaticamente se sua ROM é Americana ou Europeia e gera a ROM traduzida em poucos segundos:

1. Abra o terminal (PowerShell, Prompt de Comando ou Terminal Bash) nesta pasta.
2. Execute o comando:
   ```powershell
   python apply_patch.py
   ```
3. O script lerá a ROM, checará os checksums, aplicará o patch correto e salvará a nova ROM traduzida com verificação completa.
4. Caso sua ROM esteja em outra pasta, passe o caminho como argumento:
   ```powershell
   python apply_patch.py "C:\caminho\para\sua_rom.nds"
   ```

---

### Método 2: Patcher Online no Navegador (Rom Patcher JS)
Não é necessário instalar nenhum software adicional; funciona no computador, celular ou tablet:

1. Acesse o site gratuito **[Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/)**.
2. No campo **ROM file**, clique em *Escolher arquivo* e selecione sua ROM original `.nds`.
3. No campo **Patch file**, selecione o arquivo de patch `.bps` correspondente:
   * Se sua ROM for a versão Europeia (`CRC32 4E8C3E1B`): selecione `DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps`.
   * Se sua ROM for a versão Americana (`CRC32 A9F0B8F9`): selecione `DBZ_Attack_of_the_Saiyans_PTBR.bps`.
4. Clique no botão verde **Apply patch**.
5. O navegador baixará o novo arquivo `.nds` traduzido.

---

### Método 3: Ferramentas Desktop (Floating IPS / FLIPS / UniPatcher)
* **No Windows:**
  1. Baixe o **Floating IPS (Flips)**.
  2. Execute o programa e clique em **Apply Patch**.
  3. Selecione o arquivo `.bps` desejado.
  4. Selecione sua ROM original limpa `.nds`.
  5. Escolha o nome e o local onde a nova ROM traduzida será salva.
* **No Android:**
  1. Instale o aplicativo gratuito **UniPatcher** (Google Play Store).
  2. Em *Patch file*, selecione o arquivo `.bps`.
  3. Em *ROM file*, selecione sua ROM original `.nds`.
  4. Em *Output file*, defina onde salvar e toque no ícone de salvar (disquete) para aplicar.

---

## 6. Instruções de Emulação e Flashcards

A ROM traduzida é totalmente compatível com todos os ambientes de execução de Nintendo DS:

### Computador (Windows / macOS / Linux)
* **MelonDS (Altamente Recomendado):** Oferece emulação com precisão de ciclo de clock, suporte a renderização OpenGL/software e excelente áudio.
* **DeSmuME:** Funciona perfeitamente. Recomendado configurar o filtro de textura para *Bilinear* e sincronização de áudio ativada.
* **RetroArch:** Utilize o núcleo `MelonDS DS` ou `DeSmuME`.

### Dispositivos Móveis (Android / iOS)
* **Delta (iOS):** Adicione a ROM `.nds` traduzida diretamente ao aplicativo via iTunes ou aplicativo Arquivos.
* **DraStic (Android):** Emulador extremamente rápido e com suporte a aumento de resolução interna.
* **RetroArch Mobile:** Compatível com os núcleos MelonDS e DeSmuME.

### Console Real (Nintendo DS, DS Lite, DSi, 2DS, 3DS)
* **Flashcards (R4, Acekard, DSTWO, SuperCard):** Copie o arquivo `.nds` traduzido diretamente para a pasta de jogos no cartão MicroSD.
* **TWiLight Menu++ (Nintendo DSi / 3DS com CFW):** Coloque a ROM em `sd:/roms/nds/` e inicie normalmente pelo menu.

---

## 7. Solução de Problemas (Troubleshooting)

* **Erro "Source ROM mismatch" no Rom Patcher JS ou Flips:**
  * Sua ROM não corresponde à versão exata esperada pelo patch selecionado.
  * Verifique se sua ROM é a versão Europeia (`4E8C3E1B`) ou Americana (`A9F0B8F9`) usando o script `apply_patch.py` ou uma ferramenta de hash como 7-Zip ou HashTab. Certifique-se de escolher o arquivo `.bps` correto para a sua versão.
* **Tela Branca ou Preta ao Iniciar:**
  * Certifique-se de que aplicou o patch sobre uma cópia **limpa e original**, sem patches anteriores e sem aparagem (trimming).
  * No emulador MelonDS, certifique-se de que a opção de inicialização direta (*Direct Boot*) ou inicialização via Firmware está devidamente configurada.
* **Textos em inglês na ROM Europeia:**
  * O patch `DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps` substitui tanto as pastas `EN` quanto `US`. Caso seu console/emulador esteja em outro idioma europeu (francês, alemão, espanhol ou italiano), altere o idioma do sistema nas configurações do emulador/firmware para **Inglês** para que o jogo carregue os scripts traduzidos em português.

---

## 8. Créditos e Agradecimentos

* **Desenvolvedora Original:** Monolith Soft
* **Publicadora:** Namco Bandai Games / Bird Studio / Shueisha / Toei Animation
* **Tradução PT-BR:** ThiagoCM (using AI)
* **Base de Tradução Original:** gA & João13
* **Engenharia Reversa, Adaptação de Motor e Correção de Patches (EUR/USA):** Antigravity AI Assistant
* **Comunidade:** Romhacking Brasil e fãs da franquia Dragon Ball

*Aviso Legal: Este é um projeto sem fins lucrativos desenvolvido por fãs. Nenhuma ROM comercial protegida por direitos autorais é distribuída pelo projeto.*
