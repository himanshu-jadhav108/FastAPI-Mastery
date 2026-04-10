"""
Module 01 — Basics
Fill in the TODOs. Run with: fastapi dev starter.py
"""

from fastapi import FastAPI

# TODO 1: create the FastAPI app instance and assign it to `app`
app = ...

# In-memory storage for now — replaced by a real database in module 06.
tasks: list[dict] = []


# TODO 2: create a GET route at "/" that returns
#   {"message": "Task Manager API is running"}


# TODO 3: create a GET route at "/tasks" that returns the `tasks` list


# TODO 4: create a POST route at "/tasks" that returns
#   {"received": "ok"}
# (we'll actually accept + store data starting in module 03)


# TODO 5: create a GET route at "/ping" that returns {"pong": True}
