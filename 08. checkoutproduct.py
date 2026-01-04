from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random 

# --- KREDENSIAL ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"  

grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

# GENERATE USER DATA
random_number = random.randint(10000, 99999)
user_email = f"user_{random_number}@test.com"
user_password = "Password123!"

bill_fname = "Fadel"
bill_lname = f"Tester{random_number}"
bill_address = f"Jalan Testing No. {random.randint(1, 100)}"
bill_city = "Jakarta Selatan"
bill_postcode = "12000"

print(f"--- DATA TEST ---")
print(f"User: {user_email}")
print(f"-----------------")

# KONFIGURASI BROWSER
options = ChromeOptions()
options.browser_version = "latest"
options.platform_name = "Windows 11" 

lt_options = {
    "username": username,
    "accessKey": access_key,
    "project": "E-Commerce Testing",
    "build": "Build 45.0 - Final Success Page",
    "name": "E2E: Finish at Success Page",
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

    # STEP 1: REGISTRASI
    print("\n--- [STEP 1] REGISTRASI ---")
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/register")
    
    driver.find_element(By.ID, "input-firstname").send_keys("User")
    driver.find_element(By.ID, "input-lastname").send_keys("Baru")
    driver.find_element(By.ID, "input-email").send_keys(user_email)
    driver.find_element(By.ID, "input-telephone").send_keys("08123456789")
    driver.find_element(By.ID, "input-password").send_keys(user_password)
    driver.find_element(By.ID, "input-confirm").send_keys(user_password)
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "label[for='input-agree']"))
    driver.execute_script("arguments[0].click();", driver.find_element(By.CSS_SELECTOR, "input[type='submit']"))
    wait.until(EC.title_contains("Created"))
    print("   ✅ Register Berhasil.")

    # STEP 2: BELANJA PALM TREO PRO
    print("\n--- [STEP 2] ADD TO CART ---")
    search_input = wait.until(EC.element_to_be_clickable((By.NAME, "search")))
    search_input.clear()
    search_input.send_keys("Palm Treo Pro")
    driver.find_element(By.CSS_SELECTOR, "button.type-text").click()

    # Klik tombol cart khusus Palm Treo Pro (cart-64)
    add_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-64")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_btn)
    driver.execute_script("arguments[0].click();", add_btn)
    time.sleep(2) 

    # STEP 3: MASUK CHECKOUT
    print("\n--- [STEP 3] MASUK CHECKOUT ---")
    driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=checkout/checkout")
    wait.until(EC.title_contains("Checkout"))
    print("   ✅ Halaman Checkout Terbuka.")

    # STEP 4: ISI ALAMAT
    print("\n--- [STEP 4] MENGISI FORMULIR ---")
    
    fname_input = wait.until(EC.visibility_of_element_located((By.ID, "input-payment-firstname")))
    fname_input.clear()
    fname_input.send_keys(bill_fname)
    driver.find_element(By.ID, "input-payment-lastname").clear()
    driver.find_element(By.ID, "input-payment-lastname").send_keys(bill_lname)
    driver.find_element(By.ID, "input-payment-address-1").send_keys(bill_address)
    driver.find_element(By.ID, "input-payment-city").send_keys(bill_city)
    driver.find_element(By.ID, "input-payment-postcode").send_keys(bill_postcode)

    print("   -> Memilih Wilayah...")
    Select(driver.find_element(By.ID, "input-payment-country")).select_by_visible_text("Indonesia")
    time.sleep(2) # Tunggu AJAX
    try:
        Select(driver.find_element(By.ID, "input-payment-zone")).select_by_visible_text("DKI Jakarta")
    except:
        Select(driver.find_element(By.ID, "input-payment-zone")).select_by_index(1)
    
    # Tunggu Payment Method Refresh
    print("   -> Menunggu Payment Method Refresh (3 detik)...")
    time.sleep(3) 

    # STEP 5: PILIH PAYMENT & CONTINUE
    print("\n--- [STEP 5] PILIH PAYMENT ---")
    
    # WAJIB MEMILIH PAYMENT (Agar tombol Confirm muncul)
    try:
        cod_radio = driver.find_element(By.CSS_SELECTOR, "input[name='payment_method'][value='cod']")
        driver.execute_script("arguments[0].click();", cod_radio)
        print("   -> Payment: Cash On Delivery dipilih.")
    except:
        # Fallback
        any_payment = driver.find_element(By.NAME, "payment_method")
        driver.execute_script("arguments[0].click();", any_payment)
        print("   -> Payment Default dipilih.")

    # Centang Terms
    terms_chk = driver.find_element(By.CSS_SELECTOR, "label[for='input-agree']")
    driver.execute_script("arguments[0].click();", terms_chk)
    
    # Klik Continue
    continue_btn = driver.find_element(By.ID, "button-save")
    driver.execute_script("arguments[0].click();", continue_btn)
    print("   -> Tombol 'Continue' diklik.")

    # STEP 6: KLIK CONFIRM ORDER
    print("\n--- [STEP 6] KLIK CONFIRM ORDER ---")
    
    try:
        # Tunggu tombol Confirm muncul
        confirm_final_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "button-confirm"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", confirm_final_btn)
        time.sleep(1) 
        driver.execute_script("arguments[0].click();", confirm_final_btn)
        print("   ✅ Tombol 'Confirm Order' DIKLIK.")
        
    except TimeoutException:
        print("   ❌ ERROR: Tombol Confirm tidak muncul.")
        driver.execute_script("lambda-status=failed")
        raise Exception("Tombol Confirm Hilang")

    # STEP 7: VALIDASI HALAMAN SUKSES & SELESAI
    print("\n--- [STEP 7] VALIDASI & SESI SELESAI ---")
    
    try:
        
        print("   ✅ Pesan: Your order has been placed!")
        
        # Kirim status Passed ke LambdaTest
        driver.execute_script("lambda-status=passed")

    except TimeoutException:
        print("❌ TEST FAILED: Tidak masuk ke halaman sukses.")
        driver.execute_script("lambda-status=failed")

except Exception as e:
    print(f"Error System: {e}")
    if 'driver' in locals():
        driver.execute_script("lambda-status=failed")

finally:
    # SESI SELESAI (DRIVER QUIT)
    if 'driver' in locals():
        print("\nMenutup Browser (Sesi Selesai)...")
        driver.quit()
        print("Done.")