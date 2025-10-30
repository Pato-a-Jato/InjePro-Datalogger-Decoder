#!/usr/bin/env python3
"""
ds3_to_csv.py

Uso:
    python3 ds3_to_csv.py input.ds3 output.csv

Lê um arquivo .ds3, encontra frames iniciados por AA 55 AA (3 bytes),
decodifica os campos conforme a tabela encontrada em 'Datalogger S3000.md' 
e grava resultado em um CSV.
"""

import sys
import csv
from pathlib import Path
from typing import List, Tuple

SIGNATURE = bytes([0xAA, 0x55, 0xAA])
FRAME_SIZE = 59

def read_uint16_le(buf: bytes, off: int):
    return int.from_bytes(buf[off:off + 2], byteorder='little', signed=False)

def read_uint8(buf: bytes, off: int):
    return buf[off]

def parse_frame(frame_bytes: bytes):
    o = {}
    o['hex_frame'] = frame_bytes.hex(' ')

    # Campos decodificados
    o['rotacao_rpm'] = read_uint16_le(frame_bytes, 3)
    o['bateria_v'] = read_uint16_le(frame_bytes, 5) / 10.0
    o['map_bar'] = read_uint16_le(frame_bytes, 7) / 100.0

    o['nao_id_0'] = frame_bytes[9:15].hex(' ')

    o['pcomb_bar'] = read_uint16_le(frame_bytes, 15) / 100.0

    o['nao_id_1'] = frame_bytes[17:21].hex(' ')

    o['tps_pct'] = read_uint16_le(frame_bytes, 21) / 10.0
    o['temp_ar_c'] = read_uint16_le(frame_bytes, 23)
    o['temp_motor_c'] = read_uint16_le(frame_bytes, 25)
    o['sonda_nb_v'] = read_uint16_le(frame_bytes, 27) / 100.0
    o['sonda_wb_v'] = read_uint8(frame_bytes, 29) / 100.0

    o['nao_id_2'] = frame_bytes[30:31].hex(' ')

    o['corr_sonda_pct'] = read_uint16_le(frame_bytes, 31)

    o['nao_id_3'] = frame_bytes[33:35].hex(' ')

    o['ponto_ign_deg'] = read_uint16_le(frame_bytes, 35) / 10.0
    o['inj_b1_pct'] = read_uint16_le(frame_bytes, 37)
    o['inj_b2_pct'] = read_uint16_le(frame_bytes, 39)
    o['inj_b3_pct'] = read_uint16_le(frame_bytes, 41)
    o['inj_b1_ms'] = read_uint16_le(frame_bytes, 43) / 100.0
    o['inj_b2_ms'] = read_uint16_le(frame_bytes, 45) / 100.0
    o['inj_b3_ms'] = read_uint16_le(frame_bytes, 47) / 100.0

    booster_raw = read_uint8(frame_bytes, 49)
    o['booster_hex'] = f"0x{booster_raw:02X}"
    booster_map = {0x00: 'nda', 0x01: 'a', 0x10: 'b', 0x11: 'ba'}
    o['booster_desc'] = booster_map.get(booster_raw, '')

    o['nao_id_4'] = frame_bytes[50:53].hex(' ')

    o['fase_ang_deg'] = read_uint16_le(frame_bytes, 53)

    o['nao_id_5'] = frame_bytes[55:57].hex(' ')

    o['roda_tracao_kmh'] = read_uint16_le(frame_bytes, 57) / 10.0

    return o

def find_all_frames(data: bytes):
    frames = []
    idx = 0
    data_len = len(data)
    while True:
        pos = data.find(SIGNATURE, idx)
        if pos == -1:
            break
        if pos + FRAME_SIZE <= data_len:
            frame = data[pos:pos + FRAME_SIZE]
            frames.append((pos, frame))
            idx = pos + FRAME_SIZE
        else:
            break
    return frames

def frames_to_csv(frames: List[Tuple[int, bytes]], csv_path: Path):
    fieldnames = [
        'frame_index', 'file_offset', 'hex_frame',
        'rotacao_rpm', 'bateria_v', 'map_bar',
        'nao_id_0',
        'pcomb_bar', 'nao_id_1',
        'tps_pct', 'temp_ar_c', 'temp_motor_c',
        'sonda_nb_v', 'sonda_wb_v',
        'nao_id_2',
        'corr_sonda_pct', 'nao_id_3',
        'ponto_ign_deg',
        'inj_b1_pct', 'inj_b2_pct', 'inj_b3_pct',
        'inj_b1_ms', 'inj_b2_ms', 'inj_b3_ms',
        'booster_hex', 'booster_desc',
        'nao_id_4',
        'fase_ang_deg', 'nao_id_5',
        'roda_tracao_kmh'
    ]
    with open(csv_path, 'w', newline='', encoding='utf-8', errors='replace') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i, (off, frame_bytes) in enumerate(frames):
            parsed = parse_frame(frame_bytes)
            row = {'frame_index': i, 'file_offset': off}
            row.update(parsed)
            writer.writerow(row)

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 ds3_to_csv.py input.ds3 output.csv")
        sys.exit(1)

    in_path = Path(sys.argv[1]).resolve()
    out_csv = Path(sys.argv[2]).resolve()

    if not in_path.exists():
        print(f"Arquivo não encontrado: {in_path}")
        sys.exit(1)

    try:
        data = in_path.read_bytes()
    except Exception as e:
        print(f"Erro ao ler o arquivo {in_path}: {e}")
        sys.exit(1)

    first_sig = data.find(SIGNATURE)
    if first_sig == -1:
        print("Assinatura AA 55 AA não encontrada no arquivo.")
        sys.exit(1)

    header = data[:first_sig]
    frames = find_all_frames(data)

    print(f"Tamanho do arquivo: {len(data)} bytes")
    print(f"Header de {len(header)} bytes (até offset {first_sig})")
    print(f"{len(frames)} frames completos de {FRAME_SIZE} bytes")

    if len(frames) == 0:
        print("Nenhum frame completo encontrado.")
        sys.exit(1)

    try:
        frames_to_csv(frames, out_csv)
    except Exception as e:
        print(f"Erro ao gravar o CSV: {e}")
        sys.exit(1)

    print(f"CSV gerado com sucesso: {out_csv}")

if __name__ == "__main__":
    main()
