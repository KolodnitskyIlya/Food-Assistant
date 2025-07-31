import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/api")

if "token" not in st.session_state:
    st.session_state.token = None

if "register_mode" not in st.session_state:
    st.session_state.register_mode = False

if "app_started" not in st.session_state:
    st.session_state.app_started = False

st.set_page_config(page_title="Food Assistant", layout="centered")

# === Форма входа ===
def login_form():
    st.title("🔐 Вход")
    username = st.text_input("Логин")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        response = requests.post(f"{API_URL}/auth/login", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.success("Успешный вход!")
        else:
            st.error("Ошибка авторизации")

    if st.session_state.token:
        if st.button("Перейти к приложению"):
            st.session_state.app_started = True

    if st.button("Нет аккаунта? Зарегистрироваться"):
        st.session_state.register_mode = True

# === Форма регистрации ===
def register_form():
    st.title("📝 Регистрация")
    username = st.text_input("Новый логин")
    password = st.text_input("Пароль", type="password")
    confirm_password = st.text_input("Подтвердите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if password != confirm_password:
            st.error("Пароли не совпадают")
            return
        response = requests.post(f"{API_URL}/auth/register", json={
            "username": username,
            "password": password
        })
        if response.status_code == 200:
            st.success("Успешная регистрация! Теперь войдите.")
            st.session_state.register_mode = False
        else:
            st.error(f"Ошибка регистрации: {response.text}")

    if st.button("Назад ко входу"):
        st.session_state.register_mode = False

# === Основное приложение ===
def main_app():
    st.title("🍲 Подбор рецептов")

    st.header("Добавить рецепт")
    name = st.text_input("Название рецепта")
    goal = st.selectbox("Цель", ["Похудение", "Набор массы", "Здоровое питание"])
    time = st.number_input("Время готовки (мин)", min_value=1)
    ingredients = st.text_area("Ингредиенты (через запятую)")
    description = st.text_area("Описание")

    if st.button("Сохранить рецепт"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        data = {
            "name": name,
            "goal": goal,
            "cooking_time": time,
            "ingredients": ingredients,
            "description": description
        }
        response = requests.post(f"{API_URL}/recipes/", json=data, headers=headers)
        if response.status_code == 200:
            st.success("Рецепт добавлен!")
        else:
            st.error("Ошибка при добавлении рецепта")

    st.header("📋 Ваши рецепты")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{API_URL}/recipes/", headers=headers)
    if response.status_code == 200:
        recipes = response.json()
        for r in recipes:
            with st.expander(f"{r['name']} ({r['cooking_time']} мин)"):
                st.markdown(f"**Цель:** {r['goal']}")
                st.markdown(f"**Ингредиенты:** {r['ingredients']}")
                st.markdown(f"**Описание:** {r['description']}")
    else:
        st.warning("Не удалось загрузить рецепты")

# === Запуск ===
if st.session_state.app_started and st.session_state.token:
    main_app()
else:
    if st.session_state.register_mode:
        register_form()
    else:
        login_form()