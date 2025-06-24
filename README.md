# 🎮 Sistema de DM em Massa para Discord

![GitHub license](https://img.shields.io/github/license/CuspeDeAsura/discord-dm-bot) 
![Python Version](https://img.shields.io/badge/Python-3.10+-blue) 
![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-dark_blue) 
![Status](https://img.shields.io/badge/Status-Stable-brightgreen) 

> Um bot simples e eficiente para enviar mensagens diretas (DMs) em massa para membros de um servidor Discord. Útil para comunicação rápida com jogadores, anúncios ou notificações importantes.

---

## 📌 Sobre

Este projeto foi desenvolvido para facilitar o envio de mensagens privadas (**Direct Messages - DMs**) a todos os membros de um servidor Discord, especialmente útil em ambientes de jogos online, servidores de RPG ou qualquer comunidade onde seja necessário enviar informações importantes a todos os usuários rapidamente.

O bot permite:
- ✅ Enviar mensagens personalizadas para todos os membros do servidor
- 🔐 Verificação de cargos para uso seguro dos comandos
- 🧩 Interface modular para fácil manutenção e expansão
- 📜 Logs detalhados de todas as ações realizadas
- 🔁 Hot Reload automático para desenvolvimento ágil

---

## 🖥️ Tela do Bot em Ação (exemplo)

![Bot em ação - Envio de DM](https://github.com/matheusvalpassos/Discord-MassDM/blob/main/massdm_func.png)

Exemplo de como o bot aparece no Discord após executar o comando `!dmall`.

---

## 🛠️ Funcionalidades Principais

| Recurso | Descrição |
|--------|-----------|
| 📬 Envio de DM em Massa | O bot envia uma mensagem personalizada a todos os membros do servidor. |
| 🔐 Verificação por Cargos | Apenas cargos específicos (ex: `GM`, `Admin`) podem usar os comandos. |
| 📝 Logs Detalhados | Registra todas as ações em arquivo e no terminal para auditoria futura. |
| 🔄 Hot Reload Automático | Recarrega automaticamente os módulos ao detectar mudanças nos arquivos `.py`. |
| 📦 Estrutura Modular | Código organizado em pacotes (`commands`, `utils`, `messages`, etc.) |

---

## 📋 Comandos Disponíveis

| Comando | Descrição |
|--------|-----------|
| `!dmall <mensagem>` | Envia uma mensagem direta para todos os membros do servidor. |
| `!helpcmds` | Mostra uma lista de comandos disponíveis e como utilizá-los. |

---

## ⚙️ Requisitos

Para rodar este projeto localmente, você precisa de:

- [Python 3.10+](https://www.python.org/downloads/) 
- [Discord Bot Token](https://discord.com/developers/applications) 
- Intenção ativada: `message_content`

---

## 📦 Instalação

### Passo 1: Clone o repositório

```
git clone https://github.com/seu-usuario/seu-repo.git 
cd seu-repo
```

### Passo 2: Instale as dependências

```
pip install -r requirements.txt
```

### Passo 3: Configure o bot

```
DISCORD_TOKEN=seu_token_aqui
GM_ROLE_ID=123456789012345678
LOGS_CHANNEL_ID=876543210987654321
```

### Passo 4: Execute o bot

```
python main.py
```

## 📁 Estrutura do Projeto

```
GAME-DISCORD-BOT/
│
├── main.py                     # Ponto de entrada do bot
├── .env                        # Configurações sensíveis
├── requirements.txt            # Dependências do projeto
│
├── commands/
│   └── dm_commands.py        # Comandos relacionados ao envio de DM
│
├── messages/
│   ├── embeds.py             # Embeds reutilizáveis
│   └── ui.py                 # Interface visual com botões
│
├── utils/
│   ├── roles.py              # Verificação de cargos
│   └── logger.py             # Funções de log
│
└── database/
    └── connection.py         # Conexão com bancos (opcional)
```

## 🧪 Próximos Recursos Planejados

- Enviar DM apenas para membros online
- Agendar mensagens automáticas
- Interface web para controle via navegador
- Backup de mensagens enviadas

## 🤝 Contribuições
Contribuições são sempre bem-vindas! Se você tiver melhorias de código, correções ou novas funcionalidades, abra uma **Pull Request** ou crie uma Issue !

## 📝 Licença
MIT License – veja o arquivo LICENSE para mais detalhes.

## 💬 Contato
Se quiser falar comigo ou sugerir melhorias:

GitHub: @matheusvalpassos
Discord: matheusvalpassos

## 🎯 Exemplo de Uso

```
!dmall Olá, evento especial começa em 10 minutos!
✅ Mensagem enviada para 250 membros.
```

## ⚠️ Aviso de Responsabilidade

Este projeto foi desenvolvido com fins educativos e de automação útil para comunidades online. Não me responsabilizo pelo uso indevido ou por ações realizadas com este bot fora do escopo permitido pelas [Diretrizes da API do Discord](https://discord.com/developers/docs/policies-security). 

Ao usar ou compartilhar este projeto, você concorda:
- Em não utilizá-lo para fins maliciosos
- Em respeitar as políticas do Discord
- Em assumir total responsabilidade por suas ações

Use com ética e moderação.


