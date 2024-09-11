# Social Media REST API

## Description

This is a REST API built with FastAPI with testing using Pytest and CI/CD using Github Actions.

- API **Documentation** with _Swagger UI_.
  - [**documentation**](https://socialsyncapi.vercel.app/docs)
- Users can register and login using **JWT**.
- Users can create, read, update, and delete posts (_some operations require authentication_).
- Users can vote on posts.

## Models

- **posts** (`id`, `title`, `owner_id`, `content`, `published`, `created_at`)
- **users** (`id`, `email`, `password`, `created_at`)
- **votes** (`user_id`, `post_id`)

## Tech Stack

- **FastAPI**
- **PostgreSQL**
- _SQLAlchemy_
- _Pydantic_
- _Alembic_
