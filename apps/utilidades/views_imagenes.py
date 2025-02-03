import os
from PIL import Image

def redimensionarImagen(self_imagen, size):
	try:    
		if self_imagen and os.path.exists(self_imagen.path):
			# Redimensionar la imagen antes de guardarla
			with Image.open(self_imagen.path) as img:
				ancho, alto = img.size
				if ancho > alto:
					# La imagen es mas ancha que alta
					nuevo_alto = size
					nuevo_ancho = int((ancho/alto) * nuevo_alto)
					img = img.resize((nuevo_ancho, nuevo_alto))                          
				elif alto > ancho:
					# La imagen es mas alta que ancha
					nuevo_ancho = size
					nuevo_alto = int((alto/ancho) * nuevo_ancho )
					img = img.resize((nuevo_ancho, nuevo_alto))                         
				else:
					# La imagen es cuadrada
					img.thumbnail((size, size))
				img.save(self_imagen.path)
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False

def recortarImagenCuadrada(self_imagen):
	try:
		# El recorte de la imagen final
		if self_imagen and os.path.exists(self_imagen.path):
			with Image.open(self_imagen.path) as img:
				ancho, alto = img.size
				if ancho > alto:
					left = (ancho - alto) / 2
					top = 0
					right = (ancho + alto) / 2
					bottom = alto
				else:
					left = 0
					top = (alto - ancho) / 2
					right = ancho
					bottom = (alto + ancho) / 2
				img = img.crop((left, top, right, bottom))
				img.save(self_imagen.path)
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False

""" def redimensionarImagenPost(img_post, img_model, size):
	try:
		img = Image.open(img_post)
		ancho, alto = img.size        
		if ancho > alto:
			# La imagen es mas ancha que alta
			nuevo_alto = size
			nuevo_ancho = int((ancho/alto) * nuevo_alto)
			img = img.resize((nuevo_ancho, nuevo_alto))                                   
		elif alto > ancho:
			# La imagen es mas alta que ancha
			nuevo_ancho = size
			nuevo_alto = int((alto/ancho) * nuevo_ancho )
			img = img.resize((nuevo_ancho, nuevo_alto))                                  
		else:
			# La imagen es cuadrada
			img.thumbnail((size, size))
		buffer = BytesIO()
		img.save(buffer, format='JPEG')  # Puedes cambiar el formato si lo necesitas (PNG, etc.)
		buffer.seek(0)
		name = str(uuid.uuid4()) + '.jpg'        
		img_model.save(name, buffer)
  		return True  
	except Exception as e:
		print(e)
	 	return False	

def recortarImagenCuadrada(self_imagen):  
  	nuevo_ancho = 150
	nuevo_alto = 150
	if nuevo_ancho > nuevo_alto:
		left = (nuevo_ancho - nuevo_alto) / 2
		top = 0
		right = (nuevo_ancho + nuevo_alto) / 2
		bottom = nuevo_alto
	else:
		left = 0
		top = (nuevo_alto - nuevo_ancho) / 2
		right = nuevo_ancho
		bottom = (nuevo_alto + nuevo_ancho) / 2
	img = img.crop((left, top, right, bottom))                   
	buffer = BytesIO()
	img.save(buffer, format='JPEG')  # Puedes cambiar el formato si lo necesitas (PNG, etc.)
	buffer.seek(0)
	name = 'avatar_' + str(uuid.uuid4()) + '.jpg'        
	escort.imagen_perfil.save(name, buffer)     """