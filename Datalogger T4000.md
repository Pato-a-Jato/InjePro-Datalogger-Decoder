Hipoteses de separador de linha:
- aa 55 81

aprendi minha lição com o s3000, converter de bin para hex mas deixar todos os bytes em uma unica linha tem um espaço a cada byte

xxd -p "examples/Datalogger volta invalidada.dt4" | tr -d '\n' | sed 's/../& /g' > "Datalogger_volta_invalidada.hex"

isso facilita a quebra de linha usando o spearador de linha

usar o `aa 55 81` faz sentido pois entre dois `aa 55 81` sempre esta tendo 126 bytes

se `aa 55 81`, tudo antes do primeiro  `aa 55 81` vai ser o header do arquivo, isso da 606 bytes

para formatar o hex em blocos com 16 bytes por linha: python3 format_aa5581_block.py Datalogger_volta_invalidada.hex Datalogger_volta_invalidada_formatada.hex


aa 55 81 
00 00 85 00 09 00 00 00 00 00 00 00 00 00 00 00 
e8 03 16 00 30 00 00 00 1c a0 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 78 01 00 10 02 02 00 00 00 38 00 03 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 28 00 00 00 
f2 01 dc 01 44 00 07 01 d3 01 df 01 6b 01 00 00 
00 00 00 00 00 00 00 00 20 00 00 00 3d 00 


padrão quebrou aqui:

aa 55 81
00 00 86 00 08 00 00 00 00 00 00 00 00 00 00 00
e4 03 17 00 30 00 00 00 1c a0 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 7c 01 00 10 02 02 00 00 00 38 00 03 00 00
00 00 00 00 00 00 00 00 00 00 00 00 28 00 00 00
f1 01 db 01 44 00 05 01 d2 01 de 01 69 01 00 00
00 00 00 00 00 00 00 00 20 00 00 00 59 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

Por que isso em cima aconteceu??? Isso pode ocorrer no ds3? Não encontrei isso lá

aa 55 81 
00 00 85 00 09 00 00 00 00 00 00 00 00 00 00 00 
e8 03 16 00 30 00 00 00 1c a0 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
00 00 78 01 00 10 02 02 60 00 00 38 00 03 00 00 
00 00 00 00 00 00 00 00 00 00 00 00 28 00 00 00 
f2 01 dc 01 44 00 07 01 d3 01 df 01 6b 01 00 00 
00 00 00 00 00 00 00 00 20 00 00 00 3d 00 