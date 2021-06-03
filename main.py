import os
import threading
import time
import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait


def cek_saldo():
    global driver
    text_box.config(state=tk.NORMAL)
    text_box.delete(0, 'end')
    text_box.insert(tk.INSERT, "bentar ya")
    text_box.config(state=tk.DISABLED)
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome("D:\\PENTING\\SOFTWARE\\Program mbuat sendiri\\chromedriver.exe",
                                  options=chrome_options)
        driver.get("https://ibank.klikbca.com/")
        driver.find_element_by_name("value(user_id)").send_keys("ALANRIZK0408")
        driver.find_element_by_name("value(pswd)").send_keys("759123")
        driver.find_element_by_name("value(Submit)").click()
        time.sleep(0.5)
        wait(driver, 11).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "menu")))
        time.sleep(0.3)
        wait(driver, 11).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/table/tbody/tr/td[2]/table/tbody/tr[17]/td/a/font/b"))).click()
        driver.switch_to.default_content()
        time.sleep(0.3)
        wait(driver, 11).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "menu")))
        time.sleep(0.3)
        wait(driver, 11).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table/tbody/tr[1]/td[2]/font/a"))).click()
        time.sleep(0.3)
        driver.switch_to.default_content()
        wait(driver, 11).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "atm")))
        saldo = wait(driver, 11).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table[3]/tbody/tr[2]/td[4]/div/font"))).text
        line = saldo.replace(',', '.')
        text_box.config(state=tk.NORMAL)
        text_box.delete(0, 'end')
        text_box.insert(tk.INSERT, line[:-3])
        text_box.config(state=tk.DISABLED)
        driver.switch_to.default_content()
        wait(driver, 11).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "header")))
        wait(driver, 11).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/font/b/a"))).click()
        driver.close()
        os.system("taskkill /F /IM chromedriver.exe")
        if btn_cek['state'] == tk.DISABLED:
            btn_cek['state'] = tk.NORMAL
        if btn_quit['state'] == tk.DISABLED:
            btn_quit['state'] = tk.NORMAL

    except:
        driver.close()
        text_box.config(state=tk.NORMAL)
        text_box.delete(0, 'end')
        text_box.config(state=tk.DISABLED)
        tk.Label(root, text="Sabar", font=('Times New Roman', 15)).place(relx=0.4,
                                                                         rely=0.59)
        time.sleep(3)
        tk.Label(root, text="         ", font=('Times New Roman', 15)).place(relx=0.4,
                                                                             rely=0.59)
        if btn_cek['state'] == tk.DISABLED:
            btn_cek['state'] = tk.NORMAL
        if btn_quit['state'] == tk.DISABLED:
            btn_quit['state'] = tk.NORMAL
        os.system("taskkill /F /IM chromedriver.exe")


def start_submit_thread():
    global submit_thread
    progressbar.place(relx=0.04, rely=0.415)
    if btn_cek['state'] == tk.NORMAL:
        btn_cek['state'] = tk.DISABLED
    if btn_quit['state'] == tk.NORMAL:
        btn_quit['state'] = tk.DISABLED
    submit_thread = threading.Thread(target=cek_saldo)
    submit_thread.daemon = True
    progressbar.start(5)
    submit_thread.start()
    root.after(1, check_submit_thread)


def check_submit_thread():
    if submit_thread.is_alive():
        root.after(1, check_submit_thread)
    else:
        progressbar.stop()
        progressbar.place_forget()


root = tk.Tk()
root.geometry("300x125+800+480")
root.overrideredirect(1)
tk.Label(root, text="Saldo Rp. ", font=('Times New Roman', 15)).place(relx=0,
                                                                      rely=0.13)
progressbar = ttk.Progressbar(root, mode='indeterminate', length=278, value=0, maximum=100)

tk.Label(root, font="times 20")
text_box = tk.Entry(root, width=16, font="times 14")
text_box.config(state=tk.DISABLED)
text_box.place(relx=0.36, rely=0.14)
btn_cek = tk.Button(root, text="Cek", command=lambda: start_submit_thread(), width=10)
btn_cek.pack(side=tk.LEFT, padx=15, pady=(60, 0))
btn_quit = tk.Button(root, text="Keluar", command=root.destroy, width=10)
btn_quit.pack(side=tk.RIGHT, padx=15, pady=(60, 0))
root.wm_attributes("-topmost", 1)

root.mainloop()
