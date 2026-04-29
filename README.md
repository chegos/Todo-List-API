# 🚀 Todo List API

API RESTful para gerenciamento de tarefas com autenticação JWT, desenvolvida em Python com Flask.

---

## 🛠️ Tecnologias
- Python
- Flask
- SQLAlchemy
- JWT (Flask-JWT-Extended)
- SQLite

---

## ⚙️ Funcionalidades
- Registro e login de usuários
- Autenticação com token JWT
- CRUD de tarefas (To-Do)
- Paginação de resultados
- Proteção de rotas

---

## ▶️ Como rodar

```bash
git clone https://github.com/seu-usuario/todo-api.git
cd todo-api

python -m venv venv
venv\Scripts\activate

pip install flask flask_sqlalchemy flask_bcrypt flask_jwt_extended

python app.py
```

API rodando em:
```bash
http://127.0.0.1:5000
```
🔐 Autenticação

Após login, use o token no header:
```bash
Authorization: Bearer SEU_TOKEN
```
📌 Endpoints

Auth
- POST /register
- POST /login
  
Todos
- POST /todos → Criar
- GET /todos → Listar
- PUT /todos/<id> → Atualizar
- DELETE /todos/<id> → Deletar
  
🧪 Exemplo (criar tarefa)
```bash
{
  "title": "Estudar Python",
  "description": "Fazer projeto de API"
}
```
📈 Status

✅ Projeto funcional

🚧 Melhorias futuras: filtros, testes, deploy

👨‍💻 Autor

Luis Rodrigues
- https://github.com/chegos
- https://roadmap.sh/projects/todo-list-api


