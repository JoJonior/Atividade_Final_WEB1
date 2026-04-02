import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Configuração do Ambiente e Banco
load_dotenv()
# Se DATABASE_URL não existir no .env, ele criará um sqlite local por padrão
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Definição do Modelo (conforme sua estrutura)
class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String)
    conteudo = Column(String)
    video_url = Column(String)
    data_publicacao = Column(DateTime, default=datetime.utcnow)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# 3. Dados dos Posts (Baseados nos vídeos analisados)
posts_data = [
    {
        "titulo": "Lixo Eletrônico: O Perigo Invisível",
        "conteudo": "Pilhas e eletrônicos possuem metais pesados que poluem solo e água. Use a Logística Reversa para descartar corretamente.",
        "video_url": "52pfRQawboA"
    },
    {
        "titulo": "Resíduos vs. Lixo: Você sabe a diferença?",
        "conteudo": "A maioria do que jogamos fora são resíduos com valor (recicláveis ou orgânicos). Lixo é apenas o que não pode ser reaproveitado.",
        "video_url": "MiuIckYJfQY"
    },
    {
        "titulo": "O Guia do Descarte de Pilhas",
        "conteudo": "Nunca jogue pilhas no lixo comum. Embale em plástico resistente para evitar umidade e leve a um ponto de coleta especializado.",
        "video_url": "Gqk161ll21s"
    },
    {
        "titulo": "Checklist do Descarte Doméstico",
        "conteudo": "Dicas práticas: proteja vidros quebrados em caixas, armazene óleo em garrafas PET e nunca descarte remédios no esgoto.",
        "video_url": "0hAGXUFg3Z4"
    }
]

# 4. Função para inserir os dados
def populate_database():
    db = SessionLocal()
    try:
        for data in posts_data:
            # Verifica se o post já existe pelo título para evitar duplicatas
            exists = db.query(Post).filter(Post.titulo == data["titulo"]).first()
            if not exists:
                novo_post = Post(
                    id=uuid.uuid4(),
                    titulo=data["titulo"],
                    conteudo=data["conteudo"],
                    video_url=data["video_url"],
                    data_publicacao=datetime.now()
                )
                db.add(novo_post)
        
        db.commit()
        print("✅ Banco de dados populado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao popular banco: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()