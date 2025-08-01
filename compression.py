import zlib
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox

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
        with open(compressed_file, 'wb') as f:
            f.write(compressed_data)
        end_time = time.time()


        original_size = os.path.getsize(file_path)
        compressed_size = os.path.getsize(compressed_file)
        percent_saved = (compressed_size/original_size)*100
        
        result = f"""
 Your File has Successfully been Compressed!

 File Name: {os.path.basename(file_path)}
 Original Size(in bytes): {original_size} bytes
 Compressed Size(in bytes): {compressed_size} bytes
 Space Saved(in %): {percent_saved:.2f} %
 Time(in seconds): {end_time - start_time:.3f} seconds

 Saved to: {compressed_file} """
        messagebox.showinfo("Compression Complete", result)

    except Exception as e:
        messagebox.showerror("Compression Error", str(e))


def decompress_file():
    file_path = filedialog.askopenfilename(title="Select .zlib File to Decompress", filetypes=[("ZLIB Files", "*.zlib")])
    if not file_path:
        return

    try:
        folder = os.path.dirname(file_path)
        decompressed_file = os.path.join(folder, "decompressed_file.txt")

        start_time = time.time()
        with open(file_path, 'rb') as f:
            compressed_data = f.read()

        decompressed_data = zlib.decompress(compressed_data)
        with open(decompressed_file, 'wb') as f:
            f.write(decompressed_data)
        end_time = time.time()

        decompressed_size = os.path.getsize(decompressed_file)

        result = f"""
  Your File has Successfully been Decompressed!

 Decompressed Size(in bytes): {decompressed_size} bytes
 Time(in seconds): {end_time - start_time:.3f} seconds

 Saved to: {decompressed_file} """
        messagebox.showinfo("Decompression Complete", result)

    except Exception as e:
        messagebox.showerror("Decompression Error", str(e))
        
#GUI for the tool
window=tk.Tk()
window.title("Compress and Decompress your Files here")
window.geometry("480x350")

h1=tk.Label(window,text="Select File to Compress and Decompress",font=("Times New Roman",12))
h1.pack(pady=15)

h2=tk.Label(window,text="Code Crafter 2.0",font=("Times New Roman",10))
h2.pack(pady=15)

b1=tk.Button(window,text="Compress + Encrypt your File here",font=("Times New Roman",12),width=25,fg="Black",bg="light blue", command=compress_file)
b1.pack(pady=15)

b2=tk.Button(window,text="Decompress + Decrypt your File here",font=("Times New Roman",12),width=25,fg="Black",bg="light green", command=decompress_file)
b2.pack(pady=15)

window.mainloop()
