# Datalogger T4000 — Formato de Arquivo DT4

## Estrutura Geral

O arquivo `.dt4` é composto por um **cabeçalho fixo de 606 bytes**, seguido por uma sequência de **blocos de dados**, cada um com **126 bytes**.  
Cada bloco de dados começa com a assinatura:

```
AA 55 81
```

Tudo antes do primeiro `AA 55 81` corresponde ao cabeçalho. Os blocos seguintes contêm os dados amostrados e codificados pelo datalogger.


## Estrutura do Arquivo

| Seção        | Tamanho (bytes) | Descrição |
|---------------|----------------|------------|
| Header        | 606             | Contém informações fixas e de configuração |
| Bloco de Dados | 126 × N        | Cada bloco é delimitado por `AA 55 81` |


## Estrutura de Cada Bloco (126 bytes)

| Nº | Campo / Descrição             | Bytes | Bytes Sum | Valor Hex  | Little Endian | Valor Decimal | Escala / Fórmula | Unidade |
| -- | ----------------------------- | ----- | --------- | ---------- | ------------- | ------------- | ---------------- | ------- |
| 1  | Indicador de início do bloco  | 3     | 3         | `aa 55 81` | —             | —             | —                | —       |
| 2  | Rotação                       | 2     | 5         | `7b 0e`    | `0e7b`        | 3707          | direto           | RPM     |
| 3  | Bateria                       | 2     | 7         | `84 00`    | `0084`        | 132           | ÷100             | V       |
| 4  | MAP                           | 2     | 9         | `09 00`    | `0009`        | 9             | ÷100             | bar     |
| 5  | (não identificado)            | 2     | 11        | `00 01`    | `0100`        | —             | —                | —       |
| 6  | (não identificado)            | 2     | 13        | `00 02`    | `0200`        | —             | —                | —       |
| 7  | (não identificado)            | 2     | 15        | `00 03`    | `0300`        | —             | —                | —       |
| 8  | (não identificado)            | 2     | 17        | `00 04`    | `0400`        | —             | —                | —       |
| 9  | (não identificado)            | 2     | 19        | `00 05`    | `0500`        | —             | —                | —       |
| 10 | TPS 1                         | 2     | 21        | `e8 03`    | `03e8`        | 1000          | ÷10              | %       |
| 11 | Temp. Ar                      | 2     | 23        | `13 00`    | `0013`        | 19            | direto           | °C      |
| 12 | Temp. Motor                   | 2     | 25        | `30 00`    | `0030`        | 48            | direto           | °C      |
| 13 | Sonda NB                      | 2     | 27        | `00 06`    | `0600`        | 1536          | ÷100             | V       |
| 14 | (não identificado)            | 2     | 29        | `1c a0`    | `a01c`        | —             | —                | —       |
| 15 | Ignição Cil. 1                | 2     | 31        | `6f 01`    | `016f`        | 367           | ÷100             | °       |
| 16 | Ignição Cil. 2                | 2     | 33        | `6f 01`    | `016f`        | 367           | ÷100             | °       |
| 17 | Ignição Cil. 3                | 2     | 35        | `6f 01`    | `016f`        | 367           | ÷100             | °       |
| 18 | Ignição Cil. 4                | 2     | 37        | `6f 01`    | `016f`        | 367           | ÷100             | °       |
| 19 | Injetor A Cil. 1 (%) linha 1  | 2     | 39        | `65 00`    | `0065`        | 101           | ÷10              | %       |
| 20 | Injetor A Cil. 1 (ms) linha 1 | 2     | 41        | `d8 0c`    | `0cd8`        | 3288          | ÷100             | ms      |
| 21 | Injetor A Cil. 1 (%) linha 2  | 2     | 43        | `00 07`    | `0700`        | 1792          | ÷10              | %       |
| 22 | Injetor A Cil. 1 (ms) linha 2 | 2     | 45        | `00 08`    | `0800`        | 2048          | ÷100             | ms      |
| 23 | Injetor A Cil. 1 (%) linha 3  | 2     | 47        | `00 09`    | `0900`        | 2304          | ÷10              | %       |
| 24 | Injetor A Cil. 1 (ms) linha 3 | 2     | 49        | `00 0a`    | `0a00`        | 2560          | ÷100             | ms      |
| 25 | Injetor A Cil. 1 (%) linha 4  | 2     | 51        | `00 0b`    | `0b00`        | 2816          | ÷10              | %       |
| 26 | Injetor A Cil. 1 (ms) linha 4 | 2     | 53        | `00 0c`    | `0c00`        | 3072          | ÷100             | ms      |
| 27 | Injetor B-1 (%)               | 2     | 55        | `00 0e`    | `0e00`        | 3584          | ÷10              | %       |
| 28 | Injetor B-1 (ms)              | 2     | 57        | `00 0f`    | `0f00`        | 3840          | ÷1000            | ms      |
| 29 | Injetor B-2 (%)               | 2     | 59        | `00 10`    | `1000`        | 4096          | ÷10              | %       |
| 30 | Injetor B-2 (ms)              | 2     | 61        | `00 11`    | `1100`        | 4352          | ÷1000            | ms      |
| 31 | (não identificado)            | 2     | 63        | `00 12`    | `1200`        | —             | —                | —       |
| 32 | (não identificado)            | 2     | 65        | `00 13`    | `1300`        | —             | —                | —       |
| 33 | Ângulo de Injeção             | 2     | 67        | `00 14`    | `1400`        | 5120          | direto           | °       |
| 34 | Pressão Alvo 1                | 2     | 69        | `00 15`    | `1500`        | 5376          | ÷100             | bar     |
| 35 | Fase 1                        | 2     | 71        | `87 01`    | `0187`        | 391           | direto           | °       |
| 36 | (não identificado)            | 2     | 73        | `00 10`    | `1000`        | —             | —                | —       |
| 37 | (não identificado)            | 2     | 75        | `02 02`    | `0202`        | —             | —                | —       |
| 38 | (não identificado)            | 2     | 77        | `60 00`    | `0060`        | —             | —                | —       |
| 39 | (não identificado)            | 2     | 79        | `00 39`    | `3900`        | —             | —                | —       |
| 40 | (não identificado)            | 2     | 81        | `00 03`    | `0300`        | —             | —                | —       |
| 41 | Corr. Sonda 1                 | 2     | 83        | `00 16`    | `1600`        | 5632          | ÷100             | %       |
| 42 | Corr. Sonda 2                 | 2     | 85        | `00 17`    | `1700`        | 5888          | ÷100             | %       |
| 43 | Corr. Sonda 3                 | 2     | 87        | `00 18`    | `1800`        | 6144          | ÷100             | %       |
| 44 | Corr. Sonda 4                 | 2     | 89        | `00 19`    | `1900`        | 6400          | ÷100             | %       |
| 45 | (não identificado)            | 2     | 91        | `00 1a`    | `1a00`        | —             | —                | —       |
| 46 | (não identificado)            | 2     | 93        | `00 1b`    | `1b00`        | —             | —                | —       |
| 47 | (não identificado)            | 2     | 95        | `00 1c`    | `1c00`        | —             | —                | —       |
| 48 | P. Comb.                      | 2     | 97        | `23 00`    | `0023`        | 35            | ÷100             | bar     |
| 49 | P. Óleo                       | 2     | 99        | `00 1d`    | `1d00`        | 7424          | ÷100             | bar     |
| 50 | Tensão Ext. 01                | 2     | 101       | `f2 01`    | `01f2`        | 498           | ÷100             | V       |
| 51 | Tensão Ext. 02                | 2     | 103       | `83 01`    | `0183`        | 387           | ÷100             | V       |
| 52 | Tensão Ext. 03                | 2     | 105       | `42 00`    | `0042`        | 66            | ÷100             | V       |
| 53 | Tensão Ext. 04                | 2     | 107       | `06 01`    | `0106`        | 262           | ÷100             | V       |
| 54 | Tensão Ext. 05                | 2     | 109       | `d3 01`    | `01d3`        | 467           | ÷100             | V       |
| 55 | Tensão Ext. 06                | 2     | 111       | `de 01`    | `01de`        | 478           | ÷100             | V       |
| 56 | Tensão Ext. 07                | 2     | 113       | `75 01`    | `0175`        | 373           | ÷100             | V       |
| 57 | Litros Tanque                 | 2     | 115       | `00 1e`    | `1e00`        | 7680          | ÷10              | L       |
| 58 | Booster PWM                   | 2     | 117       | `00 1f`    | `1f00`        | 7936          | direto           | —       |
| 59 | Booster Alvo                  | 2     | 119       | `01 01`    | `0101`        | 257           | ÷100             | —       |
| 60 | (não identificado)            | 2     | 121       | `01 02`    | `0201`        | —             | —                | —       |
| 61 | (não identificado)            | 2     | 123       | `01 03`    | `0301`        | —             | —                | —       |
| 62 | (não identificado)            | 2     | 125       | `20 00`    | `0020`        | —             | —                | —       |
| 63 | (não identificado)            | 2     | 127       | `01 04`    | `0401`        | —             | —                | —       |
| 64 | (não identificado)            | 2     | 129       | `01 05`    | `0501`        | —             | —                | —       |
