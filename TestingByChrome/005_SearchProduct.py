import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_search_test():
    print("--- Memulai Test Secara Lokal ---")
    
    # 1. SETUP DRIVER LOKAL
    # Kita pakai webdriver.Chrome() agar muncul di layar laptop
    options = ChromeOptions()
    # options.add_argument("--start-maximized") # Opsional: Agar browser langsung full screen
    
    # Inisialisasi driver lokal (Pastikan Google Chrome sudah terinstall)
    # Selenium versi terbaru (4.6+) otomatis mengurus drivernya.
    driver = webdriver.Chrome(options=options)

    try:
        print("1. Membuka Toko Online Demo...")
        driver.get("https://ecommerce-playground.lambdatest.io/")

        # 2. CARI KOTAK PENCARIAN
        search_box = driver.find_element(By.NAME, "search")
        
        keyword = "iPhone"
        print(f"2. Mengetik keyword: {keyword}")
        search_box.send_keys(keyword)
        
        # Biar kelihatan mengetik (opsional, hanya untuk visual)
        time.sleep(1) 

        # 3. KLIK TOMBOL CARI
        tombol_cari = driver.find_element(By.CSS_SELECTOR, "button.type-text")
        tombol_cari.click()

        # 4. VERIFIKASI HASIL (ASSERTION)
        wait = WebDriverWait(driver, 10) # Saya naikkan jadi 10 detik jaga-jaga internet lambat
        
        wait.until(EC.title_contains(keyword))
        print("   -> Halaman hasil pencarian dimuat.")

        # Ambil SEMUA produk yang muncul
        list_produk = driver.find_elements(By.CSS_SELECTOR, "div.product-thumb h4 a")
        
        jumlah_produk = len(list_produk)
        print(f"3. Ditemukan {jumlah_produk} produk.")

        if jumlah_produk > 0:
            semua_relevan = True
            for produk in list_produk:
                nama_produk = produk.text
                print(f"   - Cek Produk: {nama_produk}")
                
                if keyword.lower() not in nama_produk.lower():
                    semua_relevan = False
                    print(f"     ❌ Aneh! Produk ini tidak mengandung '{keyword}'")
            
            if semua_relevan:
                print("✅ TEST PASSED: Semua hasil pencarian relevan!")
            else:
                print("❌ TEST FAILED: Ada hasil yang tidak relevan.")
        else:
            print("⚠️ WARNING: Tidak ada produk ditemukan.")

    except Exception as e:
        print("Error:", e)
    finally:
        print("Test Selesai. Browser akan menutup dalam 5 detik...")
        time.sleep(5) # Jeda waktu agar Anda bisa melihat hasil akhir sebelum menutup
        driver.quit()

if __name__ == "__main__":
    run_search_test()