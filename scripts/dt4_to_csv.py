#!/usr/bin/env python3
"""
dt4_to_csv.py

Uso:
    python3 dt4_to_csv.py input.dt4 output.csv

Lê um arquivo .dt4, encontra frames iniciados por AA 55 AA (3 bytes),
decodifica os campos conforme a tabela encontrada em 'Datalogger T4000.md' 
e grava resultado em um CSV, incluindo o valor raw (hex) de cada campo.
"""
