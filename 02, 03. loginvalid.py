from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- KREDENSIAL LAMBDATEST ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"

def run_login_test():
    # 1. Konfigurasi
    options = ChromeOptions()
    options.platform_name = "Windows 11"
    
    lt_options = {
        "username": username,
        "accessKey": access_key,
        "build": "Sesi: Authentication",
        "name": "Tes Login Kredensial Valid",
        "video": True,
        "w3c": True
    }
    options.set_capability('LT:Options', lt_options)

    # URL Grid LambdaTest
    grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

    driver = webdriver.Remote(command_executor=grid_url, options=options)

    try:
        print("Membuka halaman Login...")
        driver.get("https://the-internet.herokuapp.com/login")

        # 2. INPUT DATA (Menggunakan Kredensial Valid)
        print("Mengisi Username...")
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        
        print("Mengisi Password...")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # 3. KLIK LOGIN
        print("Klik tombol Login...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # 4. VERIFIKASI (ASSERTION)
        wait = WebDriverWait(driver, 5)
        
        # Cek apakah pesan sukses muncul (Elemen hijau di bagian atas)
        flash_message = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
        print(f"Pesan dari sistem: {flash_message}")

        # Validasi Logika
        if "You logged into a secure area" in flash_message:
            print("✅ TEST PASSED: Login Berhasil!")
            driver.execute_script("lambda-status=passed")
        else:
            print("❌ TEST FAILED: Gagal masuk.")
            driver.execute_script("lambda-status=failed")

        # Validasi Tambahan: Cek apakah tombol Logout ada
        logout_btn = driver.find_element(By.CSS_SELECTOR, "a[href='/logout']")
        if logout_btn.is_displayed():
            print("   -> Tombol Logout terlihat (Konfirmasi kedua sukses).")

    except Exception as e:
        print("Terjadi Error:", e)
        driver.execute_script("lambda-status=failed")
        
    finally:
        driver.quit()
        print("Sesi ditutup.")

if __name__ == "__main__":
    run_login_test()