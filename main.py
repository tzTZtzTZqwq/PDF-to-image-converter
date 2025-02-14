import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import fitz

file_path = ""
output_folder = ""
config = ""
size_multiplier = 1
rotation = 0


def pdfToImg(pdf_path, img_path):
	array = decode_config(config, getPageCount(pdf_path))
	pdfDoc = fitz.open(pdf_path)
	count = 1
	zoom_x = size_multiplier
	zoom_y = size_multiplier
	mat = fitz.Matrix(zoom_x, zoom_y)
	mat = mat.prerotate(rotation)
	for page in pdfDoc.pages():
		if (array[count] == 1):
			pix = page.get_pixmap(matrix=mat, dpi=None, colorspace='rgb', alpha=False)
			target_img_name = img_path + '/' + str(count) + '.png'
			pix.save(target_img_name)
		count += 1


def getPageCount(pdf_path):
	count = 0
	pdfDoc = fitz.open(pdf_path)
	for page in pdfDoc.pages():
		count += 1
	return count


def update_status():
	if file_path:
		status_file_label.config(text="✔", fg="green")
	else:
		status_file_label.config(text="✖", fg="red")

	if output_folder:
		status_folder_label.config(text="✔", fg="green")
	else:
		status_folder_label.config(text="✖", fg="red")

	if entry.get().strip():
		status_input_label.config(text="✔", fg="green")
	else:
		status_input_label.config(text="✖", fg="red")


def select_file():
	global file_path
	file_path = filedialog.askopenfilename()
	if file_path:
		file_label.config(text=f"file: {os.path.basename(file_path)}")
	pageCount = getPageCount(file_path)
	entry.delete(0, tk.END)
	entry.insert(0, "1-" + str(pageCount))
	pages_label.config(text=f"this file has " + str(pageCount) + " pages.")
	update_config()
	update_status()


def select_output_folder():
	global output_folder
	output_folder = filedialog.askdirectory()
	if output_folder:
		output_label.config(text=f"output folder: {output_folder}")
	update_status()


def open_file():
	if file_path:
		try:
			if os.name == "nt":
				os.startfile(file_path)
			else:
				subprocess.run(["open", file_path])
		except Exception as e:
			messagebox.showerror("error", f"can not open file: {e}")
	else:
		messagebox.showwarning("error", "please select a file first")


def open_output_folder():
	if output_folder:
		try:
			subprocess.run(["open", output_folder])
		except Exception as e:
			messagebox.showerror("error", f"can not open output folder: {e}")
	else:
		messagebox.showwarning("error", "please select a output folder first")


def create_output_folder():
	global output_folder
	current_directory = os.path.dirname(os.path.abspath(__file__))
	temp_folder_path = os.path.join(current_directory, "temp")
	if os.path.exists(temp_folder_path):
		for filename in os.listdir(temp_folder_path):
			temp_file_path = os.path.join(temp_folder_path, filename)
			if os.path.isdir(temp_file_path):
				os.rmdir(temp_file_path)
			else:
				os.remove(temp_file_path)
		os.rmdir(temp_folder_path)
	os.makedirs(temp_folder_path)
	output_folder = os.path.abspath(temp_folder_path)
	output_label.config(text=f"output folder: {output_folder}")
	update_status()


def confirm_action():
	user_input = entry.get()
	print(f"confirmed : {user_input}")
	process_label.config(text=f"processing...")
	pdfToImg(file_path, output_folder)
	process_label.config(text=f"done")
	update_status()
	open_output_folder()


def size_slider_onChange(value):
	global size_multiplier
	size_multiplier = value


def rotate_slider_onChange(value):
	global rotation
	rotation = value


def decode_config(string, n):
	result = [0] * (n + 1)
	blocks = string.split(',')
	print(string)
	print(blocks)
	for block in blocks:
		print(string)
		if '-' in block:
			a, b = map(int, block.split('-'))
			for i in range(a, b + 1):
				result[i] = 1
		else:
			c = int(block)
			result[c] = 1
	return result


def update_config():
	global config
	config = entry.get()
	update_status()


root = tk.Tk()
root.title("converter")
root.geometry("500x600")

frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=10, pady=5)

step1 = tk.Label(frame_top, text="STEP1: SELECT A PDF FILE", font=("Arial", 12))
step2 = tk.Label(frame_top, text="STEP2: SELECT ONE BETWEEN", font=("Arial", 12))

file_label = tk.Label(frame_top, text="select a PDF file first", font=("Arial", 12), anchor="w")
status_file_label = tk.Label(frame_top, text="✖", font=("Arial", 12), fg="red")
output_label = tk.Label(frame_top, text="select a output folder first", font=("Arial", 12), anchor="w")
status_folder_label = tk.Label(frame_top, text="✖", font=("Arial", 12), fg="red")
btn_select_file = tk.Button(frame_top, text="select PDF file", command=select_file)
btn_select_folder = tk.Button(frame_top, text="select output folder", command=select_output_folder)
or_label = tk.Label(frame_top, text="OR", font=("Arial", 12), anchor="w")
btn_create_folder = tk.Button(frame_top, text="create a temporary output folder(recommended)",
							  command=create_output_folder)
btn_open_file = tk.Button(frame_top, text="open selected file", command=open_file)
btn_open_folder = tk.Button(frame_top, text="open output folder", command=open_output_folder)

file_label.grid(row=0, column=0, sticky="w")
status_file_label.grid(row=0, column=1, sticky="e")
output_label.grid(row=1, column=0, sticky="w")
status_folder_label.grid(row=1, column=1, sticky="e")
step1.grid(row=2, column=0, sticky="w")
btn_select_file.grid(row=3, column=0, sticky="w")
btn_open_file.grid(row=4, column=0, sticky="w")
step2.grid(row=5, column=0, sticky="w")
btn_create_folder.grid(row=6, column=0, sticky="w")
or_label.grid(row=7, column=0, sticky="w")
btn_select_folder.grid(row=8, column=0, sticky="w")
btn_open_folder.grid(row=9, column=0, sticky="w")

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=10, pady=5)

frame_middle = tk.Frame(root)
frame_middle.pack(fill="x", padx=10, pady=5)
step3 = tk.Label(frame_middle, text="STEP3: EDIT SETTINGS", font=("Arial", 12))
input_label = tk.Label(frame_middle, text="enter pages you want to convert e.g.1-4,6,9-11 will save 8 pages in total :",
					   font=("Arial", 12), anchor="w")
pages_label = tk.Label(frame_middle, text="select a PDF file first", font=("Arial", 12), anchor="w")
status_input_label = tk.Label(frame_middle, text="✖", font=("Arial", 12), fg="red")
step3.grid(row=0, column=0, sticky="w")
input_label.grid(row=1, column=0, sticky="w")
pages_label.grid(row=2, column=0, sticky="w")
status_input_label.grid(row=0, column=1, sticky="e")
entry = tk.Entry(frame_middle, font=("Arial", 12))
entry.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)
entry.bind("<KeyRelease>", lambda event: update_config())

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=10, pady=5)

frame_settings = tk.Frame(root)
frame_settings.pack(fill="x", padx=10, pady=5)
rotate_label = tk.Label(frame_settings, text="rotation of every image", font=("Arial", 12), anchor="w")
size_label = tk.Label(frame_settings, text="size multiplier. Higher size multiplier makes image clearer and larger",
					  font=("Arial", 12), anchor="w")
rotate_slider = tk.Scale(frame_settings, from_=0, to=360, orient="horizontal", resolution=90,
						 command=rotate_slider_onChange)
size_slider = tk.Scale(frame_settings, from_=0.2, to=4, orient="horizontal", resolution=0.1,
					   command=size_slider_onChange)
rotate_label.grid(row=0, column=0, sticky="w")
rotate_slider.grid(row=1, column=0, sticky="w")
size_label.grid(row=2, column=0, sticky="w")
size_slider.grid(row=3, column=0, sticky="w")
rotate_slider.set(0)
size_slider.set(2)

ttk.Separator(root, orient="horizontal").pack(fill="x", padx=10, pady=5)

frame_bottom = tk.Frame(root)
frame_bottom.pack(fill="x", padx=10, pady=10)
process_label = tk.Label(frame_bottom, text="", font=("Arial", 12), anchor="w")
confirm_button = tk.Button(frame_bottom, text="confirm", command=confirm_action)
process_label.grid(row=0, column=0, sticky="w")
confirm_button.grid(row=1, column=0, sticky="w")

root.mainloop()
