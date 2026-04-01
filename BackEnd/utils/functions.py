from fastapi import UploadFile
import shutil
import os

UPLOAD_DIR = "FrontEnd/static/uploads"

def salvar_imagem(file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    caminho = f"{UPLOAD_DIR}/{file.filename}"

    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return caminho





import bcrypt

def gerar_hash(senha: str):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def verificar_senha(senha: str, hash: str):
    return bcrypt.checkpw(senha.encode(), hash.encode())

