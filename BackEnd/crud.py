


import uuid
from db import SessionLocal
from models import Usuario,Denuncia,Imagem,Post
from utils.functions import salvar_imagem,gerar_hash,verificar_senha

from sqlalchemy.orm import Session

# teste de inserção esse funciona
def criar_usuario(nome, email, password):
    try:
        db = SessionLocal()
        novo = Usuario(
            nome=nome,
            email=email,
            senha_hash=gerar_hash(password)
        )
        db.add(novo)
        db.commit()
        db.close()
        print("\n SUCESSO!")
    except Exception as e:
        print("Erro ao criar usuário:", e)
        return e

def criar_denuncia(db, descricao, imagens, localizacao, data_ocorrencia):
    try:
     
        nova: Denuncia = Denuncia(
            descricao=descricao,
            localizacao=localizacao,
            data_ocorrencia=data_ocorrencia,
        
        )
        print(nova)
        db.add(nova)
        db.commit()
        db.refresh(nova)


        for img in imagens:
            caminho = salvar_imagem(img)

            imagem = Imagem(
                caminho=caminho,
                denuncia_id=nova.id
            )

            db.add(imagem)

        db.commit()
        db.close()
        return {"msg": "Sucess!"}
    except Exception as e:
        print("Erro", e)
        return {"msg": "Error!", "data": str(e)}

def get_denuncias(db):
    try:
        denuncias = db.query(Denuncia).all()

        resultado = []

        for d in denuncias:
            resultado.append({
                "id": d.id,
                "descricao": d.descricao,
                "localizacao": d.localizacao,
                "data_ocorrencia": str(d.data_ocorrencia),
                "imagens": [    
                    {"caminho": img.caminho}
                    for img in d.imagens
                ],
                "status": d.status
            })

        db.close()
        return resultado
    except Exception as e:
        print("Erro ao listar denúncias:", e)
        return {"msg": "Erro ao listar denúncias!", "data": str(e)}

def excluir_denuncia(db, id_denuncia):
    try:
        print("ID recebido:", id_denuncia)  # 👈 DEBUG
        denuncia = db.query(Denuncia).filter(Denuncia.id == uuid.UUID(id_denuncia)).first()
    
        if not denuncia:
            return {"msg": "Denuncia não encontrado!"}

        db.delete(denuncia)
        db.commit()
        db.close()
        return {"msg": "Denuncia excluído com sucesso!"}
    except Exception as e:
        print("Erro ao excluir post:", e)
        return {"msg": "Erro ao excluir Denuncia!", "data": str(e)}


def atualizar_denuncia(db, id_denuncia, status):
    try:
        print("ID recebido:", id_denuncia)  # 👈 DEBUG
        denuncia = db.query(Post).filter(Post.id == uuid.UUID(id_denuncia)).first()
    
        if not denuncia:
            return {"msg": "Denuncia não encontrado!"}

        if not status:
            return
        
        denuncia.status = status
        db.commit()
        db.refresh(denuncia)
        return {"msg": "Status da Denuncia atualizada com sucesso!"}
    except Exception as e:
        print("Erro:", e)
        return {"msg": "Erro", "data": str(e)}




from datetime import datetime
def criar_post(db, titulo, conteudo, video_url):
    try:
        novo = Post(
            titulo=titulo,
            conteudo=conteudo,
            video_url=video_url,
            data_publicacao=datetime.now()
        )
        db.add(novo)
        db.commit()
        db.close()
        return {"msg": "Post criado com sucesso!"}
    except Exception as e:
        print("Erro ao criar post:", e)
        return {"msg": "Erro ao criar post!", "data": str(e)}
def editar_post(db, id_post, novo_titulo, novo_conteudo, novo_video_url):
    try:
        post = db.query(Post).filter(Post.id == uuid.UUID(id_post)).first()
 

        if not post:
            return {"msg": "Post não encontrado!"}

        # 🔥 só atualiza se tiver valor
        if novo_titulo:
            post.titulo = novo_titulo

        if novo_conteudo:
            post.conteudo = novo_conteudo

        if novo_video_url:
            post.video_url = novo_video_url

        db.commit()
        db.refresh(post)

        return {"msg": "Post editado com sucesso!"}

    except Exception as e:
        print("Erro ao editar post:", e)
        return {"msg": "Erro ao editar post!", "data": str(e)}
    
def excluir_post(db, id_post):
    try:
        print("ID recebido:", id_post)  # 👈 DEBUG
        post = db.query(Post).filter(Post.id == uuid.UUID(id_post)).first()
    
        if not post:
            return {"msg": "Post não encontrado!"}

        db.delete(post)
        db.commit()
        db.close()
        return {"msg": "Post excluído com sucesso!"}
    except Exception as e:
        print("Erro ao excluir post:", e)
        return {"msg": "Erro ao excluir post!", "data": str(e)}


def autenticar_usuario(db, email, senha):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return None

    if not verificar_senha(senha, usuario.senha_hash):
        return None


    return usuario


def get_posts(db):
    try:
        post = db.query(Post).all()

        resultado = []

        for p in post:
            resultado.append({
                "id": p.id,
                "titulo": p.titulo,
                "conteudo": p.conteudo,
                "video_url": p.video_url,
                "data_publicacao": str(p.data_publicacao)
            })
    
            db.close()
        return resultado
    except Exception as e:
        print("Erro ao listar Posts:", e)
        return {"msg": "Erro ao listar Posts!", "data": str(e)}

if __name__ == "__main__":
    criar_usuario(nome="ADMIN", email="ADMIN@gmail.com", password="123456")