import zlib
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# AES Key (16 bytes for AES-128)
KEY = get_random_bytes(16)

def compress_file():
    file_path = filedialog.askopenfilename(title="Select a File to Compress")
    if not file_path:
        return

    try:
        folder = os.path.dirname(file_path)
        compressed_file = os.path.join(folder, "compressed_file.zlib")

        with open(file_path, 'rb') as f:
            original_data = f.read()

        start_time = time.time()

        compressed_data = zlib.compress(original_data, level=9)

        file_name = os.path.basename(file_path)
        file_name_bytes = file_name.encode()
        file_name_length = len(file_name_bytes).to_bytes(2, 'big') 

        payload = file_name_length + file_name_bytes + compressed_data

        cipher = AES.new(KEY, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(payload, AES.block_size))
        encrypted_payload = cipher.iv + encrypted_data

        with open(compressed_file, 'wb') as f:
            f.write(encrypted_payload)

        end_time = time.time()

        original_size = os.path.getsize(file_path)
        compressed_size = os.path.getsize(compressed_file)
        space_compressed = (compressed_size / original_size) * 100

        result = f"""
     Your File has Successfully been Compressed and Encrypted!

    File Name : {file_name}

    Original file size(in bytes) : {original_size} bytes

    File Size after Compression(in bytes) : {compressed_size} bytes

    Percentage of file Compressed(in %) : {space_compressed:.2f}%

    Total Time Consumed(in seconds) : {end_time - start_time:.2f} seconds

    Saved to Directory : {compressed_file}"""

        messagebox.showinfo("Compression Successfully Completed", result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def decompress_file():
    file_path = filedialog.askopenfilename(title="Select .zlib File to Decompress", filetypes=[("ZLIB Files", "*.zlib")])
    if not file_path:
        return

    try:
        folder = os.path.dirname(file_path)

        start_time = time.time()

        with open(file_path, 'rb') as f:
            encrypted_payload = f.read()

        iv = encrypted_payload[:16]
        encrypted_data = encrypted_payload[16:]

        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_padded, AES.block_size)

        file_name_length = int.from_bytes(decrypted_data[:2], 'big')
        file_name = decrypted_data[2:2+file_name_length].decode()
        compressed_data = decrypted_data[2+file_name_length:]

        decompressed_data = zlib.decompress(compressed_data)

        decompressed_file = os.path.join(folder, f"Decompressed_{file_name}")
        with open(decompressed_file, 'wb') as f:
            f.write(decompressed_data)

        end_time = time.time()

        decompressed_size = os.path.getsize(decompressed_file)

        result = f"""
     Your File has Successfully been Decrypted and Decompressed!

     Decompressed File Name : decompressed_{file_name}

     File Size after Decompression(in bytes) : {decompressed_size} bytes
     
     Total Time Consumed(in seconds) : {end_time - start_time:.2f} seconds

     Saved to: {decompressed_file}
"""
        messagebox.showinfo("Decompression Successfully Completed", result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
window = tk.Tk()
window.title("Compression and Decompression tool")
window.geometry("580x350")

tk.Label(window, text="Secured Compression and Decompression tool ", font=("Times New Roman", 20)).pack(pady=15)

tk.Button(window, text="Compress and Encrypt", font=("Times New Roman", 12), width=30, bg="light blue", command=compress_file).pack(pady=10)
tk.Button(window, text="Decrypt and Decompress", font=("Times New Roman", 12), width=30, bg="light green", command=decompress_file).pack(pady=10)


window.mainloop()
