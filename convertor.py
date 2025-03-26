import this

import fitz


class Convertor:
	file_path = ""
	output_folder = ""
	config = ""
	size_multiplier = 1
	rotation = 0

	def __init__(self):
		pass

	def getPageCount(self):
		with fitz.open(self.file_path) as pdfDoc:
			return len(pdfDoc)

	def decode_config(self, string, n):
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

	def pdfToImg(self):
		array = self.decode_config(self.config, self.getPageCount())
		pdfDoc = fitz.open(self.file_path)
		count = 1
		zoom_x = self.size_multiplier
		zoom_y = self.size_multiplier
		mat = fitz.Matrix(zoom_x, zoom_y)
		mat = mat.prerotate(self.rotation)
		for page in pdfDoc.pages():
			if array[count] == 1:
				pix = page.get_pixmap(matrix=mat, dpi=None, colorspace='rgb', alpha=False)
				target_img_name = self.output_folder + '/' + str(count) + '.png'
				pix.save(target_img_name)
			count += 1
