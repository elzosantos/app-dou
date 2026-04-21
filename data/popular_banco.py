from src.backend.database import inserir_noticias

# Lista de 20 notícias fictícias
noticias_ficticias = [
    ("Startup de IA levanta 2M de investimento em Brasília", "2026-04-20", "DF", 1),
    ("Nova incubadora de empresas abre inscrições em São Paulo", "2026-05-15", "SP", 1),
    ("Tecnologia de blockchain revolucionando logística em SC", "2026-06-02", "SC", 1),
    ("Evento de empreendedorismo feminino reúne 500 líderes", "2026-07-10", "MG", 1),
    ("Governo lança edital de incentivo a fintechs", "2026-08-22", "RJ", 1),
    ("Workshop de IA aplicada para pequenas empresas", "2026-09-05", "BA", 1),
    ("Plataforma de e-commerce cresce 30% no setor de moda", "2026-10-12", "RS", 1),
    ("Hub de inovação é inaugurado em Manaus", "2026-11-01", "AM", 1),
    ("Startup de energia solar expande operações no Nordeste", "2026-12-05", "PE", 1),
    ("Programa de aceleração para agritechs aberto", "2027-01-15", "MT", 1),
    ("Projeto de gestão de resíduos recebe prêmio de inovação", "2027-02-20", "PR", 1),
    ("Edtech lança curso focado em governança de dados", "2027-03-10", "GO", 1),
    ("Iniciativa de apoio a empreendedores negros ganha força", "2027-04-05", "ES", 1),
    ("Startup de telemedicina atinge 1 milhão de usuários", "2027-05-12", "CE", 1),
    ("Feira de negócios locais movimenta economia no Pará", "2027-06-18", "PA", 1),
    ("Empresa de cibersegurança abre filial em Curitiba", "2027-07-25", "PR", 1),
    ("App de entregas ecológicas chega ao Mato Grosso do Sul", "2027-08-30", "MS", 1),
    ("Centro de inovação em biotecnologia é anunciado", "2027-09-14", "RN", 1),
    ("Incentivo fiscal para startups no setor hoteleiro", "2027-10-02", "AL", 1),
    ("Conferência de tendências para o varejo 2028", "2027-11-20", "SP", 1)
]

if __name__ == "__main__":
    count = inserir_noticias(noticias_ficticias)
    print(f"{count} notícias inseridas com sucesso!")