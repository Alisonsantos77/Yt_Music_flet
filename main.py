# main.py
from loguru import logger
import flet as ft
from routes import setup_routes

# Configuração básica do Loguru
logger.add("app.log", format="{time} {level} {message}", level="INFO", rotation="1 MB", compression="zip")


def main(page: ft.Page):
    logger.info("Aplicação iniciada")
    page.title = "Painel Alison dev"
    setup_routes(page)
    page.update()


if __name__ == "__main__":
    logger.info("Inicializando a aplicação")
    ft.app(target=main, assets_dir='assets')
