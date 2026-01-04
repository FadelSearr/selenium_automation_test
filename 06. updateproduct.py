from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- KREDENSIAL ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"

grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

# KONFIGURASI BROWSER
options = ChromeOptions()
options.browser_version = "latest"
options.platform_name = "Windows 11" 

lt_options = {
    "username": username,
    "accessKey": access_key,
    "project": "E-Commerce Testing",
    "build": "Update Cart Test",
    "name": "Update Quantity (Fixed Selector)",
    "w3c": True,
    "plugin": "python-python"
}
options.set_capability('LT:Options', lt_options)

try:
    print(f"Menghubungkan ke Cloud LambdaTest...")
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )
    print("✅ Browser terbuka.")

    wait = WebDriverWait(driver, 20)

    # --- LANGKAH 1: ISI KERANJANG ---
    print("1. Menyiapkan keranjang (Add Product)...")
    driver.get("https://ecommerce-playground.lambdatest.io/")
    
    # Cari barang
    search_box = driver.find_element(By.NAME, "search")
    search_box.clear()
    search_box.send_keys("iPod Nano")
    driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

    # Klik Add to Cart (JS)
    print("   -> Menambahkan barang...")
    add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-57")))
    driver.execute_script("arguments[0].click();", add_btn)
    
    # Tunggu sebentar biar server memproses
    time.sleep(3) 

    # --- LANGKAH 2: MASUK KE CART ---
    print("2. Masuk ke Halaman Cart...")
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart")

    # --- LANGKAH 3: UPDATE QUANTITY ---
    print("3. Mengubah jumlah produk...")
    
    # Cari Input
    qty_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name^='quantity']")))
    qty_input.clear()
    qty_input.send_keys("5")
    print("   -> Input diubah menjadi 5.")

    # --- PERBAIKAN DI SINI ---
    print("   -> Mencari tombol Update...")
  
    xpath_update = "//button[@type='submit' and contains(@class, 'btn-primary')]"
    
    update_btn = wait.until(EC.presence_of_element_located((By.XPATH, xpath_update)))
    
    # Klik Paksa via JS
    driver.execute_script("arguments[0].click();", update_btn)
    print("   -> Tombol Update BERHASIL diklik.")

    # --- LANGKAH 4: VERIFIKASI ---
    print("4. Verifikasi Hasil...")
    
    # Tunggu pesan sukses
    success_alert = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.alert-success")))
    pesan_text = success_alert.text
    print(f"   Pesan Website: {pesan_text}")

    if "modified your shopping cart" in pesan_text:
        print("✅ TEST PASSED: Quantity berhasil diupdate!")
        driver.execute_script("lambda-status=passed")
    else:
        print("❌ TEST FAILED: Pesan sukses tidak muncul.")
        driver.execute_script("lambda-status=failed")

except Exception as e:
    print(f"❌ Error Terjadi: {e}")
    if 'driver' in locals():
        driver.execute_script("lambda-status=failed")

finally:
    if 'driver' in locals():
        driver.quit()
        print("Sesi selesai.")