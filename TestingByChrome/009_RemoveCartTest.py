from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_remove_cart_local():
    print("--- Memulai Test Hapus Produk Secara Lokal ---")

    # 1. KONFIGURASI DRIVER LOKAL
    options = ChromeOptions()
    options.add_argument("--start-maximized") # Browser langsung full screen
    
    # Inisialisasi driver Chrome lokal
    driver = webdriver.Chrome(options=options)
    print("✅ Browser terbuka.")

    try:
        wait = WebDriverWait(driver, 20)

        # --- LANGKAH 1: PRE-CONDITION (ISI KERANJANG DULU) ---
        print("1. Menyiapkan keranjang (Add Product)...")
        driver.get("https://ecommerce-playground.lambdatest.io/")
        time.sleep(1) # Jeda visual

        # Search Produk
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("iPod Nano")
        driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

        # Klik Add to Cart (JS Click)
        print("   -> Menambahkan barang...")
        add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-57")))
        driver.execute_script("arguments[0].click();", add_btn)
        
        # Tunggu notifikasi muncul
        time.sleep(2) 

        # --- LANGKAH 2: MASUK KE CART ---
        print("2. Masuk ke Halaman Cart...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")
        time.sleep(1) # Jeda agar Anda melihat produknya ada di list

        # --- LANGKAH 3: HAPUS PRODUK ---
        print("3. Menghapus produk...")

        # STRATEGI SELECTOR (Tetap digunakan)
        # Mencari tombol dengan class 'btn-danger' (Warna Merah)
        xpath_remove = "//button[contains(@class, 'btn-danger')]"
        remove_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath_remove)))
        
        # Klik Paksa via JS
        driver.execute_script("arguments[0].click();", remove_btn)
        print("   -> Tombol Remove (Merah) diklik.")
        
        # Jeda sebentar untuk melihat proses loading
        time.sleep(2)

        # --- LANGKAH 4: VERIFIKASI ---
        print("4. Verifikasi Hasil...")

        # Kita tunggu sampai teks "empty" muncul di halaman body
        # Ini memastikan halaman sudah selesai refresh setelah penghapusan
        wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Your shopping cart is empty!"))
        
        # Ambil teks konten utama
        content_text = driver.find_element(By.ID, "content").text
        print(f"   Isi Halaman saat ini: {content_text}")

        if "Your shopping cart is empty" in content_text:
            print("✅ TEST PASSED: Keranjang kosong, produk berhasil dihapus!")
        else:
            print("❌ TEST FAILED: Produk masih ada atau pesan error tidak muncul.")

    except Exception as e:
        print(f"❌ Error Terjadi: {e}")

    finally:
        print("Test Selesai. Browser akan menutup dalam 5 detik...")
        time.sleep(5)
        if 'driver' in locals():
            driver.quit()
        print("Sesi selesai.")

if __name__ == "__main__":
    run_remove_cart_local()