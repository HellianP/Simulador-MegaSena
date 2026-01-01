# 🎰 Simulador de Mega-Sena

Um simulador completo e interativo da Mega-Sena desenvolvido em Python com interface gráfica. Teste suas chances, simule milhares de sorteios e descubra quanto você precisaria gastar para ganhar!

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Funcionalidades

### 🎯 Sorteio Manual
- **Três formas de selecionar números:**
  - ✍️ Digitação manual (ex: 1,5,12,23,34,45)
  - 🎯 Seletor visual com grid interativo
  - 🎲 Gerador de jogos aleatórios
- **Múltiplos jogos:** Adicione quantos jogos quiser (6 a 20 dezenas)
- **Sorteio em tempo real:** Números sorteados a cada 5 segundos
- **Estatísticas ao vivo:** Acompanhe seus acertos durante o sorteio
- **Cálculo automático:** Preços reais e probabilidades de cada jogo

### 🚀 Simulação Automática
- **Múltiplos jogos simultâneos:** Teste várias combinações ao mesmo tempo
- **Sorteios ilimitados ou definidos:** Configure a quantidade desejada
- **Condições de parada personalizáveis:**
  - ☐ Parar ao acertar QUADRA (4 números)
  - ☐ Parar ao acertar QUINA (5 números)
  - ☑ Parar ao acertar SENA (6 números)
- **Histórico completo:** Veja todos os sorteios realizados
- **Análise de custos:** Descubra quanto gastaria para ganhar
- **Velocidade:** Milhares de sorteios por minuto

## 📊 Análises e Estatísticas

- **Probabilidades precisas:** Cálculo matemático exato das chances
- **Custo por sorteio:** Soma dos preços de todos os seus jogos
- **Gasto total:** Quanto você investiria na simulação
- **Custo médio para ganhar:** Investimento necessário até acertar
- **Contadores de prêmios:** Quadras, Quinas e Senas obtidos
- **Melhor resultado:** Maior número de acertos alcançado

## 🛠️ Requisitos

- Python 3.7 ou superior
- tkinter (geralmente incluído no Python)
- Bibliotecas padrão: `random`, `time`, `threading`, `itertools`

## 📥 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/HellianP/Simulador-MegaSena.git
cd simulador-megasena
```

2. Execute o programa:
```bash
python megasena_simulator.py
```

> **Nota:** O tkinter já vem instalado com Python na maioria das distribuições. Se necessário, instale com:
> - **Ubuntu/Debian:** `sudo apt-get install python3-tk`
> - **Fedora:** `sudo dnf install python3-tkinter`
> - **macOS/Windows:** Geralmente já incluído

## 🎮 Como Usar

### Sorteio Manual

1. **Adicionar jogos:**
   - Digite as dezenas separadas por vírgula, OU
   - Clique em "Seletor Visual" para escolher visualmente, OU
   - Clique em "Jogo Aleatório" para gerar automaticamente

2. **Iniciar sorteio:**
   - Clique em "Iniciar Sorteio"
   - Acompanhe os números sendo sorteados a cada 5 segundos
   - Veja seus acertos em tempo real

3. **Resultado:**
   - Ao final, visualize se ganhou algum prêmio
   - Quadra (4 acertos), Quina (5) ou Sena (6)

### Simulação Automática

1. **Configurar jogos:**
   - Adicione um ou mais jogos usando qualquer método
   - Veja o custo total por sorteio

2. **Configurar simulação:**
   - Digite a quantidade de sorteios (0 = ilimitado)
   - Marque as condições de parada desejadas

3. **Executar:**
   - Clique em "Iniciar Simulação"
   - Acompanhe as estatísticas em tempo real
   - Veja o histórico de sorteios

4. **Resultado:**
   - Ao finalizar, veja quanto gastou
   - Descubra o custo médio para ganhar cada prêmio
   - Analise a quantidade de prêmios obtidos

## 💰 Tabela de Preços (2024)

| Dezenas | Preço (R$) | Probabilidade |
|---------|-----------|---------------|
| 6       | 6,00      | 1 em 50.063.860 |
| 7       | 42,00     | 1 em 7.151.980 |
| 8       | 168,00    | 1 em 1.787.995 |
| 9       | 504,00    | 1 em 595.998 |
| 10      | 1260,00  | 1 em 238.399 |
| 15      | 30030,00 | 1 em 3.174 |
| 20      | 232,560.00| 1 em 543 |


## 🧮 Exemplos de Uso

### Exemplo 1: Testar um jogo simples
```python
# Adicione 6 dezenas: 1, 5, 12, 23, 34, 45
# Custo: R$ 6,00
# Probabilidade: 0.000002% (1 em 50 milhões)
```

### Exemplo 2: Simular até ganhar a Sena
```python
# Adicione um jogo com 10 dezenas
# Configure: 0 sorteios (ilimitado)
# Marque: ☑ Parar em SENA
# Execute e descubra quantos sorteios foram necessários!
```

### Exemplo 3: Estratégia com múltiplos jogos
```python
# Adicione 3 jogos diferentes (6, 7 e 8 dezenas)
# Custo por sorteio: R$ 6,00 + R$ 42,00 + R$168,00 
# Simule 1000 sorteios
# Compare os resultados de cada jogo
```

## 🔬 Curiosidades Matemáticas

- **Probabilidade de ganhar na Sena com 6 dezenas:** 1 em 50.063.860 (~0,000002%)
- **Para ter 50% de chance de ganhar:** Seria necessário jogar ~34.657.359 vezes
- **Custo para 50% de chance (6 dezenas):** Maior do que R$ 173.286.795,00
- **Estatisticamente:** Você tem mais chance de ser atingido por um raio! ⚡

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um Fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abrir um Pull Request

## 📋 Ideias para Futuras Melhorias

- [ ] Exportar resultados para CSV/Excel
- [ ] Gráficos de estatísticas (matplotlib)
- [ ] Análise de números mais sorteados
- [ ] Histórico de jogos anteriores da Mega-Sena real
- [ ] Modo "estratégia inteligente" baseado em padrões
- [ ] Comparação de diferentes estratégias
- [ ] Suporte para outras loterias (Quina, Lotofácil, etc)
- [ ] Tema claro/escuro

## ⚠️ Aviso Importante

Este é um **simulador educacional** para fins de entretenimento e aprendizado sobre probabilidades. 

**Lembre-se:**
- Jogos de azar podem causar dependência
- As chances reais de ganhar são extremamente baixas
- Jogue com responsabilidade e consciência
- Este software não garante ou incentiva ganhos reais

## 📄 Licença

Este projeto está sob a licença MIT. 

## 👤 ~ Hellian

Desenvolvido com para fins educacionais


- Inspirado pela curiosidade sobre probabilidades

---

