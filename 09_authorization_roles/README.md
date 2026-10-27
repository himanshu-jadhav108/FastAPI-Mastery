# 09 — Role-Based Authorization

## Theory

Module 08 answered "who are you?" This module answers "are you allowed to
do *this*?"

The pattern: build a dependency **factory** — a function that returns a
dependency, parameterized by what role is required.

```python
def require_role(required_role: str):
    def role_checker(current_user: CurrentUserDep) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Requires '{required_role}' role.",
            )
        return current_user
    return role_checker

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    current_user: Annotated[User, Depends(require_role("admin"))],
):
    ...
```

Note the distinction:
- Missing/invalid token → **401 Unauthorized** ("I don't know who you are")
- Valid token, wrong role → **403 Forbidden** ("I know who you are, you're
  just not allowed")

**Ownership checks** are a related, even more common pattern — not "is
your role X" but "is this *your* resource":

```python
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user: CurrentUserDep, session: SessionDep):
    task = session.get(Task, task_id)
    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your task.")
    ...
```

## Task

Open `starter.py` (carries over module 08's User/Task/auth).

1. Add `role: str = "user"` to `User`.
2. Write `require_role(required_role: str)` as shown.
3. `GET /admin/users` → list all users, requires `role="admin"`.
   `response_model=list[UserRead]`.
4. `DELETE /tasks/{task_id}` → a user can delete their own task
   regardless of role; an admin can delete *any* task. Anyone else gets
   403. 404 if the task doesn't exist.
5. `PATCH /tasks/{task_id}/reassign` → admin-only (`require_role("admin")`),
   accepts a query param `new_owner_id: int`, reassigns the task.

Test by registering two users, manually setting one's role to `"admin"`
(you'll need to poke the DB directly or add a temporary endpoint — real
apps seed this at setup or via a separate internal tool), and confirming
403s happen correctly for the non-admin.
