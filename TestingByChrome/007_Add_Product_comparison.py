from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_compare_fix_local():
    print("--- Memulai Test Compare Produk (Fixed) ---")

    options = ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    print("✅ Browser terbuka.")

    try:
        wait = WebDriverWait(driver, 15)

        print("1. Membuka Website...")
        driver.get("https://ecommerce-playground.lambdatest.io/")

        # ==========================================
        # PRODUK 1: iPod Nano
        # ==========================================
        print("\n--- [1/3] Memproses iPod Nano ---")
        
        search_box = driver.find_element(By.NAME, "search")
        search_box.clear()
        search_box.send_keys("iPod Nano")
        driver.find_element(By.CSS_SELECTOR, "button.type-text").click()
        
        # Cari tombol Compare Nano
        # Kita pakai XPath yang spesifik mencari tombol compare milik iPod Nano
        # XPath ini artinya: Cari tombol compare yang berada di dalam produk yang punya judul 'iPod Nano'
        xpath_nano_compare = "//h4/a[contains(text(),'iPod Nano')]/ancestor::div[@class='product-thumb']//button[contains(@onclick,'compare.add')]"
        
        btn_compare_nano = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_nano_compare)))
        driver.execute_script("arguments[0].click();", btn_compare_nano)
        print("   -> Klik Compare Nano (Berhasil).")
        
        time.sleep(2) # Biar notifikasi muncul

        # ==========================================
        # PRODUK 2: iPod Touch (BAGIAN YG SERING ERROR)
        # ==========================================
        print("\n--- [2/3] Memproses iPod Touch ---")

        # SOLUSI: Banner hijau "Success" sering menutupi search bar.
        # Cara paling aman: Refresh halaman atau Clear search bar pakai JS.
        print("   -> Membersihkan area pencarian...")
        
        search_box = driver.find_element(By.NAME, "search")
        
        # Hapus isi search bar secara paksa (kadang .clear() biasa kurang bersih)
        driver.execute_script("arguments[0].value = '';", search_box)
        
        # Ketik iPod Touch
        search_box.send_keys("iPod Touch")
        
        # Klik tombol cari (pastikan tidak tertutup banner)
        # Kita pakai JS Click untuk tombol cari agar tembus banner hijau
        search_btn = driver.find_element(By.CSS_SELECTOR, "button.type-text")
        driver.execute_script("arguments[0].click();", search_btn)
        
        print("   -> Mencari 'iPod Touch'...")

        # Pastikan hasil pencarian iPod Touch SUDAH MUNCUL sebelum mencari tombol compare
        # Ini mencegah script mengklik tombol sisa dari halaman sebelumnya
        wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "iPod Touch")))

        # LOGIKA KUAT:
        # Cari tombol compare KHUSUS milik iPod Touch.
        # Jika kita cuma cari "button onclick", bisa jadi malah ketemu tombol produk lain.
        # Kita gunakan XPath Relatif: "Cari Judul iPod Touch -> Naik ke Bapaknya (ancestor) -> Cari tombol compare di situ"
        xpath_touch_compare = "//h4/a[contains(text(),'iPod Touch')]/ancestor::div[@class='product-thumb']//button[contains(@onclick,'compare.add')]"
        
        btn_compare_touch = wait.until(EC.presence_of_element_located((By.XPATH, xpath_touch_compare)))
        
        # Scroll & Click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_compare_touch)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", btn_compare_touch)
        print("   -> Klik Compare Touch (Berhasil).")
        
        time.sleep(2)

        # ==========================================
        # LANGKAH 3: Buka Halaman Compare
        # ==========================================
        print("\n--- [3/3] Buka Halaman Perbandingan ---")

        # Cari Link Product Compare
        compare_link_selector = (By.CSS_SELECTOR, "a[href*='route=product/compare']")
        compare_link = wait.until(EC.presence_of_element_located(compare_link_selector))
        
        # Scroll ke atas karena link ada di header
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", compare_link)
        time.sleep(1)
        
        driver.execute_script("arguments[0].click();", compare_link)
        print("✅ Berhasil masuk halaman Compare.")

        # ==========================================
        # VALIDASI
        # ==========================================
        wait.until(EC.title_contains("Comparison"))
        
        page_source = driver.page_source
        if "iPod Nano" in page_source and "iPod Touch" in page_source:
            print("✅ TEST PASSED: Nano & Touch ada di tabel.")
        else:
            print("❌ TEST FAILED: Produk tidak lengkap.")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        print("\nMenutup browser dalam 5 detik...")
        time.sleep(5)
        driver.quit()

if __name__ == "__main__":
    run_compare_fix_local()