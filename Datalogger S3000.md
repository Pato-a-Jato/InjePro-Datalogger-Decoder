# Decodificação do Datalogger S3000 — Engenharia Reversa

## Descrição

Este documento apresenta o processo de **engenharia reversa do formato binário `.ds3`**, utilizado pelo datalogger da **Injepro S3000**, com o objetivo de compreender sua estrutura interna e possibilitar a extração dos dados em formato aberto (ex.: `.csv`).

O arquivo inicia com um **cabeçalho (header)**, responsável por armazenar informações como a versão, possui 41 bytes conforme o exemplo abaixo:

```
41 52 51 01 00 29 00 3b 00 30 aa 06
00 00 00 02 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 05 31 2e 32 2e
30 01 00 00 00
```

Após o cabeçalho, o arquivo é composto por uma sequência de **blocos de dados** (frames), cada um iniciado pela assinatura fixa `AA 55 AA`.  
Essa sequência se repete **13.970 vezes** neste exemplo, indicando que cada ocorrência marca o **início de uma nova amostra de sensores** registrada pelo datalogger.

O método de análise empregado baseia-se nos seguintes passos:

1. **Conversão** do arquivo `.ds3` para formato hexadecimal legível (`xxd -p`);
2. **Edição controlada** de pequenos blocos de bytes para observar alterações nos valores exibidos pelo software oficial;
3. **Comparação dos resultados** para identificar a correspondência entre bytes e parâmetros físicos (rotação, tensão, MAP, etc.).


## Conversões úteis

```bash
# Converter arquivo binário para hexadecimal (texto)
xxd -p "Datalogger s3000 EUA.ds3" > "Datalogger s3000 EUA.hex"

# Converter hexadecimal de volta para binário
xxd -r -p "teste_ds3.txt" "output1.ds3"
```

## Exemplo de bloco analisado

```
aa 55 aa                             
87 0e 84 00 00 00 dd 01 43 00 1d 00  
00 00 00 00 00 00 00 00 1d 00 43 00  
00 00 00 00 00 00 00 00 00 00 00 00  
00 00 00 00 00 00 00 00 00 00 00 00  
00 00 b7 00 00 00 00 00              
```

### Tabela completa de decodificação com bytes acumulados

| Nº | Campo / Descrição       | Bytes | Bytes Sum | Valor Hex         | Little Endian | Valor Decimal  | Fórmula / Escala       | Observações                        |
| -- | ----------------------- | ----- | ----------| ----------------- | ------------- | -------------- | -----------------------| -----------------------------------|
| 1  | **Início do bloco**     | 3     | 3         | AA 55 AA          | -             | -              | -                      | Delimitador de frame               |
| 2  | **Rotação (RPM)**       | 2     | 5         | 87 0E             | 0E87          | 3719           | valor_dec              | -                                  |
| 3  | **Bateria (V)**         | 2     | 7         | 84 00             | 0084          | 13,2           | valor_dec / 10         | -                                  |
| 4  | **MAP (bar)**           | 2     | 9         | 00 00             | 0000          | 0,00           | valor_dec / 100        | -                                  |
| 5  | **Não Identificado #0** | 6     | 15        | DD 01 43 00 1D 00 | -             | -              | -                      | Não identificado                   |
| 6  | **P. Comb (bar)**       | 2     | 17        | 00 00             | 0000          | 0,00           | valor_dec / 100        | -                                  |
| 7  | **Não Identificado #1** | 4     | 21        | 00 00 00 00       | -             | -              | -                      | Não identificado                   |
| 8  | **TPS (%)**             | 2     | 23        | 00 00             | 0000          | 0              | valor_dec / 10         | -                                  |
| 9  | **Temp. Ar (°C)**       | 2     | 25        | 1D 00             | 001D          | 29             | valor_dec              | -                                  |
| 10 | **Temp. Motor (°C)**    | 2     | 27        | 43 00             | 0043          | 67             | valor_dec              | -                                  |
| 11 | **Sonda NB (V)**        | 2     | 29        | 00 00             | 0000          | 0,00           | valor_dec / 100        | -                                  |
| 12 | **Sonda WB (V)**        | 1     | 30        | 00                | 00            | 0,00           | valor_dec / 100        | -                                  |
| 13 | **Não Identificado #2** | 1     | 31        | 00                | 00            | -              | -                      | Não identificado                   |
| 14 | **Corr. Sonda (%)**     | 2     | 33        | 00 00             | 0000          | 0              | valor_dec              | -                                  |
| 15 | **Não Identificado #3** | 2     | 35        | 00 00             | 0000          | -              | -                      | Não identificado                   |
| 16 | **Ponto Ignição (°)**   | 2     | 37        | 00 00             | 0000          | 0              | valor_dec / 10         | -                                  |
| 17 | **Inj. B1 (%)**         | 2     | 39        | 00 00             | 0000          | 0              | valor_dec              | -                                  |
| 18 | **Inj. B2 (%)**         | 2     | 41        | 00 00             | 0000          | 0              | valor_dec              | -                                  |
| 19 | **Inj. B3 (%)**         | 2     | 43        | 00 00             | 0000          | 0              | valor_dec              | -                                  |
| 20 | **Inj. B1 (ms)**        | 2     | 45        | 00 00             | 0000          | 0              | valor_dec / 100        | -                                  |
| 21 | **Inj. B2 (ms)**        | 2     | 47        | 00 00             | 0000          | 0              | valor_dec / 100        | -                                  |
| 22 | **Inj. B3 (ms)**        | 2     | 49        | 00 00             | 0000          | 0              | valor_dec / 100        | -                                  |
| 23 | **Booster / Arrancada** | 1     | 50        | 00                | 00            | nda            | -                      | 00=nda, 01=a, 10=b, 11=ba          |
| 24 | **Não Identificado #4** | 3     | 53        | 00 00 00          | -             | -              | -                      | Não identificado                   |
| 25 | **Ângulo de Fase (°)**  | 2     | 55        | B7 00             | 183           | valor_dec      | -                      |                                    |
| 26 | **Não Identificado #5** | 2     | 57        | 00 00             | -             | -              | -                      | Não identificado                   |
| 27 | **Roda Tração (km/h)**  | 2     | 59        | 00 00             | 0,0           | valor_dec / 10 | Ignorar casas decimais |                                    |
| 28 | **Fim do bloco**        | -     | 59        | -                 | -             | -              | -                      | Próximo bloco inicia com `AA 55 AA`|

## Observações

- **Endianess:** Todos os campos numéricos utilizam **Little Endian (LSB → MSB)**.
- **Campos *Não Identificado*:** bytes que, quando modificados, **não alteram os valores exibidos** no software foram marcados como `SOBRANDO` ou `PLACEHOLDER`.
- **Fórmulas de escala:** derivadas experimentalmente, comparando a leitura exibida no software com o valor em bytes alterado manualmente.

## Como usar o script de decoder
O script `ds3_to_csv.py` permite extrair todos os frames de um arquivo `.ds3` e gerar um CSV com todos os campos decodificados, incluindo os valores *raw* (hexadecimais) de cada dado.

### Uso
```bash
python3 ds3_to_csv.py <arquivo_entrada.ds3> <arquivo_saida.csv>
```

**Exemplo:**

```bash
python3 ds3_to_csv.py "Datalogger s3000 EUA.ds3" "dados_decodificados.csv"
```

- `<arquivo_entrada.ds3>`: caminho para o arquivo `.ds3` que será lido.
- `<arquivo_saida.csv>`: caminho do arquivo CSV que será gerado com os dados decodificados.

### Resultado esperado
- Um arquivo CSV contendo:
  - `frame_index`: índice do frame no arquivo.
  - `file_offset`: posição inicial do frame no arquivo `.ds3`.
  - `hex_frame`: bytes completos do frame em hexadecimal.
  - Cada campo decodificado (rotacao, bateria, MAP, TPS, temperatura, injeções, etc.).
  - Colunas `_raw` correspondentes aos bytes originais de cada campo.

### Observações
- O script **ignora bytes do cabeçalho** antes do primeiro frame (`AA 55 AA`).
- Apenas frames completos (59 bytes) são processados.

