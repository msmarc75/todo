import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import datetime

# Fonction pour initialiser la liste des tâches
def init_todo_list():
    if 'todos' not in st.session_state:
        st.session_state.todos = []

# Fonction pour ajouter une tâche
def add_todo():
    todo = st.session_state.new_todo
    if todo:
        st.session_state.todos.append({"task": todo, "completed": False})
        st.session_state.new_todo = ""  # Reset the input box after adding

# Fonction pour marquer une tâche comme terminée
def complete_todo(index):
    st.session_state.todos[index]["completed"] = True

# Fonction pour supprimer une tâche
def delete_todo(index):
    del st.session_state.todos[index]

# Initialisation de la liste de tâches
init_todo_list()

# Titre de l'application
st.set_page_config(page_title="Todoist-like Todo List", page_icon="✅", layout="wide")
st.title("Todo List App")

# Charger l'image d'icône depuis l'URL
icon_url = "https://upload.wikimedia.org/wikipedia/commons/7/7e/To-do-list-checklist-icon.png"

# Récupérer l'image depuis l'URL
response = requests.get(icon_url)

# Vérifier si la réponse est valide (code 200) et si le contenu est une image
if response.status_code == 200:
    try:
        # Essayer de charger l'image
        todo_icon = Image.open(BytesIO(response.content))
        st.image(todo_icon, width=100)
    except Exception as e:
        # Si l'image ne peut pas être ouverte, afficher l'erreur
        st.error(f"Erreur lors de l'ouverture de l'image : {e}")
else:
    st.error(f"Échec du téléchargement de l'image, code de réponse HTTP : {response.status_code}")

# Entrée de nouvelle tâche
with st.container():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Ajouter une nouvelle tâche", key="new_todo", on_change=add_todo, label_visibility="collapsed")

    with col2:
        add_button = st.button("Ajouter", use_container_width=True, on_click=add_todo)

# Affichage des tâches
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2, col3 = st.columns([5, 2, 1])

        with col1:
            # Style des tâches
            if todo["completed"]:
                st.markdown(f"**<s>{todo['task']}</s>**", unsafe_allow_html=True)
            else:
                st.markdown(todo['task'])

        with col2:
            # Boutons de gestion des tâches
            if not todo["completed"]:
                if st.button("✔️ Terminer", key=f"complete_{i}", on_click=complete_todo, args=(i,)):
                    st.experimental_rerun()

        with col3:
            if st.button("❌ Supprimer", key=f"delete_{i}", on_click=delete_todo, args=(i,)):
                st.experimental_rerun()

else:
    st.write("Aucune tâche à afficher. Ajoutez une nouvelle tâche ci-dessus.")

# Affichage de l'heure actuelle
st.write(f"Heure actuelle : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
