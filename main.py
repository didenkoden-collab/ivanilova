import json
import os
from datetime import datetime

DATA_FILE = "books.json"

def load_books():
    """Загружает список книг из JSON-файла"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_books(books):
    """Сохраняет список книг в JSON-файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(books, file, ensure_ascii=False, indent=2)

def is_duplicate(books, author, title):
    """Проверяет, есть ли уже книга с таким автором и названием"""
    return any(book['author'].lower() == author.lower() 
               and book['title'].lower() == title.lower() 
               for book in books)

def add_book():
    """Добавляет новую книгу"""
    books = load_books()
    
    print("\n=== Добавление книги ===")
    author = input("Введите автора: ").strip()
    title = input("Введите название: ").strip()
    
    # Проверка на дубликаты (связано с Issue)
    if is_duplicate(books, author, title):
        print("Ошибка: Такая книга уже есть в списке!")
        return
    
    # Валидация оценки
    while True:
        try:
            rating = int(input("Введите оценку (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Оценка должна быть от 1 до 5!")
        except ValueError:
            print("Введите целое число!")
    
    date = input("Введите дату прочтения (ГГГГ-ММ-ДД): ").strip()
    
    # Валидация даты
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        date = datetime.now().strftime('%Y-%m-%d')
        print(f"Дата изменена на сегодняшнюю: {date}")
    
    book = {
        'author': author,
        'title': title,
        'rating': rating,
        'date': date
    }
    
    books.append(book)
    save_books(books)
    print(f"Книга '{title}' успешно добавлена!")

def show_books():
    """Показывает все книги"""
    books = load_books()
    
    if not books:
        print("\nСписок книг пуст!")
        return
    
    print("\n=== Список книг ===")
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['author']} - \"{book['title']}\"")
        print(f"   Оценка: {book['rating']}/5, Дата: {book['date']}")

def show_average_rating():
    """Показывает среднюю оценку всех книг"""
    books = load_books()
    
    if not books:
        print("\nНет книг для расчёта средней оценки!")
        return
    
    total = sum(book['rating'] for book in books)
    average = total / len(books)
    print(f"\nСредняя оценка всех книг: {average:.2f}")

def show_author_stats():
    """Показывает статистику по авторам"""
    books = load_books()
    
    if not books:
        print("\nНет книг для статистики!")
        return
    
    stats = {}
    for book in books:
        author = book['author']
        stats[author] = stats.get(author, 0) + 1
    
    print("\n=== Статистика по авторам ===")
    for author, count in sorted(stats.items()):
        print(f"{author}: {count} книг(а/и)")

def delete_book():
    """Удаляет книгу по индексу"""
    books = load_books()
    
    if not books:
        print("\nНет книг для удаления!")
        return
    
    show_books()
    
    try:
        index = int(input("\nВведите номер книги для удаления: ")) - 1
        if 0 <= index < len(books):
            deleted = books.pop(index)
            save_books(books)
            print(f"Книга '{deleted['title']}' удалена!")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Введите число!")

def main():
    """Главное меню приложения"""
    while True:
        print("\n" + "="*40)
        print("📚 ТРЕКЕР ПРОЧИТАННЫХ КНИГ")
        print("="*40)
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Показать среднюю оценку")
        print("4. Статистика по авторам")
        print("5. Удалить книгу")
        print("6. Выход")
        print("="*40)
        
        choice = input("Выберите действие (1-6): ").strip()
        
        if choice == '1':
            add_book()
        elif choice == '2':
            show_books()
        elif choice == '3':
            show_average_rating()
        elif choice == '4':
            show_author_stats()
        elif choice == '5':
            delete_book()
        elif choice == '6':
            print("\nДо свидания! 📖")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")

if __name__ == "__main__":
    main()
