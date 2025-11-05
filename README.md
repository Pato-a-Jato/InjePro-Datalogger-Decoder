# injepro-datalogger-decoder
**Descrição**

Este repositório contém um *decoder* (decodificador) para os arquivos de datalogger utilizados nas injeções eletrônicas **Injepro S3000** e **Injepro T4000**. O objetivo é permitir a leitura e a extração dos dados contidos nos arquivos binários (`.ds3`, `.dt4`) e convertê-los para um formato aberto e analisável (CSV). Além do script principal de conversão, o repositório traz documentação e exemplos para facilitar a engenharia reversa e a manutenção.

## Estrutura do repositório
```text
README.md
Datalogger S3000.md
Datalogger T4000.md
scripts/
  └─ ds3_to_csv.py
  └─ dt4_to_csv.py
examples/
  └─ Datalogger s3000 EUA.ds3
  └─ Datalogger volta invalidada.dt4
```

## Arquivos importantes
- `scripts/ds3_to_csv.py` — script para decodificar arquivos `.ds3` do S3000.
- `scripts/dt4_to_csv.py` — script para decodificar arquivos `.dt4` do T4000.
- `examples/` — exemplos de arquivos binários para testes.

## Compatibilidade

Os scripts foram desenvolvidos para rodar em **Python 3.8+** e projetados para funcionar tanto em **Windows** quanto em **Linux** (testados em ambos ambientes). As dependências usadas são nativas de **Python 3.8+**.

## Como o binário do datalogger funciona (visão geral)

- O arquivo binário contém blocos ou *frames* com início reconhecível por uma assinatura/sequência fixa (por exemplo `AA 55 AA` ou `AA 55 81`).
- Cada bloco representa um conjunto de leituras e campos (por exemplo: rotações, temperatura, voltagem, sensores, status da bateria ou marcação temporal).
- Os campos dentro do bloco têm tamanho fixo (ex.: `uint8`, `uint16`, `int32`) e a codificação é, na maioria dos casos, **little-endian**. Algumas leituras exigem aplicação de escala ou offset para chegar ao valor físico.

## Como usar
1. Clone o repositório:

```bash
git clone https://github.com/Pato-a-Jato/InjePro-Datalogger-Decoder.git
cd injepro-datalogger-decoder
```

2. Rodando o decoder S3000 (exemplo):

```bash
python3 scripts/ds3_to_csv.py "examples/Datalogger s3000 EUA.ds3" output_s3000.csv
```

3. Rodando o decoder T4000 (exemplo):

```bash
python3 scripts/dt4_to_csv.py "examples/Datalogger volta invalidada.dt4" output_t4000.csv
```