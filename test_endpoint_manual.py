#!/usr/bin/env python
"""
Manual test script untuk endpoint reset-all
Mengecek apakah endpoint berfungsi dengan benar
"""

import requests
import json

# Server endpoint
BASE_URL = "http://localhost:5000"

def test_reset_endpoint():
    """Test endpoint reset-all"""
    
    print("=" * 60)
    print("TESTING RESET-ALL ENDPOINT")
    print("=" * 60)
    
    # Endpoint untuk reset
    url = f"{BASE_URL}/api/edc-machines/reset-all"
    
    print(f"\n1. Memanggil endpoint POST: {url}")
    
    try:
        response = requests.post(url)
        
        print(f"\n   Status Code: {response.status_code}")
        print(f"   Response:")
        
        result = response.json()
        print(f"   {json.dumps(result, indent=2)}")
        
        # Verifikasi response
        if response.status_code == 200:
            if result.get('success'):
                print("\n✓ BERHASIL: Endpoint reset-all berfungsi dengan baik!")
                print(f"   - EDC machines direset: {result['data']['edc_machines_reset']}")
                print(f"   - Agents direset: {result['data']['agents_reset']}")
                print(f"   - Cash flows dihapus: {result['data']['cashflows_deleted']}")
                return True
            else:
                print("\n✗ GAGAL: Response tidak success")
                return False
        else:
            print(f"\n✗ GAGAL: Status code tidak 200 (dapat {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Tidak dapat terhubung ke server")
        print("   Pastikan Flask server sudah berjalan di http://localhost:5000")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return False

def verify_reset_effects():
    """Verify bahwa endpoint benar-benar mereset data"""
    
    print("\n" + "=" * 60)
    print("VERIFYING RESET EFFECTS")
    print("=" * 60)
    
    # Ini membutuhkan authentication untuk mengecek data
    # Untuk sekarang kita hanya print informasi
    print("\nUntuk memverifikasi efek reset, Anda perlu:")
    print("1. Membuat EDC machine dengan saldo")
    print("2. Membuat cash flow")
    print("3. Memanggil endpoint /api/edc-machines/reset-all")
    print("4. Mengecek apakah saldo EDC dan cash flow telah direset")
    
if __name__ == '__main__':
    success = test_reset_endpoint()
    verify_reset_effects()
    
    print("\n" + "=" * 60)
    if success:
        print("TEST COMPLETED SUCCESSFULLY ✓")
    else:
        print("TEST FAILED ✗")
    print("=" * 60)
