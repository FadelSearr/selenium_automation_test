from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- KREDENSIAL ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"

def run_registration_test():
    # 1. Konfigurasi
    options = ChromeOptions()
    options.platform_name = "Windows 11"
    
    lt_options = {
        "username": username,
        "accessKey": access_key,
        "build": "Sesi: Registration Form",
        "name": "Tes Registrasi Data Valid", # Nama Test
        "video": True,
        "w3c": True
    }
    options.set_capability('LT:Options', lt_options)

    # URL Grid
    grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

    driver = webdriver.Remote(command_executor=grid_url, options=options)

    try:
        print("Membuka halaman formulir...")
        driver.get("https://www.lambdatest.com/selenium-playground/input-form-demo")
        
        # Maksimalkan layar agar semua elemen terlihat
        driver.maximize_window()

        # 2. PENGISIAN DATA (Valid Data)
        print("Mulai mengisi formulir...")
        
        # A. Nama
        driver.find_element(By.ID, "name").send_keys("Budi Santoso")
        
        # B. Email (Harus format email valid)
        driver.find_element(By.ID, "inputEmail4").send_keys("budi.test@contoh.com")
        
        # C. Password
        driver.find_element(By.ID, "inputPassword4").send_keys("Rahasia123!")
        
        # D. Company & Website
        driver.find_element(By.ID, "company").send_keys("PT Maju Mundur")
        driver.find_element(By.ID, "websitename").send_keys("www.majumundur.com")
        
        # E. Negara (Dropdown/Select) - Bagian Paling Penting!
        elemen_negara = driver.find_element(By.NAME, "country")
        dropdown = Select(elemen_negara)
        dropdown.select_by_visible_text("United States") # Pilih negara
        
        # F. Kota, Alamat, Kode Pos
        driver.find_element(By.ID, "inputCity").send_keys("New York")
        driver.find_element(By.ID, "inputAddress1").send_keys("Jalan 5th Avenue No 10")
        driver.find_element(By.ID, "inputAddress2").send_keys("Apartment 4B")
        driver.find_element(By.ID, "inputState").send_keys("NY")
        driver.find_element(By.ID, "inputZip").send_keys("10001")
        
        print("Data selesai diisi.")

        # 3. SUBMIT
        tombol_submit = driver.find_element(By.XPATH, "//button[text()='Submit']")
        tombol_submit.click()
        print("Tombol Submit diklik.")

        # 4. VERIFIKASI (ASSERTION)
        wait = WebDriverWait(driver, 5)
        
        # Mencari elemen pesan sukses (biasanya class 'success-msg')
        pesan_sukses = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "success-msg")))
        teks_muncul = pesan_sukses.text
        
        print(f"Pesan dari website: {teks_muncul}")

        # Cek apakah pesannya sesuai harapan
        if "Thanks for contacting us" in teks_muncul:
            print("✅ TEST PASSED: Registrasi Berhasil!")
            driver.execute_script("lambda-status=passed")
        else:
            print("❌ TEST FAILED: Pesan sukses tidak muncul.")
            driver.execute_script("lambda-status=failed")

    except Exception as e:
        print("Terjadi Error:", e)
        driver.execute_script("lambda-status=failed")
        
    finally:
        driver.quit()
        print("Sesi ditutup.")

if __name__ == "__main__":
    run_registration_test()