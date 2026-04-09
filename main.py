"""
=============================================================================
PAKİZE DİKEN BIO-IT FRAMEWORK (PDBF) - VERSION 2.0.0-DIAMOND
Copyright (c) 2026 Pakize Diken. All Rights Reserved.

Modüller:
1. PD-MIP : Molecular Internet Protocol (Core Diffusion & Packetization)
2. BDE    : Bio-Dynamic Encryption (Biometric seed encryption)
3. MRP    : Microfluidic Routing Protocol (pH & Temp based routing)
4. LLG    : Liquid Logic Gates (Enzyme-substrate threshold logic)
5. BDS    : Bio-Digital Sync (Latency and emission buffer)
6. MEC    : Molecular Error Correction (Self-healing data via repetition)
=============================================================================
"""

import numpy as np
import math
import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

# =============================================================================
# MODULE 1 & 5: PHYSICAL LAWS & BIO-DIGITAL SYNC (BDS)
# =============================================================================
class BioPhysics:
    BOLTZMANN = 1.38e-23
    
    @staticmethod
    def get_diffusion(temp_k: float, viscosity: float, radius: float) -> float:
        """Stokes-Einstein Denklemi"""
        return (BioPhysics.BOLTZMANN * temp_k) / (6 * math.pi * viscosity * radius)

    @staticmethod
    def sync_emission(bit_rate: int):
        """BDS (Bio-Digital Sync): Dijital hızı biyolojik emisyon hızına senkronize eder."""
        delay = 1.0 / bit_rate
        time.sleep(delay / 1000) # Simülasyonu hızlandırmak için milisaniye ölçeğinde

# =============================================================================
# MODULE 2: BIO-DYNAMIC ENCRYPTION (BDE)
# =============================================================================
class BioEncryption:
    @staticmethod
    def generate_bio_key(heart_rate: int, blood_glucose: float) -> str:
        """Kullanıcının anlık biyolojik verilerinden kırılamaz şifre anahtarı üretir."""
        raw_data = f"{heart_rate}_{blood_glucose}_PAKIZEDIKEN"
        return hashlib.sha256(raw_data.encode()).hexdigest()

    @staticmethod
    def xor_cipher(payload: List[int], bio_key: str) -> List[int]:
        """Moleküler veriyi biyolojik anahtarla maskeler."""
        key_bits = [int(b) for c in bio_key for b in format(ord(c), '08b')]
        return [bit ^ key_bits[i % len(key_bits)] for i, bit in enumerate(payload)]

# =============================================================================
# MODULE 6 & 3: ERROR CORRECTION (MEC) & ROUTING (MRP)
# =============================================================================
@dataclass
class PDMolecularPacket:
    source_id: str
    dest_id: str
    target_pH: float        # MRP: Sadece hedef pH'a ulaşınca açılır
    target_temp: float      # MRP: Sadece hedef sıcaklıkta aktifleşir
    payload: List[int]
    sequence_no: int
    
    def apply_mec(self):
        """MEC: Forward Error Correction (Triple Modular Redundancy). Veriyi klonlar."""
        self.payload = [bit for bit in self.payload for _ in range(3)]

# =============================================================================
# MODULE 4: LIQUID LOGIC GATES (LLG)
# =============================================================================
class LiquidLogic:
    @staticmethod
    def threshold_gate(concentration: float, activation_threshold: float) -> int:
        """Hücresel Enzim Mantığı: Konsantrasyon eşiği geçerse reseptör ateşlenir (1)."""
        return 1 if concentration >= activation_threshold else 0

    @staticmethod
    def majority_vote(bits: List[int]) -> int:
        """MEC Çözücü: Biyolojik gürültüde bozulan veriyi onarır."""
        return 1 if sum(bits) >= 2 else 0

# =============================================================================
# THE MASTER KERNEL - PAKIZE DIKEN BIO-OS
# =============================================================================
class PDBioOS:
    def __init__(self, node_id: str, env_pH: float, env_temp: float):
        self.node_id = node_id
        self.env_pH = env_pH
        self.env_temp = env_temp # Kelvin
        self.viscosity = 0.001
        self.radius = 1e-9
        self.D = BioPhysics.get_diffusion(self.env_temp, self.viscosity, self.radius)
        self.mpb = 50000 # Molecules per bit

    def transmit(self, message: str, bio_key: str, dest_pH: float) -> PDMolecularPacket:
        print(f"\n[{self.node_id}] BDE Şifreleme Başlatıldı...")
        binary_payload = [int(b) for b in ''.join(format(ord(c), '08b') for c in message)]
        
        # 1. BDE Şifreleme
        encrypted_payload = BioEncryption.xor_cipher(binary_payload, bio_key)
        
        packet = PDMolecularPacket(
            source_id=self.node_id, dest_id="TUMOR_CELL_01",
            target_pH=dest_pH, target_temp=self.env_temp,
            payload=encrypted_payload, sequence_no=1
        )
        # 2. MEC Hata Düzeltme (Klonlama)
        packet.apply_mec()
        print(f"[{self.node_id}] MEC Uygulandı. Paket boyutu: {len(packet.payload)} molekül kümesi.")
        return packet

    def simulate_bloodstream(self, packet: PDMolecularPacket, distance_um: float):
        distance = distance_um * 1e-6
        received_signals = []
        t_peak = (distance**2) / (6 * self.D)

        print(f"[KAN AKIŞI] Hedefe difüzyon sağlanıyor ({distance_um}um)...")
        for bit in packet.payload:
            BioPhysics.sync_emission(bit_rate=100) # BDS Senkronizasyonu
            q = self.mpb if bit == 1 else 0
            
            # Fick Yasası ve Advektif Gürültü (Biyolojik yıkım)
            conc = (q / (4 * math.pi * self.D * t_peak)**1.5) * math.exp(-(distance**2) / (4 * self.D * t_peak))
            noise = np.random.normal(0, conc * 0.4) if conc > 0 else abs(np.random.normal(0, 1e11))
            received_signals.append(conc + noise)
            
        return received_signals

    def receive(self, packet: PDMolecularPacket, signals: List[float], bio_key: str):
        # 3. MRP (Yönlendirme Kontrolü)
        if abs(self.env_pH - packet.target_pH) > 0.2:
            return "[HATA] MRP Reddedildi: Yanlış Doku pH Seviyesi! İlaç aktifleşmedi."
            
        avg_signal = np.mean(signals)
        raw_bits = []
        
        # 4. LLG (Likit Mantık) ile Sinyal Çözme
        for s in signals:
            raw_bits.append(LiquidLogic.threshold_gate(s, avg_signal))
            
        # 5. MEC ile Hata Onarımı (Self-Healing)
        healed_bits = []
        for i in range(0, len(raw_bits), 3):
            chunk = raw_bits[i:i+3]
            if len(chunk) == 3:
                healed_bits.append(LiquidLogic.majority_vote(chunk))
                
        # 6. BDE Deşifreleme
        decrypted_bits = BioEncryption.xor_cipher(healed_bits, bio_key)
        
        # Karaktere dönüştürme
        chars = [chr(int("".join(map(str, decrypted_bits[i:i+8])), 2)) for i in range(0, len(decrypted_bits), 8)]
        return "".join(chars)

# =============================================================================
# EXECUTION: THE FUTURE OF BIO-NETWORKS
# =============================================================================
if __name__ == "__main__":
    print(f"{'='*70}")
    print(f"PAKİZE DİKEN BIO-IT FRAMEWORK (PDBF) BAŞLATILIYOR...")
    print(f"{'='*70}")

    # Biyometrik Anahtar Üretimi (Kişiye Özel Şifreleme - BDE)
    print("\n[SİSTEM] Biyometrik Veri Okunuyor (Nabız: 72, Glikoz: 98.5)...")
    MASTER_KEY = BioEncryption.generate_bio_key(72, 98.5)

    # Gönderici (Kalp/Damar Yolu) ve Alıcı (Kanserli Doku - Düşük pH)
    SENDER = PDBioOS(node_id="NANO_INJECTOR", env_pH=7.4, env_temp=310.15)
    RECEIVER = PDBioOS(node_id="TUMOR_RECEPTOR", env_pH=6.5, env_temp=310.15) # Tümörler asidiktir (pH 6.5)

    CMD = "APOPTOSIS_PROTOCOL_ALPHA" # Hücre intiharı komutu
    
    # İletim Başlıyor
    packet = SENDER.transmit(CMD, MASTER_KEY, dest_pH=6.5)
    signals = SENDER.simulate_bloodstream(packet, distance_um=15.0)
    
    # Alıcıda İşleme
    print("\n[ALICI] Hedef Dokuya Ulaşıldı. LLG ve MEC Protokolleri Devrede...")
    decoded_msg = RECEIVER.receive(packet, signals, MASTER_KEY)

    print(f"\n{'='*70}")
    print(f">>> PROTOKOL SONUCU <<<")
    print(f"Orijinal Komut: {CMD}")
    print(f"Çözülen Komut : {decoded_msg}")
    
    if decoded_msg == CMD:
        print("\n[BAŞARI] %100 HATA DÜZELTME. HÜCRE İNTİHARI BAŞLATILDI.")
        print("[SİSTEM] TÜM HAKLARI SAKLIDIR (C) 2026 PAKİZE DİKEN.")
    else:
        print("\n[BAŞARISIZ] SİNYAL KAYBI ÇOK YÜKSEK.")
    print(f"{'='*70}")
