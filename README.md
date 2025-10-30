    # Decodificando o datalogger da S3000

    bin para hex: xxd -p "Datalogger s3000 EUA.ds3" > "Datalogger s3000 EUA.hex"
    hex para bin: xxd -r -p teste_ds3.txt output1.ds3

    AA 55 AA se repete 13970 vezes -> Provavelmente delimita bloco de dados

    https://www.rapidtables.com/convert/number/decimal-to-hex.html?x=30

    minha analise para a engenharia reversa esta sendo modificar um arquivo reduzido (header e 2 blocos de dados) e checar no programa como o valor altera

    header é
    41 52 51 01 00 29 00 3b 00 30 aa 06 00 00 00 02 
    00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 05 
    31 2e 32 2e 30 01 00 00 00 

    linha de exemplo:

    aa 55 aa 
    87 0e 84 00 00 00 dd 01 43 00 1d 00 
    00 00 00 00 00 00 00 00 1d 00 43 00 
    00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 00 00 00 00 00 00 00 00 00 00 
    00 00 b7 00 00 00 00 00

    aa 55 aa
    87 0e

    
    aa 55 aa -> inicio do bloco
    87 0e -> dec de 0e 87 ->  rotação -> 3719
    84 00 -> dec de 00 84 -> Bateria -> 13,2 (valor_dec/10)
    00 00 -> MAP -> 0,00 (valor_dec/100)
    dd 01 43 00 1d 00 -> não sei
    00 00 -> P. Comb (valor_dec/100)
    00 00 00 00 -> não sei
    00 00 -> TPS (valor_dec/10)
    1d 00 -> Temp Ar
    43 00 -> Temp Motor
    00 00 -> Sonda NB (valor_dec/100)
    00 -> Sonda WB (valor_dec/100)
    00 -> Alterar não mudou nada -> SOBRANDO -> pode ser placeholder o byte identificador ou eu vi errado
    00 00 -> Corr Sonda % (valor_dec)
    00 00 -> Alterar não mudou nada -> SOBRANDO -> pode ser placeholder o byte identificador ou eu vi errado
    00 00 -> Ponto ign (valor_dec/10) 
    00 00 -> Inj Banca 1 % (valor_dec) 
    00 00 -> Inj Banca 2 % (valor_dec) 
    00 00 -> Inj Banca 3 % (valor_dec) 
    00 00 -> Inj Banca 1 ms (valor_dec/100) 
    00 00 -> Inj Banca 2 ms (valor_dec/100) 
    00 00 -> Inj Banca 3 ms (valor_dec/100) 
    00 -> booster e arrancada (10:b, 01:a, 11:ba, 00:nda)
    00 00 00 -> Alterar não mudou nada -> SOBRANDO -> pode ser placeholder ou byte identificador ou eu vi errado
    b7 00 -> Angulo de fase
    00 00 -> Alterar não mudou nada -> SOBRANDO -> pode ser placeholder ou byte identificador ou eu vi errado
    00 00 -> Roda Tração (valor_dec/10 e ignora o que tiver depois da virgula)


    # Decodificando o datalogger da T4000

    xxd -p "Datalogger volta invalidada.dt4" > "Datalogger volta invalidada.hex"