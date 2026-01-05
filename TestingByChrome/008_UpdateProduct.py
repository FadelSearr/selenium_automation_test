from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_update_cart_local():
    print("--- Memulai Test Update Quantity Secara Lokal ---")

    # 1. KONFIGURASI DRIVER LOKAL
    options = ChromeOptions()
    options.add_argument("--start-maximized") # Browser langsung full screen
    
    # Inisialisasi driver Chrome lokal
    driver = webdriver.Chrome(options=options)
    print("✅ Browser terbuka.")

    try:
        wait = WebDriverWait(driver, 20)

        # --- LANGKAH 1: ISI KERANJANG ---
        print("1. Menyiapkan keranjang (Add Product)...")
        driver.get("https://ecommerce-playground.lambdatest.io/")
        time.sleep(1) # Jeda visual

        # Cari barang
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("iPod Nano")
        time.sleep(1) # Jeda visual
        
        driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

        # Klik Add to Cart (JS)
        print("   -> Menambahkan barang...")
        add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-57")))
        driver.execute_script("arguments[0].click();", add_btn)
        
        # Tunggu notifikasi muncul sebentar
        time.sleep(2) 

        # --- LANGKAH 2: MASUK KE CART ---
        print("2. Masuk ke Halaman Cart...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
        time.sleep(1)

        # --- LANGKAH 3: UPDATE QUANTITY ---
        print("3. Mengubah jumlah produk...")
        
        # Cari Input
        qty_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
        qty_input.clear()
        # Kita ketik pelan-pelan (opsional, biar kelihatan berubah)
        qty_input.send_keys("3")
        time.sleep(1) # Jeda agar Anda melihat angka 5 terketik
        print("   -> Input diubah menjadi 5.")

        print("   -> Mencari tombol Update...")
        
        # LOGIKA XPATH (Dipertahankan karena sangat bagus)
        # Mencari tombol refresh/update warna biru
        xpath_update = "//button[@type='submit' and contains(@class, 'btn-primary')]"
        update_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath_update)))
        
        # Klik Paksa via JS
        driver.execute_script("arguments[0].click();", update_btn)
        print("   -> Tombol Update BERHASIL diklik.")
        
        # Jeda sebentar melihat proses reload
        time.sleep(2)

        # --- LANGKAH 4: VERIFIKASI ---
        print("4. Verifikasi Hasil...")
        
        # Tunggu pesan sukses
        success_alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
        pesan_text = success_alert.text
        print(f"   Pesan Website: {pesan_text}")

        if "modified your shopping cart" in pesan_text:
            print("✅ TEST PASSED: Quantity berhasil diupdate!")
        else:
            print("❌ TEST FAILED: Pesan sukses tidak muncul.")

    except Exception as e:
        print(f"❌ Error Terjadi: {e}")

    finally:
        print("Test Selesai. Browser akan menutup dalam 5 detik...")
        time.sleep(5)
        if 'driver' in locals():
            driver.quit()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_update_cart_local()