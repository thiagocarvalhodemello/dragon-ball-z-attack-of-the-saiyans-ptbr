#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dragon Ball Z: Attack of the Saiyans — Aplicador de Patch PT-BR
Compatível com ROMs USA (BRPE - A9F0B8F9) e Europa (BRPP - 4E8C3E1B).
"""

import sys
import os
import struct
import zlib
import hashlib

def decode_vli(data, pos):
    val = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        val += (b & 0x7F) << shift
        if b & 0x80:
            break
        shift += 7
        val += 1 << shift
    return val, pos

def apply_bps_patch(source_bytes: bytes, patch_bytes: bytes) -> bytes:
    if patch_bytes[:4] != b'BPS1':
        raise ValueError("Arquivo de patch inválido (não é formato BPS1).")
    
    pos = 4
    src_sz, pos = decode_vli(patch_bytes, pos)
    tgt_sz, pos = decode_vli(patch_bytes, pos)
    meta_sz, pos = decode_vli(patch_bytes, pos)
    metadata = patch_bytes[pos : pos + meta_sz].decode('utf-8', errors='replace')
    pos += meta_sz
    
    if len(source_bytes) != src_sz:
        raise ValueError(f"Tamanho da ROM incorreto! Esperado: {src_sz} bytes, obtido: {len(source_bytes)} bytes.")
    
    target = bytearray(tgt_sz)
    tgt_out = 0
    
    while pos < len(patch_bytes) - 12:
        action, pos = decode_vli(patch_bytes, pos)
        mode = action & 3
        length = (action >> 2) + 1
        
        if mode == 0:  # SourceRead
            target[tgt_out : tgt_out + length] = source_bytes[tgt_out : tgt_out + length]
        elif mode == 1:  # TargetRead
            target[tgt_out : tgt_out + length] = patch_bytes[pos : pos + length]
            pos += length
        tgt_out += length

    # Verificações de integridade do BPS
    src_crc, tgt_crc, p_crc = struct.unpack_from('<III', patch_bytes, len(patch_bytes) - 12)
    actual_src_crc = zlib.crc32(source_bytes) & 0xFFFFFFFF
    actual_tgt_crc = zlib.crc32(target) & 0xFFFFFFFF
    actual_p_crc = zlib.crc32(patch_bytes[:-4]) & 0xFFFFFFFF
    
    if actual_src_crc != src_crc:
        raise ValueError(f"Checksum da ROM base incompatível! Esperado: {hex(src_crc)}, obtido: {hex(actual_src_crc)}")
    if actual_tgt_crc != tgt_crc:
        raise ValueError(f"Falha de integridade na aplicação do patch! Checksum esperado: {hex(tgt_crc)}, obtido: {hex(actual_tgt_crc)}")
    if actual_p_crc != p_crc:
        raise ValueError("O arquivo de patch está corrompido (patch CRC mismatch).")
        
    return bytes(target)

def main():
    print("=" * 70)
    print(" Dragon Ball Z: Attack of the Saiyans — Tradução PT-BR")
    print(" Aplicador de Patch Automático (Suporta Versões USA e Europa)")
    print("=" * 70)

    # Identificar diretório base
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Identificar ROM base
    rom_path = None
    if len(sys.argv) > 1:
        rom_path = sys.argv[1]
    else:
        # Tentar localizar automaticamente arquivos .nds na pasta atual
        candidates = [f for f in os.listdir(base_dir) if f.lower().endswith('.nds') and not ('pt-br' in f.lower() or 'ptbr' in f.lower())]
        if candidates:
            rom_path = os.path.join(base_dir, candidates[0])
            
    if not rom_path or not os.path.exists(rom_path):
        print("\nUso:")
        print("  python apply_patch.py \"caminho/para/Dragon Ball Z - Attack of the Saiyans.nds\"\n")
        print("Nenhuma ROM compatível foi encontrada automaticamente no diretório atual.")
        sys.exit(1)

    print(f"\n[+] Lendo ROM base: {os.path.basename(rom_path)}")
    with open(rom_path, 'rb') as f:
        rom_data = f.read()

    crc_val = format(zlib.crc32(rom_data) & 0xFFFFFFFF, '08X')
    md5_val = hashlib.md5(rom_data).hexdigest()
    print(f"    Tamanho: {len(rom_data):,} bytes")
    print(f"    CRC32:   {crc_val}")
    print(f"    MD5:     {md5_val}")

    # Determinar versão da ROM
    patch_file = None
    version_name = None
    out_default_name = None

    if crc_val == '4E8C3E1B':
        version_name = "Europa (BRPP - En,Fr,De,Es,It)"
        patch_file = os.path.join(base_dir, "DBZ_Attack_of_the_Saiyans_EUR_PTBR.bps")
        out_default_name = "Dragon Ball Z - Attack of the Saiyans (EUR) (PT-BR).nds"
    elif crc_val == 'A9F0B8F9':
        version_name = "USA (BRPE - En,Fr)"
        patch_file = os.path.join(base_dir, "DBZ_Attack_of_the_Saiyans_PTBR.bps")
        out_default_name = "Dragon Ball Z - Attack of the Saiyans (USA) (PT-BR).nds"
    else:
        print(f"\n[!] AVISO: Checksum CRC32 ({crc_val}) não corresponde a nenhuma ROM limpa homologada.")
        print("    ROMs aceitas:")
        print("    - USA (BRPE): CRC32 A9F0B8F9")
        print("    - EUR (BRPP): CRC32 4E8C3E1B")
        sys.exit(1)

    print(f"[+] Versão identificada: {version_name}")
    print(f"[+] Arquivo de patch selecionado: {os.path.basename(patch_file)}")

    if not os.path.exists(patch_file):
        print(f"\n[!] Erro: Arquivo de patch não encontrado: {patch_file}")
        sys.exit(1)

    with open(patch_file, 'rb') as f:
        patch_data = f.read()

    print("[+] Aplicando patch de tradução...")
    try:
        patched_data = apply_bps_patch(rom_data, patch_data)
    except Exception as e:
        print(f"\n[!] Falha ao aplicar patch: {e}")
        sys.exit(1)

    out_path = os.path.join(base_dir, out_default_name)
    with open(out_path, 'wb') as f:
        f.write(patched_data)

    out_crc = format(zlib.crc32(patched_data) & 0xFFFFFFFF, '08X')
    out_md5 = hashlib.md5(patched_data).hexdigest()
    out_sha1 = hashlib.sha1(patched_data).hexdigest()
    out_sha256 = hashlib.sha256(patched_data).hexdigest()

    print("\n" + "=" * 70)
    print(" PATCH APLICADO COM SUCESSO!")
    print("=" * 70)
    print(f" Arquivo gerado:  {out_default_name}")
    print(f" Tamanho:         {len(patched_data):,} bytes")
    print(f" CRC32:           {out_crc}")
    print(f" MD5:             {out_md5}")
    print(f" SHA-1:           {out_sha1}")
    print(f" SHA-256:         {out_sha256}")
    print("=" * 70)
    print("Aproveite o jogo totalmente em Português do Brasil no seu emulador ou console!\n")

if __name__ == '__main__':
    main()
