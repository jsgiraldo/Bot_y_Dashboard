# --------------------------------------------------------------------------
# BOT DE DESCARGA DE DATOS v1.5 (con Playwright - El Preciso)
# OBJETIVO: Descargar datos de energía.
# MEJORA: Se añade el parámetro `exact=True` al localizador final para
#         resolver la ambigüedad entre "CSV para Excel" y
#         "CSV para Excel (Europa)", completando la misión.
# --------------------------------------------------------------------------

import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

def descargar_con_playwright():
    """
    Función principal que orquesta la descarga usando Playwright.
    """
    
    with sync_playwright() as p:
        print(">>> [FASE 1/3] Iniciando el bot Preciso...")
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        page.set_default_timeout(60000) 
        
        URL_DATOS = "https://www.datos.gov.co/Minas-y-Energ-a/Tarifas-y-Costos-de-Energ-a-El-ctrica-para-el-Merc/ytme-6qnu/about_data"

        try:
            print(f">>> [FASE 2/3] Navegando y ejecutando la secuencia final...")
            page.goto(URL_DATOS)
            
            print("...Haciendo clic en 'Exportar'.")
            page.get_by_role("button", name="Exportar").click()

            dialog = page.locator("forge-dialog")
            
            print("...Esperando que el diálogo de exportación esté listo.")
            dialog.get_by_role("button", name="Cancelar").wait_for(state="visible")
            print("...Diálogo confirmado y listo.")

            print("...Abriendo el menú desplegable de formatos.")
            dialog.get_by_label("Exportar formato").click()

            # ----- LA CORRECCIÓN FINAL Y PRECISA -----
            # Añadimos `exact=True` para diferenciar las dos opciones.
            print("...Seleccionando la opción EXACTA 'CSV para Excel'.")
            page.get_by_role("option", name="CSV para Excel", exact=True).click()
            
            print(">>> [FASE 3/3] Iniciando la descarga...")
            
            with page.expect_download() as download_info:
                print("...Realizando el clic final.")
                dialog.locator("button[data-testid='export-download-button']").click()
            
            download = download_info.value
            
            download_dir = "datos_descargados_energia_playwright"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            destination_path = os.path.join(download_dir, download.suggested_filename)
            download.save_as(destination_path)
            
            print("\n------------------------------------------------------------")
            print("¡MISIÓN CUMPLIDA! EL BOT FUNCIONA.")
            print("Has completado con éxito uno de los flujos de automatización más complejos.")
            print(f"Ruta del archivo: {destination_path}")
            print("¡FELICIDADES!")
            print("------------------------------------------------------------")

        except PlaywrightTimeoutError as e:
            print(f"\nERROR: El tiempo de espera se agotó. {e}")
            page.screenshot(path="error_playwright.png")
            print("Se guardó una captura de pantalla del error en 'error_playwright.png'")
        except Exception as e:
            print(f"\nERROR INESPERADO: {e}")
        finally:
            print(">>> Cerrando el bot.")
            browser.close()

if __name__ == '__main__':
    descargar_con_playwright()