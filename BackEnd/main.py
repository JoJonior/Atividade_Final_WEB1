from datetime import date
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from fastapi import Depends
from db import Base, engine,SessionLocal,get_db
from sqlalchemy.orm import Session

from starlette.middleware.sessions import SessionMiddleware


from crud import criar_denuncia, criar_post, criar_usuario, editar_post, excluir_post, get_denuncias, autenticar_usuario, get_posts

import uvicorn

app = FastAPI()




templates = Jinja2Templates(directory="FrontEnd/")

app.mount("/static", StaticFiles(directory="FrontEnd/static"), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key="secret_key"

)

#region Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    name="index.html",
    request=request,
    context={}
)

@app.get("/mapa_coleta", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    name="mapacoleta.html",
    request=request,
    context={}
)

@app.get("/fazer_denuncia", response_class=HTMLResponse)
async def form_denuncia(request: Request, sucesso: int = 0):
    return templates.TemplateResponse(
    name="formulario_denuncia.html",
    request=request,
    context={"sucesso": sucesso}
)



@app.post("/fazer_denuncia")
async def enviar_denuncia(
    local: str = Form(...),
    data: date = Form(None),
    descricao: str = Form(...),
    imagens: list[UploadFile] = File([]),
    db: Session = Depends(get_db)
    
):
    nova = criar_denuncia(db,descricao, imagens, local, data)

    #return {"msg": f"{nova} criada com sucesso!"}
    return RedirectResponse("/fazer_denuncia?sucesso=1", status_code=303)




@app.get("/posts_educativos", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    name="posts_educativos.html",
    request=request,
    context={}
)



@app.get("/api/denuncias")
def listar_denuncias(
    db: Session = Depends(get_db),
    
):
    return get_denuncias(db)


# REQQUEST LOGIN

@app.get("/ADMIN/denuncias")
def listar_denuncias(
    request: Request,
):
    user = usuario_logado(request)
    if not user:
        return RedirectResponse("/ADMIN/login", status_code=303)

    #return get_denuncias(db)
    return templates.TemplateResponse(
    name="ver_denuncias.html",
    request=request,
    context={}
)


@app.get("/ADMIN/login")
def listar_denuncias(
    request: Request,
    erro: int = 0,
    msg = "Email ou senha incorretos!"
):
    
    return templates.TemplateResponse(
    name="admin_login.html",
    request=request,
    context={"erro": erro, "msg": msg}
)

@app.get("/ADMIN")
def redirect_to_login(request: Request):
    user = usuario_logado(request)
    if not user:
        return RedirectResponse("/ADMIN/login", status_code=303)
    
    return RedirectResponse("/ADMIN/denuncias", status_code=303)

@app.post("/ADMIN/login")
def admin_login(
    request: Request,
    db: Session = Depends(get_db),
    
    email: str = Form(...),

    senha: str = Form(...),
    
):
    try:
        usuario = autenticar_usuario(db,email, senha)
        print(usuario) # SEMPRE DA NONE
    except Exception as e:
        print(e)
        #return RedirectResponse(f"/ADMIN/login?erro=1&msg={e}", status_code=303)

    if not usuario:
        return RedirectResponse(f"/ADMIN/login?erro=1&msg=Email ou senha incorretos!", status_code=303)

    request.session["user_id"] = str(usuario.id)
    return RedirectResponse("/ADMIN/denuncias", status_code=303)

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/ADMIN/login", status_code=303)


@app.get("/ADMIN/Posts", response_class=HTMLResponse)
async def home(request: Request):

    user = usuario_logado(request)
    if not user:
        return RedirectResponse("/ADMIN/login", status_code=303)

    return templates.TemplateResponse(
    name="admin_posts.html",
    request=request,
    context={}
)


@app.get("/api/posts")
def listar_posts(
    db: Session = Depends(get_db),
    
):
    return get_posts(db)

@app.post("/api/posts")
def criar_posts(
    titulo: str = Form(...),
    conteudo: str = Form(...),
    video_url: str = Form(...),
    
    db: Session = Depends(get_db)
    
):
    return criar_post(db, titulo, conteudo, video_url)  


@app.put("/api/posts/{post_id}")
def editar_posts(
    post_id: str,
    titulo: str = Form(...),
    conteudo: str = Form(...),
    video_url: str = Form(...),
    db: Session = Depends(get_db)
):
    return editar_post(db, post_id, titulo, conteudo, video_url)


@app.delete("/api/posts/{post_id}")
def deletar_posts(
    post_id: str,
    db: Session = Depends(get_db)
):
    return excluir_post(db, post_id)

#endregion

from fastapi.responses import RedirectResponse

def usuario_logado(request: Request):
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    return user_id

if __name__ == "__main__":
    
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    