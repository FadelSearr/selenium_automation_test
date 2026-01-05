from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def run_checkout_no_validation():
    print("--- E2E Checkout: Direct (Tanpa Validasi Akhir) ---")

    # KREDENSIAL
    user_email = "johndoe321@gmail.com"
    user_password = "1234"

    # SETUP BROWSER
    options = ChromeOptions()
    options.add_argument("--start-maximized") 
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # -------------------------------------------
        # STEP 1: LOGIN
        # -------------------------------------------
        print("\n[1] Login...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")
        
        wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(user_email)
        driver.find_element(By.ID, "input-password").send_keys(user_password)
        driver.find_element(By.CSS_SELECTOR, "input[value='Login']").click()
        
        wait.until(EC.title_is("My Account"))
        print("    ✅ Login Sukses.")

        # -------------------------------------------
        # STEP 2: ADD PRODUCT
        # -------------------------------------------
        print("\n[2] Add to Cart...")
        # Search & Add palm treo pro
        search_input = wait.until(EC.element_to_be_clickable((By.NAME, "search")))
        search_input.clear()
        search_input.send_keys("Palm Treo Pro")
        driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

        # Klik Add to Cart
        add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-64")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", add_btn)
        time.sleep(2) # Tunggu notifikasi

        # -------------------------------------------
        # STEP 3: CHECKOUT (LANGSUNG GAS)
        # -------------------------------------------
        print("\n[3] Masuk Checkout & Proses...")
        driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/checkout")
        wait.until(EC.title_contains("Checkout"))

        # Kita asumsikan alamat lama otomatis terpilih.
        print("    -> Menunggu loading data lama (3 detik)...")
        time.sleep(3) 

        # --- TERMS & CONDITIONS ---
        print("    -> Checklist Terms & Conditions...")
        terms_chk = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='input-agree']")))
        driver.execute_script("arguments[0].click();", terms_chk)

        # --- KLIK CONTINUE ---
        print("    -> Klik Continue...")
        continue_btn = driver.find_element(By.ID, "button-save")
        driver.execute_script("arguments[0].click();", continue_btn)

        # -------------------------------------------
        # STEP 4: FINAL CONFIRMATION
        # -------------------------------------------
        print("\n[4] Confirm Order...")
        
        # Tunggu tombol Confirm muncul
        confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "button-confirm")))
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_btn)
        time.sleep(1)
        
        # KLIK TERAKHIR
        driver.execute_script("arguments[0].click();", confirm_btn)
        print("    ✅ Tombol CONFIRM diklik! (Selesai)")

    except Exception as e:
        print(f"❌ Error Terjadi: {e}")

    finally:
        print("\nMenutup browser dalam 5 detik...")
        # Saya beri waktu 5 detik agar Anda bisa lihat halaman suksesnya muncul
        time.sleep(5)
        if 'driver' in locals():
            driver.quit()
        print("Sesi Selesai.")

if __name__ == "__main__":
    run_checkout_no_validation()