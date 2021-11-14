# *Виключно для індивідуальної роботи*
# Завантажені бібліотеки (tkinter - для інтерфейсу, pandas - для реалізації імпорту таблиці,
# matplotlib - для виведення графіків, sklearn - для обчислення методу локтя та кластеризації
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Параметри головного вікна, головне тло програми;
main = tk.Tk()
main.title("Індивідуальна робота")
main.geometry("600x600")
main.resizable(0, 0)

# Інтерфейс програми та логіка;
frame_t = tk.LabelFrame(main, text="Таблиця", font=('arial', 11))
frame_t.place(height=300, width=600)

file_frame = tk.LabelFrame(main, text="Головне меню", font=('arial', 11))
file_frame.place(height=400, width=600, rely=0.50, relx=0)

button_o = tk.Button(file_frame, text="Додати таблицю", font=('arial', 10), command=lambda: file_dialog())
button_o.place(rely=0.55, relx=0.02)

button_l = tk.Button(file_frame, text="Завантажити таблицю", font=('arial', 10), command=lambda: load_table_data())
button_l.place(rely=0.55, relx=0.21)

button_k = tk.Button(file_frame, text="Кластеризувати дані", font=('arial', 10), command=lambda: get_kmeans())
button_k.place(rely=0.55, relx=0.46)

button_e = tk.Button(file_frame, text="Метод «локтя»", font=('arial', 10), command=lambda: get_elbow())
button_e.place(rely=0.55, relx=0.70)

button_e = tk.Button(file_frame, text="Вихід", font=('arial', 10), command=main.destroy)
button_e.place(rely=0.55, relx=0.88)

label_file = ttk.Label(file_frame, text="Файл не обрано", font=('arial', 11))
label_file.place(rely=0.01, relx=0.425)

label_k = ttk.Label(file_frame, text="Кількість кластерів:", font=('arial', 9))
label_k.place(rely=0.10, relx=0.10)

label_t = ttk.Label(file_frame, text="Підпис зверху:", font=('arial', 9))
label_t.place(rely=0.20, relx=0.10)

label_m = ttk.Label(file_frame, text="Ім'я 1-го стовпця:", font=('arial', 9))
label_m.place(rely=0.10, relx=0.53)

label_n = ttk.Label(file_frame, text="Ім'я 2-го стовпця:", font=('arial', 9))
label_n.place(rely=0.20, relx=0.53)

label_x = ttk.Label(file_frame, text="Підпис X:", font=('arial', 9))
label_x.place(rely=0.30, relx=0.10)

label_y = ttk.Label(file_frame, text="Підпис Y:", font=('arial', 9))
label_y.place(rely=0.40, relx=0.10)

# Комірки для вводу даних
entry_x = tk.Entry(file_frame)
entry_x.place(rely=0.30, relx=0.30)

entry_t = tk.Entry(file_frame)
entry_t.place(rely=0.20, relx=0.30)

entry_y = tk.Entry(file_frame)
entry_y.place(rely=0.40, relx=0.30)

entry_k = tk.Entry(file_frame)
entry_k.place(rely=0.10, relx=0.30)

entry_m = tk.Entry(file_frame)
entry_m.place(rely=0.10, relx=0.71)

entry_n = tk.Entry(file_frame)
entry_n.place(rely=0.20, relx=0.71)

label_a = ttk.Label(file_frame, text="БІКС-51 Чиренко Н.П.", font=('arial', 6))
label_a.place(rely=0.68, relx=0.85)

# Секція для перегляду завантажених даних;
tv1 = ttk.Treeview(frame_t)
tv1.place(relheight=1, relwidth=1)

windowy = tk.Scrollbar(frame_t, orient="vertical", command=tv1.yview)
windowx = tk.Scrollbar(frame_t, orient="horizontal", command=tv1.xview)
tv1.configure(xscrollcommand=windowx.set, yscrollcommand=windowy.set)
windowx.pack(side="bottom", fill="x")
windowy.pack(side="right", fill="y")


# Перед додаванням файлу, попередній файл видаляється з секції попереднього перегляду, щоб уникнути спотворення;
def file_dialog():
    tv1.delete(*tv1.get_children())
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Оберіть файл",
                                          filetype=(("CSV файл", "*.csv"), ("Усі файли", "*.*")))
    label_file["text"] = filename
    return None


# Завантажує файл та передає глобальну змінну для подальшої взаємодії, для методу локтя та кластеризації
def load_table_data():
    global readf
    file_path = label_file["text"]
    try:
        import_table = "{}".format(file_path)
        readf = pd.read_csv(import_table)
    except ValueError:
        tk.messagebox.showerror("Помилка", "Файл не може бути прочитаним, оберіть .csv")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Помилка", "Щоб завантажити таблицю, її спочатку потрібно додати!")
        return None
    tv1["column"] = list(readf.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column)
    readf_rows = readf.to_numpy().tolist()
    for row in readf_rows:
        tv1.insert("", "end", values=row)
    return None


# Метод "локтя", для обчислення оптимальної кількості кластерів, формує графік функції в діапазоні
# від 1-11 можливих варіантів, оптимальним є той, який не змінюється з довжиною кривої
def get_elbow():
    try:
        wcss = []
        dff = DataFrame(readf, columns=[entry_m.get(), entry_n.get()])
        for i in range(1, 11):
            eblow = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=3)
            eblow.fit(dff)
            wcss.append(eblow.inertia_)
        plt.figure('Метод локтя')
        plt.plot(range(1, 11), wcss)
        plt.title('Метод локтя')
        plt.xlabel('Кількість кластерів')
        plt.ylabel('WCSS')
        plt.show()
    except ValueError:
        tk.messagebox.showerror("Помилка", "Не задані або не вірно задані комірки")
        return None
    except NameError:
        tk.messagebox.showerror("Помилка", "Не заватажено файл!")
        return None


# Ця функція обраховує отримані данні з комірок та основі кількості клстерів сформує графік з центроїдами кожного
# кластеру, кількість центроїдів напряму залежить від кількості заданих кластерів
def get_kmeans():
    try:
        clusternum = int(entry_k.get())
        dff = DataFrame(readf, columns=[entry_m.get(), entry_n.get()])
        kmeans = KMeans(n_clusters=clusternum, init='k-means++', max_iter=300, n_init=10, random_state=3)
        kmeans.fit(dff)
    except ValueError:
        tk.messagebox.showerror("Помилка", "Не заватажено файл або не вірно обрані комірки")
        return None
    except NameError:
        tk.messagebox.showerror("Помилка", "Такої/таких комірок немає в таблиці")
        return None
    centroids = kmeans.cluster_centers_
    plt.figure('Результат кластерізації')
    plt.scatter(dff[entry_m.get()], dff[entry_n.get()], c=kmeans.labels_.astype(float), s=20, alpha=0.7)
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=20)
    plt.title(entry_t.get())
    plt.xlabel(entry_x.get())
    plt.ylabel(entry_y.get())
    plt.show()


main.mainloop()
