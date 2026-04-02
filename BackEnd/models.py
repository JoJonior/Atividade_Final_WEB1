import uuid
from sqlalchemy import Column, Integer, String,UUID,DateTime,ForeignKey
from sqlalchemy.orm import relationship

from db import Base, engine,SessionLocal


# modelo (tabela)
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)   


class Denuncia(Base):
    __tablename__ = "denuncias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descricao = Column(String)
    localizacao = Column(String)
    data_ocorrencia = Column(DateTime)
    imagens = relationship("Imagem", back_populates="denuncia")
    status = Column(String, default="Pendente")  # Exemplo de campo para status da denúncia

class Imagem(Base):
    __tablename__ = "imagens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caminho = Column(String)  # salva onde está o arquivo
    denuncia_id = Column(UUID(as_uuid=True), ForeignKey("denuncias.id"))

    denuncia = relationship("Denuncia", back_populates="imagens")

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String)
    conteudo = Column(String)
    video_url = Column(String)
    data_publicacao = Column(DateTime)

    
# cria as tabelas no arquivo
Base.metadata.create_all(bind=engine)




