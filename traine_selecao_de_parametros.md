# Seleção de Parâmetros para a Injeção Eletrônica: Traine Pato a Jato

## Introdução
Como *Traine*, foi proposto que eu desenvolvesse uma metodologia para seleção dos parâmetros da injeção eletrônica do Potiguara, visando alcançar maior eficiência energética.

Independentemente do método escolhido para a seleção dos parâmetros, a primeira etapa fundamental é definir como a eficiência energética será medida.

## Definição da Métrica de Eficiência Energética
A medida de eficiência selecionada foi o $BSFC$ (Brake-Specific Fuel Consumption), que representa a eficiência de consumo de combustível de uma máquina motriz que queima combustível e produz potência rotacional (ou de eixo).

O $BSFC$ é amplamente utilizado para comparar a eficiência de motores de combustão interna com saída de potência mecânica.

$$
\text{BSFC} = \frac{r}{P}
$$

Onde:

- $r$: taxa de consumo de combustível em gramas por segundo (g/s)
- $P$: potência produzida em watts (W), dada por:

$$
P = \tau \cdot \omega
$$

Em que:
-  $\tau$ : torque do motor (N·m)
- $\omega$: velocidade angular do motor (rad/s)



## Aquisição das Variáveis Físicas

A taxa de consumo de combustível $r$ será obtida por meio de um fluxômetro volumétrico, que mede o volume de combustível consumido em um intervalo de tempo.
Multiplicando o volume pela densidade do combustível e dividindo pelo tempo, obtém-se $r$ em g/s.

Como exemplo, podem ser utilizados fluxômetros da linha Microstream Flowsensor OF-Z, que apresentam baixo custo e simplicidade de uso, com saídas em forma de pulsos digitais, cada pulso correspondendo a um volume conhecido de combustível.

**Referências:**

- [AliExpress](https://pt.aliexpress.com/item/32757170131.html)
- [eBay](https://www.ebay.com/itm/276816027767)

A **potência mecânica** $P$ será determinada a partir das medições de torque e rotação (RPM) obtidas pelo dinamômetro, integradas aos dados de injeção eletrônica coletados via *datalogger*.



## Ferramenta de Processamento de Dados
Para simplificar o processo de coleta e exportação de dados do *datalogger*, foram desenvolvidos scripts em Python, disponíveis no repositório:

[https://github.com/Pato-a-Jato/InjePro-Datalogger-Decoder](https://github.com/Pato-a-Jato/InjePro-Datalogger-Decoder)

Esses scripts recebem arquivos `.dt4` ou `.ds3` e geram como saída um arquivo `.csv` contendo as variáveis coletadas, pronto para análise.



## Metodologia Proposta
A metodologia definida se baseia em quatro etapas principais:

1. **Aquisição de dados** para geração de uma simulação;
2. **Simulação do sistema** com base nos dados obtidos;
3. **Seleção dos parâmetros ótimos** com base nos resultados da simulação;
4. **Aplicação e validação** dos parâmetros selecionados em testes reais.

## Etapa 1: Aquisição de Dados
Será necessário dispor de $N$ mapas de injeção já configurados pela equipe e de um dinamômetro capaz de controlar a carga aplicada ao motor.

Para cada mapa de injeção, será realizada uma bateria de testes abrangendo as seguintes variáveis:

- **TPS (Throttle Position Sensor):** 0% e 100%
- **RPM:** 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, ..., até $\text{RPM}_{\text{máx}}$
- **Carga no dinamômetro:** 0%, 10%, 20%, 30%, ..., 100%

### Pseudocódigo do processo de medição:
```text
for m in MAPAS_DE_INJECAO:
    for t in TPS:
        for r in RPM:
            for c in CARGA_DINAMÔMETRO:
                aguardar_estabilização_do_motor()
                medir_BSFC(m, t, r, c)
```

Dessa forma, obtém-se o **$BSFC$** para todas as combinações possíveis de **mapa de injeção**, **TPS**, **RPM** e **carga aplicada**.

## Etapa 2: Modelagem do Comportamento do Motor
Com os dados adquiridos, são geradas matrizes de $BSFC$ correspondentes aos diferentes mapas de injeção.
A partir delas, aplicam-se métodos de regressão para modelar o comportamento do consumo em função das variáveis:

$$
\text{BSFC} = f(\text{mapa}, \text{TPS}, \text{RPM}, \text{carga})
$$

### Métodos de Regressão Possíveis
- **Regressão Linear Múltipla**
- **Regressão Polinomial**
- **Modelos Baseados em Árvores** (*Decision Trees*, *Random Forests*)
- **Redes Neurais Artificiais (ANNs)**: recomendadas para relações altamente não lineares

## Etapa 3: Otimização dos Parâmetros
Com o modelo obtido, o próximo passo é aplicar métodos de otimização para encontrar o conjunto de parâmetros que minimizam o $BSFC$, ou seja, maximizam a eficiência energética do motor.

### Métodos de Otimização Sugeridos
- **Busca em Grade (Grid Search)**: simples e eficiente para pequenos espaços de parâmetros
- **Gradiente Descendente (Gradient Descent)**: útil para superfícies contínuas e suaves
- **Algoritmos Genéticos (Genetic Algorithms)**: aplicáveis a otimizações complexas e não lineares
- **Simulated Annealing**: adequado para problemas com múltiplos mínimos locais
- **Otimização Bayesiana**: eficiente em casos de alto custo computacional

## Etapa 4: Validação Experimental
Após identificar os parâmetros que minimizam o $BSFC$ nas simulações, realiza-se a validação experimental em condições reais.
Esses testes iram permitir comparar os resultados simulados com os valores obtidos no dinamômetro, checando assim a consistência e eficácia da metodologia proposta.


## Conclusão
Espera-se que a aplicação da metodologia proposta permita a seleção sistemática dos parâmetros ótimos da injeção eletrônica, fundamentada em medições experimentais, modelagem matemática e técnicas de otimização. Dessa forma, objetiva-se não apenas elevar a eficiência energética, mas também disponibilizar uma ferramenta analítica consistente para futuras calibrações do sistema de injeção.
