from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# --- SETUP KREDENSIAL ---
username = "jihannabilah624"  # Ganti
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q" # Ganti
grid_url = f"https://{username}:{access_key}@hub.lambdatest.com/wd/hub"

# Kita buat list konfigurasi untuk 2 browser berbeda
browsers = [
    {
        "platformName": "Windows 10",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "project": "Cross Browser Test",
        "name": "Tes di Chrome"
    },
    {
        "platformName": "Windows 10",
        "browserName": "Firefox",  # <--- Bedanya di sini
        "browserVersion": "latest",
        "project": "Cross Browser Test",
        "name": "Tes di Firefox"
    }
]

def run_test(capability):
    print(f"--- Memulai tes di {capability['browserName']} ---")
    
    # Opsi khusus untuk LambdaTest Selenium 4
    options = webdriver.ChromeOptions()
    options.set_capability('LT:Options', {
        "username": username,
        "accessKey": access_key,
        "video": True,
        "w3c": True,
        "platformName": capability["platformName"],
        "build": "Sesi Multi-Browser",
        "name": capability["name"]
    })
    # Set browser name langsung
    options.set_capability("browserName", capability["browserName"])
    options.set_capability("browserVersion", capability["browserVersion"])

    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )

    try:
        driver.get("https://www.lambdatest.com/selenium-playground/simple-form-demo")
        
        # Logika tes (Sama seperti sebelumnya)
        pesan = f"Halo dari {capability['browserName']}"
        driver.find_element(By.ID, "user-message").send_keys(pesan)
        driver.find_element(By.ID, "showInput").click()
        
        hasil = driver.find_element(By.ID, "message").text
        
        if pesan == hasil:
            print(f"✅ {capability['browserName']}: PASSED")
            driver.execute_script("lambda-status=passed")
        else:
            print(f"❌ {capability['browserName']}: FAILED")
            driver.execute_script("lambda-status=failed")
            
    except Exception as e:
        print(f"Error di {capability['browserName']}: {e}")
    finally:
        driver.quit()

# Loop untuk menjalankan kedua browser berurutan
for cap in browsers:
    run_test(cap)