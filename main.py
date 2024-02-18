import tkinter as tk
from tkinter import Canvas, Button, Text, messagebox
from functools import partial

class Lymphocyte:
    def __init__(self, black_pixels, white_pixels):
        self.black_pixels = black_pixels
        self.white_pixels = white_pixels

    def calculate_affinity(self, antigen_matrix):
        total_pixels = len(self.black_pixels) + len(self.white_pixels)
        black_pixels_matched = sum(antigen_matrix[i][j] == 'B' for i, j in self.black_pixels)
        affinity = black_pixels_matched / total_pixels
        return affinity

class ImmuneSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Искусственная Иммунная Система")

        # Создаем матрицу для хранения данных о рисунке
        self.matrix_size = 5
        self.matrix = [['W'] * self.matrix_size for _ in range(self.matrix_size)]

        # Создаем Canvas для рисования
        self.canvas = Canvas(self.master, width=self.matrix_size * 150, height=self.matrix_size * 140, bg="white")
        self.canvas.pack()

        # Создаем Text для отображения введенной матрицы
        self.input_matrix_text = Text(self.master, height=self.matrix_size, width=self.matrix_size * 2)
        self.input_matrix_text.pack()

        # Создаем кнопку для подачи на распознавание
        self.recognize_button = Button(self.master, text="Распознать", command=self.recognize)
        self.recognize_button.pack()

        # Привязываем обработчик к Canvas для отслеживания рисования
        self.canvas.bind("<B1-Motion>", self.draw)

        # Создаем лимфоциты с паттернами букв
        self.lymphocytes = [
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)], []),
            Lymphocyte([(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (4, 1), (4, 2), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4), (4, 1), (4, 2), (4, 3), (4, 4)], []),
            Lymphocyte([(0, 1), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 1), (2, 1), (2, 2), (2, 3), (3, 3), (4, 1), (4, 2), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 1), (2, 1), (2, 2), (2, 3), (3, 1), (3, 3), (4, 1), (4, 2), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (2, 3), (3, 3), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 4), (4, 1), (4, 2), (4, 3)], []),
            Lymphocyte([(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3), (3, 3), (4, 1), (4, 2), (4, 3)], []),
        ]

    def draw(self, event):
        # Определяем координаты клетки, в которой происходит рисование
        x, y = event.x // 150, event.y // 150

        # Записываем информацию о рисовании в матрицу
        self.matrix[y][x] = 'B'

        # Обновляем Text с введенной матрицей
        self.update_input_matrix_text()

        # Рисуем черный квадрат на Canvas
        self.canvas.create_rectangle(x * 150, y * 150, (x + 1) * 150, (y + 1) * 150, fill="black")

    def recognize(self):
        # Пример: вывод матрицы на консоль
        print("Распознанная матрица:")
        for row in self.matrix:
            print(row)

        # Классификация антигена
        classified_antigen = self.classify_antigen(self.matrix, 0.6)

        if classified_antigen is not None:
            messagebox.showinfo("Результат", f"Антиген классифицирован как {classified_antigen}")
        else:
            messagebox.showinfo("Результат", "Ни один антиген не классифицирован")

        self.canvas.delete("all")
        self.clear_matrix()

    def classify_antigen(self, antigen_matrix, threshold):
        max_affinity = 0
        classified_antigen = None

        for antigen_id, lymphocyte in enumerate(self.lymphocytes):
            affinity = lymphocyte.calculate_affinity(antigen_matrix)

            # Если аффинность выше порога и больше текущей максимальной аффинности
            if affinity > max_affinity and affinity >= threshold:
                max_affinity = affinity
                classified_antigen = antigen_id

        return classified_antigen

    def clear_matrix(self):
        # Очищаем матрицу
        self.matrix = [['W'] * self.matrix_size for _ in range(self.matrix_size)]

        # Обновляем Text с введенной матрицей
        self.update_input_matrix_text()

    def update_input_matrix_text(self):
        # Отображение введенной матрицы в Text
        self.input_matrix_text.delete(1.0, tk.END)
        for row in self.matrix:
            self.input_matrix_text.insert(tk.END, ' '.join(row) + '\n')

# Создаем главное окно
root = tk.Tk()
app = ImmuneSystemApp(root)
root.mainloop()
