# 08 — Authentication: OAuth2 Password Flow + JWT

## Theory

**Authentication** = "who are you?" (covered here).
**Authorization** = "are you allowed to do this?" (module 09).

### The flow

1. User registers → password is **hashed** (never stored in plain text)
   and saved.
2. User logs in with username+password → server verifies, issues a
   **JWT access token**.
3. Client stores the token, sends it on every future request:
   `Authorization: Bearer <token>`.
4. Server validates the token on protected routes, without touching the
   database or asking for a password again — the signature proves it's
   legitimate.

### Password hashing

Never store plain passwords. Use a proper hashing algorithm (Argon2 here,
via `pwdlib`):

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
hashed = password_hash.hash("mypassword")
password_hash.verify("mypassword", hashed)  # True
```

Hashing is one-way — you can verify a guess against a hash, but never
recover the original password from the hash.

### JWT (JSON Web Token)

A JWT is a signed blob of claims (data). "Signed" means: anyone can read
it, but only someone with `SECRET_KEY` could have created a *valid* one —
so the server trusts a token it can successfully verify.

```python
import jwt
from datetime import datetime, timedelta, timezone

def create_access_token(subject: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

- `sub` (subject) — who the token is about, usually the username
- `exp` (expiration) — token stops being valid after this time

### OAuth2PasswordBearer + the login endpoint

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.post("/auth/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    token = create_access_token(subject=user.username, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
```

`OAuth2PasswordRequestForm` expects form data (not JSON) with `username`
and `password` fields — this is why `python-multipart` is required, and
why `/docs`' "Authorize" button works out of the box with this endpoint.

### Protecting a route

```python
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    user = get_user_by_username(session, username)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]

@app.get("/tasks/mine")
def my_tasks(current_user: CurrentUserDep, session: SessionDep):
    ...
```

Any route that takes `current_user: CurrentUserDep` is now protected —
FastAPI runs the whole chain (extract token → decode → look up user)
before your function body executes, and rejects with `401` automatically
if any step fails.

## Task

Open `starter.py`. It carries over the `Task` model from module 07 and
adds `User`.

1. `User(SQLModel, table=True)`: `id`, `username` (unique), `email`
   (unique), `hashed_password: str`, `is_active: bool = True`.
2. `hash_password` / `verify_password` using `pwdlib`.
3. `POST /auth/register` → `UserCreate` in, `UserRead` out (no password
   field in the response!). 409 if username/email taken.
4. `create_access_token(subject, expires_delta)`.
5. `POST /auth/login` → `OAuth2PasswordRequestForm`, verify credentials,
   401 if wrong, else return `{"access_token": ..., "token_type": "bearer"}`.
6. `get_current_user` dependency + `CurrentUserDep` alias.
7. Also add `owner_id: int` to `Task`, and make `POST /tasks` require
   `current_user: CurrentUserDep`, setting `owner_id = current_user.id`.
8. `GET /tasks/mine` → only tasks belonging to `current_user`.

Test: register, then log in via the `/docs` **Authorize** button (top
right — it uses your `/auth/login` endpoint automatically), then try
`/tasks/mine`.
