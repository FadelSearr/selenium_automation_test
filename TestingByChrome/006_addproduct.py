from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_add_to_cart_local():
    print("--- Memulai Test Add to Cart Secara Lokal ---")

    # 1. KONFIGURASI DRIVER LOKAL
    options = ChromeOptions()
    options.add_argument("--start-maximized") # Browser langsung full screen
    
    # Inisialisasi driver Chrome lokal
    driver = webdriver.Chrome(options=options)
    print("✅ Browser terbuka.")

    try:
        # LOGIKA TEST
        wait = WebDriverWait(driver, 20)

        # A. Buka Website & Search
        print("1. Membuka Website...")
        driver.get("https://ecommerce-playground.lambdatest.io/")
        time.sleep(1) # Jeda visual
        
        print("   Mencari 'iPod Nano'...")
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("iPod Nano")
        time.sleep(1) # Jeda visual
        
        driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

        # B. Temukan Tombolnya
        print("2. Mencari tombol 'Add to Cart'...")
        # Kita tunggu sampai tombol ada di DOM
        add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-57")))
        
        # C. EKSEKUSI KLIK (SOLUSI FIX - JavaScript)
        # Tombol ini sering tertutup overlay gambar saat mouse bergerak, jadi click() biasa sering gagal.
        # Kita paksa klik langsung via mesin browser (JavaScript).
        print("   Mengeksekusi JavaScript Click (Force Click)...")
        driver.execute_script("arguments[0].click();", add_btn)
        
        # D. Tunggu & Buka Keranjang
        print("⏳ Menunggu proses server (notifikasi muncul)...")
        time.sleep(2) # Memberi waktu notifikasi "Success" muncul sebentar
        
        print("🚀 3. Membuka Halaman Keranjang...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")

        # E. Verifikasi
        # Judul halaman keranjang biasanya "Shopping Cart"
        print(f"   Judul Halaman saat ini: {driver.title}")
        
        if "Shopping Cart" in driver.title:
            print("✅ TEST PASSED: Berhasil masuk ke halaman keranjang.")
        else:
            print("❌ TEST FAILED: Judul halaman salah/tidak masuk keranjang.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        print("Test Selesai. Browser akan menutup dalam 5 detik...")
        time.sleep(5) # Jeda agar Anda bisa melihat hasil akhir di keranjang
        if 'driver' in locals():
            driver.quit()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_add_to_cart_local()