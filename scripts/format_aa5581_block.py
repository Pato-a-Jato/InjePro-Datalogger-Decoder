#!/usr/bin/env python3
"""
format_aa5581_blocks.py

Lê um arquivo hexadecimal contínuo e salva todos os dados (header + blocos iniciados por 'aa 55 81')
em um único arquivo formatado com 16 bytes por linha.
"""

import sys
from pathlib import Path

def split_blocks(data: bytes) -> tuple[bytes, list[bytes]]:
    signature = bytes([0xAA, 0x55, 0x81])
    blocks = []

    # encontra o primeiro bloco
    first_idx = data.find(signature)
    if first_idx == -1:
        return data, []  # não há blocos, tudo é header

    header = data[:first_idx]
    start = first_idx

    while True:
        idx = data.find(signature, start)
        if idx == -1:
            break
        next_idx = data.find(signature, idx + 3)
        block = data[idx: next_idx if next_idx != -1 else None]
        blocks.append(block)
        start = next_idx if next_idx != -1 else len(data)

    return header, blocks

def format_hex_lines(header: bytes, blocks: list[bytes]) -> str:
    lines = []

    # escreve o header (antes do primeiro aa 55 81)
    if header:
        for i in range(0, len(header), 16):
            line = " ".join(f"{b:02x}" for b in header[i:i+16])
            lines.append(line)
        lines.append("")

    # escreve os blocos (cada um com seu próprio aa 55 81)
    for block in blocks:
        lines.append("aa 55 81")
        payload = block[3:]
        for i in range(0, len(payload), 16):
            line = " ".join(f"{b:02x}" for b in payload[i:i+16])
            lines.append(line)
        lines.append("")

    return "\n".join(lines)

def main(input_file: str, output_file: str) -> None:
    hex_str = Path(input_file).read_text().replace("\n", " ").replace("\r", " ")
    data = bytes.fromhex(hex_str)
    header, blocks = split_blocks(data)
    formatted = format_hex_lines(header, blocks)
    Path(output_file).write_text(formatted)
    print(f"Arquivo salvo: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 format_aa5581_block.py entrada.hex saida.hex")
    else:
        main(sys.argv[1], sys.argv[2])
