from collections import namedtuple

# Locations IFE C Type
OCRLocation = namedtuple("OCRLocation", ["id", "bbox",
	"filter_keywords"])
OCR_LOCATIONS_IFEC = [
	OCRLocation("Nombre", (35, 125, 180, 85),
		["NOMBRE"]),
	OCRLocation("Domicilio", (35, 207, 220, 88),
		["DOMICILIO"]),
	OCRLocation("Clave de elector", (35, 313, 330, 25),
		["clave"]),
	OCRLocation("CURP", (35, 333, 270, 25),
		["CURP"]),
	OCRLocation("Año de registro", (220, 295, 230, 25),
		["año"]),
	OCRLocation("Edad", (375, 147, 80, 25),
		["EDAD"]),
]

# Locations IFE D Type
OCR_LOCATIONS_IFED = [
OCRLocation("Nombre", (205, 110, 205, 90),
  ["NOMBRE"]),
OCRLocation("Domicilio", (205, 198, 340, 97),
  ["DOMICILIO","OOMICIUO","DOMICIUO", "CLAVE", "ELECTOR", "REGISTRO", "REGISTR", "CRAVE", "LECTOR", "DOMICHUO"]),
OCRLocation("Clave de elector", (205, 290, 340, 27),
  ["clave"]),
OCRLocation("CURP", (205, 315, 255, 30),
  ["CURP"]),
OCRLocation("Año de registro", (475, 317, 198, 30),
  ["año"]),
OCRLocation("Fecha de nacimiento", (535, 110, 155, 50),
  ["FECHA", "DE", "NACIMIENTO"]),
]


# Locations INE EF Type
OCR_LOCATIONS_INEEF = [
OCRLocation("Nombre", (205, 115, 205, 90),
  ["NOMBRE"]),
OCRLocation("Domicilio", (205, 203, 340, 97),
  ["DOMICILIO","OOMICIUO","DOMICIUO", "CLAVE", "ELECTOR", "REGISTRO", "REGISTR", "CRAVE", "LECTOR", "DOMICHUO"]),
OCRLocation("Clave de elector", (205, 297, 340, 27),
  ["clave"]),
OCRLocation("CURP", (205, 322, 255, 30),
  ["CURP"]),
OCRLocation("Año de registro", (483, 325, 198, 30),
  ["año"]),
OCRLocation("Fecha de nacimiento", (540, 115, 150, 50),
  ["FECHA", "DE", "NACIMIENTO"]),
]

# Locations INE GH Type
OCR_LOCATIONS_INEGH = [
OCRLocation("Nombre", (230, 125, 205, 90),
  ["NOMBRE"]),
OCRLocation("Domicilio", (230, 225, 320, 85),
  ["DOMICILIO","OOMICIUO","DOMICIUO", "CLAVE", "ELECTOR", "REGISTRO", "REGISTR", "CRAVE", "LECTOR", "DOMICHUO"]),
OCRLocation("Clave de elector", (230, 310, 340, 25),
  ["clave"]),
OCRLocation("CURP", (230, 333, 200, 45),
  ["CURP"]),
OCRLocation("Año de registro", (490, 333, 140, 45),
  ["año"]),
OCRLocation("Fecha de nacimiento", (230, 375, 170, 45),
  ["FECHA", "DE", "NACIMIENTO"]),
]
