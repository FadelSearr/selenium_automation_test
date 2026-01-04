from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- KREDENSIAL ---
username = "jihannabilah624"
access_key = "LT_jPmVCl9oWJsWNGFOJGktJMsZQnmCHbqV0Z8OnCT2G0hr70Q"


def run_tc010_password_confirmation_test():
    """
    TC-010: Form Validation pada Registration
    Password dan Confirm Password tidak sama
    """

    options = ChromeOptions()
    options.platform_name = "Windows 11"
    options.browser_version = "latest"

    options.set_capability("LT:Options", {
        "username": username,
        "accessKey": access_key,
        "build": "Validation Registration",
        "name": "TC-010 Password Confirmation Validation",
        "video": True,
        "w3c": True
    })

    driver = webdriver.Remote(
        command_executor="https://hub.lambdatest.com/wd/hub",
        options=options
    )

    wait = WebDriverWait(driver, 20)

    try:
        # STEP 1: Open Register Page
        print("🔹 Membuka halaman registrasi...")
        driver.get(
            "https://ecommerce-playground.lambdatest.io/index.php?route=account/register"
        )

        wait.until(EC.presence_of_element_located((By.ID, "input-firstname")))

        # STEP 2: Fill Form
        print("🔹 Mengisi form registrasi")

        driver.find_element(By.ID, "input-firstname").send_keys("John")
        driver.find_element(By.ID, "input-lastname").send_keys("Doe")

        unique_email = f"john.{int(time.time())}@test.com"
        driver.find_element(By.ID, "input-email").send_keys(unique_email)

        driver.find_element(By.ID, "input-telephone").send_keys("081234567890")

        driver.find_element(By.ID, "input-password").send_keys("123")
        driver.find_element(By.ID, "input-confirm").send_keys("456")

        # STEP 3: Select Newsletter = No (WAJIB)
        print("🔹 Pilih Newsletter: No")
        newsletter_no = driver.find_element(By.XPATH, "//input[@name='newsletter' and @value='0']")
        driver.execute_script("arguments[0].click();", newsletter_no)

        # STEP 4: Agree Privacy Policy
        print("🔹 Centang Privacy Policy")
        agree = driver.find_element(By.NAME, "agree")
        driver.execute_script("arguments[0].click();", agree)

        # STEP 5: Submit Form
        print("🔹 Submit form")
        continue_btn = driver.find_element(By.XPATH, "//input[@value='Continue']")
        driver.execute_script("arguments[0].click();", continue_btn)

        # STEP 6: Verify Error Message
        print("🔹 Verifikasi pesan error")

        error_message = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(text(),'Password confirmation')]")
            )
        )

        error_text = error_message.text
        print("Pesan Error:", error_text)

        assert "Password confirmation does not match password!" in error_text

        print("✅ TEST PASSED: Validasi password confirmation berhasil")
        driver.execute_script("lambda-status=passed")

    except Exception as e:
        print("❌ TEST FAILED:", e)
        driver.execute_script("lambda-status=failed")

    finally:
        driver.quit()
        print("🧹 Sesi pengujian ditutup")


if __name__ == "__main__":
    run_tc010_password_confirmation_test()
