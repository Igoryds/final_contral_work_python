import json
import datetime

class Note:
    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'created_at': self.created_at
        }

class NoteApp:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, 'r') as f:
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = []

    def save_notes(self):
        with open(self.filename, 'w') as f:
            json.dump(self.notes, f)

    def create_note(self, id, title, body):
        note = Note(id, title, body)
        self.notes.append(note.to_dict())
        self.save_notes()

    def get_note(self, id):
        for note in self.notes:
            if note['id'] == id:
                return note
        return None

    def update_note(self, id, title=None, body=None):
        note = self.get_note(id)
        if note is not None:
            if title:
                note['title'] = title
            if body:
                note['body'] = body
            note['created_at'] = datetime.datetime.now().isoformat()
            self.save_notes()

    def delete_note(self, id):
        note = self.get_note(id)
        if note is not None:
            self.notes.remove(note)
            self.save_notes()

    def list_notes(self):
        sorted_notes = sorted(self.notes, key=lambda x: x['created_at'], reverse=True)
        for note in sorted_notes:
            print(note)

    def user_interface(self):
        while True:
            print("1. Создать заметку")
            print("2. Получить заметку")
            print("3. Обновить заметку")
            print("4. Удалить заметку")
            print("5. Показать все заметки")
            print("6. Выход")
            choice = input("Выберите действие: ")
            if choice == '1':
                id = input("Введите ID: ")
                title = input("Введите заголовок: ")
                body = input("Введите текст заметки: ")
                self.create_note(id, title, body)
            elif choice == '2':
                id = input("Введите ID заметки: ")
                note = self.get_note(id)
                if note:
                    print(note)
                else:
                    print("Заметка не найдена.")
            elif choice == '3':
                id = input("Введите ID заметки: ")
                title = input("Введите новый заголовок (оставьте пустым, чтобы не менять): ")
                body = input("Введите новый текст заметки (оставьте пустым, чтобы не менять): ")
                self.update_note(id, title, body)
            elif choice == '4':
                id = input("Введите ID заметки: ")
                self.delete_note(id)
            elif choice == '5':
                self.list_notes()
            elif choice == '6':
                break
            else:
                print("Неверный выбор. Пожалуйста, попробуйте еще раз.")

app = NoteApp('notes.json')
app.user_interface()
