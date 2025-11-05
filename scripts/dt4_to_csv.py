#!/usr/bin/env python3
"""
dt4_to_csv.py

Uso:
    python3 dt4_to_csv.py input.dt4 output.csv

Lê um arquivo .dt4, ignora o header de 606 bytes,
encontra blocos iniciados por AA 55 81, decodifica campos
conforme a tabela grava resultado em CSV.
"""

import sys
import csv
from pathlib import Path
from typing import List, Tuple

SIGNATURE = bytes([0xAA, 0x55, 0x81])
HEADER_SIZE = 606

def read_uint16_le(buf: bytes, off: int):
    return int.from_bytes(buf[off:off + 2], byteorder='little', signed=False)

def parse_block(block: bytes):
    o = {}
    o['hex_block'] = block.hex(' ')

    def add(name, off, scale=None):
        raw = block[off:off+2]
        val = read_uint16_le(block, off)
        o[f'{name}_hex'] = raw.hex(' ')
        o[f'{name}_dec'] = val
        if scale is None:
            o[f'{name}_fmt'] = val
        else:
            o[f'{name}_fmt'] = val * scale
        return off + 2

    off = 3  # pula assinatura (3 bytes)

    off = add('rotacao', off, 1)
    off = add('bateria_v', off, 1/100)
    off = add('map_bar', off, 1/100)

    campos_seq = [
        ('nao_identifico_0', None),
        ('tps_1', 1/10),
        ('temp_ar', 1),
        ('temp_motor', 1),
        ('sonda_nb_v', 1/100),
        ('nao_identifico_1', None),
        ('ign_cil_1', 1/100),
        ('ign_cil_2', 1/100),
        ('ign_cil_3', 1/100),
        ('ign_cil_4', 1/100),
        ('inj_a_cil1_pct_l1', 1/10),
        ('inj_a_cil1_ms_l1', 1/100),
        ('inj_a_cil1_pct_l2', 1/10),
        ('inj_a_cil1_ms_l2', 1/100),
        ('inj_a_cil1_pct_l3', 1/10),
        ('inj_a_cil1_ms_l3', 1/100),
        ('inj_a_cil1_pct_l4', 1/10),
        ('inj_a_cil1_ms_l4', 1/100),
        ('inj_b1_pct', 1/10),
        ('inj_b1_ms', 1/1000),
        ('inj_b2_pct', 1/10),
        ('inj_b2_ms', 1/1000),
        ('nao_identifico_2', None),
        ('ang_injecao', 1),
        ('pressao_alvo_1', 1/100),
        ('fase_1', 1),
        ('nao_identifico_3', None),
        ('nao_identifico_4', None),
        ('nao_identifico_5', None),
        ('corr_sonda_1', 1/100),
        ('corr_sonda_2', 1/100),
        ('corr_sonda_3', 1/100),
        ('corr_sonda_4', 1/100),
        ('nao_identifico_6', None),
        ('nao_identifico_7', None),
        ('nao_identifico_8', None),
        ('p_comb_bar', 1/100),
        ('p_oleo_bar', 1/100),
        ('tensao_ext_01', 1/100),
        ('tensao_ext_02', 1/100),
        ('tensao_ext_03', 1/100),
        ('tensao_ext_04', 1/100),
        ('tensao_ext_05', 1/100),
        ('tensao_ext_06', 1/100),
        ('tensao_ext_07', 1/100),
        ('litros_tanque', 1/10),
        ('booster_pwm', 1),
        ('booster_alvo', 1/100),
        ('nao_identifico_9', None),
        ('nao_identifico_10', None),
        ('nao_identifico_11', None),
        ('nao_identifico_12', None),
    ]

    for name, scale in campos_seq:
        try:
            off = add(name, off, scale)
        except IndexError:
            break

    return o

def find_blocks(data: bytes) -> List[Tuple[int, bytes]]:
    blocks = []
    idx = HEADER_SIZE
    while True:
        pos = data.find(SIGNATURE, idx)
        if pos == -1:
            break
        next_pos = data.find(SIGNATURE, pos + 3)
        end = next_pos if next_pos != -1 else len(data)
        block = data[pos:end]
        blocks.append((pos, block))
        idx = end
    return blocks

def blocks_to_csv(blocks: List[Tuple[int, bytes]], csv_path: Path):
    fieldnames = ['block_index', 'file_offset']
    sample_parsed = parse_block(blocks[0][1])
    fieldnames.extend(sample_parsed.keys())

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, (off, blk) in enumerate(blocks):
            parsed = parse_block(blk)
            row = {'block_index': i, 'file_offset': off}
            row.update(parsed)
            writer.writerow(row)

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 dt4_to_csv.py input.dt4 output.csv")
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_csv = Path(sys.argv[2])

    if not in_path.exists():
        print(f"Arquivo não encontrado: {in_path}")
        sys.exit(1)

    data = in_path.read_bytes()

    blocks = find_blocks(data)
    if not blocks:
        print("Nenhum bloco encontrado (assinatura AA 55 81).")
        sys.exit(1)

    print(f"Header ignorado: {HEADER_SIZE} bytes")
    print(f"Blocos encontrados: {len(blocks)}")

    blocks_to_csv(blocks, out_csv)
    print(f"CSV gerado com sucesso: {out_csv}")

if __name__ == '__main__':
    main()
