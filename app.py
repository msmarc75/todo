import streamlit as st
import datetime

# Fonction pour initialiser la liste des tâches
def init_todo_list():
    if 'todos' not in st.session_state:
        st.session_state.todos = []

# Fonction pour ajouter une tâche
def add_todo():
    todo = st.session_state.new_todo
    if todo:
        st.session_state.todos.append(todo)
        st.session_state.new_todo = ""  # Reset the input box after adding

# Fonction pour marquer une tâche comme terminée
def complete_todo(index):
    st.session_state.todos[index] = f"✔️ {st.session_state.todos[index]}"

# Fonction pour supprimer une tâche
def delete_todo(index):
    del st.session_state.todos[index]

# Initialisation de la liste de tâches
init_todo_list()

# Titre de l'application
st.title("To-Do List App")

# Entrée de nouvelle tâche
st.text_input("Nouvelle tâche", key="new_todo", on_change=add_todo)

# Affichage des tâches
if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos):
        col1, col2 = st.columns([5, 1])

        with col1:
            st.write(f"{i+1}. {todo}")

        with col2:
            if st.button("Terminer", key=f"complete_{i}", on_click=complete_todo, args=(i,)):
                st.experimental_rerun()
            if st.button("Supprimer", key=f"delete_{i}", on_click=delete_todo, args=(i,)):
                st.experimental_rerun()

else:
    st.write("Aucune tâche à afficher.")

# Affichage de l'heure actuelle
st.write(f"Heure actuelle : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
