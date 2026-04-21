from src.backend.database import inicializar_banco


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso em data/diariooficial.db")