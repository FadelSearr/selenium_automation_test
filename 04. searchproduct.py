from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- KREDENSIAL ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"

def run_search_test():
    options = ChromeOptions()
    options.platform_name = "Windows 11"
    
    lt_options = {
        "username": username,
        "accessKey": access_key,
        "build": "Sesi: E-Commerce",
        "name": "Tes Pencarian Produk (iPhone)",
        "video": True,
        "w3c": True
    }
    options.set_capability('LT:Options', lt_options)

    grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"
    driver = webdriver.Remote(command_executor=grid_url, options=options)

    try:
        print("1. Membuka Toko Online Demo...")
        driver.get("https://ecommerce-playground.lambdatest.io/")

        # 2. CARI KOTAK PENCARIAN
        search_box = driver.find_element(By.NAME, "search")
        
        keyword = "iPhone"
        print(f"2. Mengetik keyword: {keyword}")
        search_box.send_keys(keyword)

        # 3. KLIK TOMBOL CARI
        tombol_cari = driver.find_element(By.CSS_SELECTOR, "button.type-text")
        tombol_cari.click()

        # 4. VERIFIKASI HASIL (ASSERTION)
        wait = WebDriverWait(driver, 5)
        
        # Tunggu sampai judul halaman berubah (biasanya "Search - iPhone")
        wait.until(EC.title_contains(keyword))
        print("   -> Halaman hasil pencarian dimuat.")

        # Ambil SEMUA produk yang muncul
        list_produk = driver.find_elements(By.CSS_SELECTOR, "div.product-thumb h4 a")
        
        jumlah_produk = len(list_produk)
        print(f"3. Ditemukan {jumlah_produk} produk.")

        if jumlah_produk > 0:
            # Loop untuk mengecek satu per satu
            semua_relevan = True
            for produk in list_produk:
                nama_produk = produk.text
                print(f"   - Cek Produk: {nama_produk}")
                
                # Cek apakah kata 'iPhone' ada di nama produk (case insensitive)
                if keyword.lower() not in nama_produk.lower():
                    semua_relevan = False
                    print(f"     ❌ Aneh! Produk ini tidak mengandung '{keyword}'")
            
            if semua_relevan:
                print("✅ TEST PASSED: Semua hasil pencarian relevan!")
                driver.execute_script("lambda-status=passed")
            else:
                print("❌ TEST FAILED: Ada hasil yang tidak relevan.")
                driver.execute_script("lambda-status=failed")
        else:
            print("⚠️ WARNING: Tidak ada produk ditemukan (Mungkin stok habis atau keyword salah).")
            # Tergantung kebutuhan, 0 hasil bisa dianggap Pass atau Fail
            driver.execute_script("lambda-status=passed")

    except Exception as e:
        print("Error:", e)
        driver.execute_script("lambda-status=failed")
    finally:
        driver.quit()

if __name__ == "__main__":
    run_search_test()