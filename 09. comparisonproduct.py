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
    "build": "Comparison Product",
    "name": "Click Compare via Link URL",
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

    driver.get("https://ecommerce-playground.lambdatest.io/")

    # PRODUK 1: iPod Nano
    print("\nMemproses iPod Nano")
    
    # Search
    search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search input[name='search']")))
    search_input.clear()
    search_input.send_keys("iPod Nano")
    driver.find_element(By.CSS_SELECTOR, "div#search button[type='submit']").click()
    
    # Add Compare
    btn_compare_nano = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick*='compare.add']")))
    driver.execute_script("arguments[0].click();", btn_compare_nano)
    print("   -> Klik Compare Nano.")
    time.sleep(1) # Jeda proses

    # PRODUK 2: iPod Touch
    print("\nMemproses iPod Touch")

    # Search Lagi
    search_input_2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div#search input[name='search']")))
    search_input_2.click()
    search_input_2.clear()
    search_input_2.send_keys("iPod Touch")
    driver.find_element(By.CSS_SELECTOR, "div#search button[type='submit']").click()

    # Tunggu Hasil
    wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "iPod Touch")))
    
    # Add Compare
    btn_compare_touch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[onclick*='compare.add']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_compare_touch)
    driver.execute_script("arguments[0].click();", btn_compare_touch)
    print("   -> Klik Compare Touch.")
    
    # Tunggu sebentar agar angka di tombol berubah jadi (2)
    time.sleep(2)

    # Klik Tombol "Product Compare"
    print("\nMencari Tombol 'Product Compare")

    compare_btn_selector = (By.CSS_SELECTOR, "a[href*='route=product/compare']")
    
    try:
        # 1. Tunggu tombol link muncul di DOM
        compare_link = wait.until(EC.presence_of_element_located(compare_btn_selector))
        
        # 2. Scroll ke elemen tersebut (PENTING: kadang ada di header paling atas)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", compare_link)
        time.sleep(1) # Jeda setelah scroll
        
        # 3. Klik Paksa dengan JS (Solusi anti-gagal)
        driver.execute_script("arguments[0].click();", compare_link)
        print("✅ Tombol 'Product Compare' berhasil diklik (via Link URL).")
        
    except Exception as click_err:
        print(f"⚠️ Gagal klik tombol utama. Mencoba alternatif pencarian teks...")
        # Backup: Cari elemen apapun yang berisi tulisan "Product Compare"
        backup_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Product Compare")
        driver.execute_script("arguments[0].click();", backup_link)

    # VALIDASI AKHIR
    wait.until(EC.title_contains("Comparison"))
    
    page_source = driver.page_source
    if "iPod Nano" in page_source and "iPod Touch" in page_source:
        print("✅ TEST PASSED: Nano & Touch ada di tabel.")
        driver.execute_script("lambda-status=passed")
    else:
        print(f"❌ TEST FAILED: Produk tidak lengkap.")
        driver.execute_script("lambda-status=failed")

except Exception as e:
    print(f"Error: {e}")
    if 'driver' in locals():
        driver.execute_script("lambda-status=failed")

finally:
    if 'driver' in locals():
        driver.quit()
        print("Sesi selesai.")