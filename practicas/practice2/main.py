import sys, requests
import utilities

urls_funciones = {
    "1": "http://localhost:8080/function/face-detect-pigo",
    "2": "http://localhost:8080/function/face-detect-opencv",
    "3": "http://localhost:8080/function/basic-face-detection",
    "4": "http://localhost:8080/function/cnn-face-detection",
    "5": "http://localhost:8080/function/sam-segmentation",
    "6": "http://localhost:8080/function/sam-segmentation-light"
}

while True:
    print("Selecciona una opción de la lista de funciones disponibles:")
    print("1. Face-detect-pigo")
    print("2. Face-detect-opencv")
    print("3. Basic-face-detection")
    print("4. CNN-face-detection")
    print("5. SAM-segmentation ")
    print("6. SAM-segmentation-light")
    print("7. Salir")

    opcion = int(input("\nIngresa el número de la opción que deseas: "))

    if opcion not in range(1, 8):
        print("Opción inválida, por favor ingresa una opción válida.\n")
        continue
    else:
        break

if opcion == 5 or opcion == 6:
    print("\n¡Advertencia! SAM-segmentation puede tardar varios minutos en procesar la imagen.\n")
if opcion == 7:
    print("¡Hasta pronto!")
    sys.exit()

image_url = input("Introduce el enlace de la imagen a procesar: ")
output_filename = input("Introduce el nombre del fichero de salida: ")

response = requests.post(urls_funciones.get(str(opcion)), data=image_url)
if response.status_code == 200:
    if opcion == 1 or opcion == 2:
        with open(output_filename, "wb") as f:
            f.write(response.content)

    elif opcion >= 3:
        success = utilities.save_image_from_base64(response.text, output_filename)
        if success:
            print("Imagen procesada correctamente.")
        else:
            print("Error al guardar la imagen.")
else:
    print("Error al procesar la imagen en el servidor. ->", response.text)
