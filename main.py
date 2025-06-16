import tkinter as tk
import tkinter.font as tkFont
from tkinter import PhotoImage
import json
import os

class Uniterm1Frame(tk.Frame):
    def __init__(self, master, callback):
        super().__init__(master, bg="#e0e0e0")
        self.callback = callback
        self.build()

    def build(self):
        tk.Label(self, text="Uniterm 1", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))
        self.entry_a = self._add_entry("A:", 1)
        self.entry_b = self._add_entry("B:", 2)
        self.entry_c = self._add_entry("C:", 3)

        btn = tk.Button(self, text="  Pokaż dane  ", command=self.show_data)
        btn.grid(row=4, column=0, columnspan=2, pady=10)

    def _add_entry(self, label, row):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def show_data(self):
        a, b, c = self.entry_a.get(), self.entry_b.get(), self.entry_c.get()
        self.callback(a, b, c)

    def get_values(self):
        return self.entry_a.get(), self.entry_b.get(), self.entry_c.get()


class Uniterm2Frame(tk.Frame):
    def __init__(self, master, callback, get_abc_callback):
        super().__init__(master, bg="#e0e0e0")
        self.callback = callback
        self.get_abc = get_abc_callback
        self.build()

    def build(self):
        tk.Label(self, text="Uniterm 2", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5))

        self.entry_x = self._add_entry("X:", 1)
        self.entry_y = self._add_entry("Y:", 2)

        tk.Label(self, text="Zamień:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.variable = tk.StringVar()
        self.variable.set("A")
        option_menu = tk.OptionMenu(self, self.variable, "A", "B")
        option_menu.grid(row=3, column=1, padx=5, pady=5)

        btn = tk.Button(self, text="  Zamień  ", command=self.convert)
        btn.grid(row=4, column=1, columnspan=2, pady=10)

    def _add_entry(self, label, row):
        tk.Label(self, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(self)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry

    def convert(self):
        x, y = self.entry_x.get(), self.entry_y.get()
        wybrane = self.variable.get()
        a, b, c = self.get_abc()
        self.callback(x, y, wybrane, a, b, c)

class ListaFrame(tk.Frame):
    def __init__(self, master, get_abc_callback, get_xy_callback, get_wybor_callback, **kwargs):
        super().__init__(master, **kwargs)
        self.get_abc = get_abc_callback
        self.get_xy = get_xy_callback
        self.get_wybor = get_wybor_callback
        self.build()

    def build(self):
        tk.Label(self, text="Zapis do JSON", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        tk.Label(self, text="Nazwa:").pack(anchor="w", padx=10)
        self.entry_nazwa = tk.Entry(self)
        self.entry_nazwa.pack(padx=10, pady=(0, 10), fill="x")

        btn_zapisz = tk.Button(self, text="Zapisz", command=self.zapisz)
        btn_zapisz.pack(pady=5)

    def zapisz(self):
        from tkinter import messagebox
        nazwa = self.entry_nazwa.get()
        if not nazwa.strip():
            messagebox.showwarning("Brak nazwy", "Podaj nazwę zapisu.")
            return

        a, b, c = self.get_abc()
        x, y = self.get_xy()
        wybor = self.get_wybor()

        entry = {
            "nazwa": nazwa.strip(),
            "a": a,
            "b": b,
            "c": c,
            "x": x,
            "y": y,
            "wybor": wybor
        }

        try:
            JsonSaver.save_entry(entry)
            messagebox.showinfo("Sukces", "Zapisano dane do pliku JSON.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać danych: {e}")
class BottomFrame(tk.Frame):
    def __init__(self, master, nawias_img):
        super().__init__(master, bg="white")
        self.nawias_img = nawias_img
        self.build()

    def build(self):
        self.canvas = tk.Canvas(self, width=300, height=60, bg="white", highlightthickness=0)
        self.canvas.place(relx=0.05, rely=0.11)

        self.label_before = tk.Label(self, text="", font=("Courier", 14), bg="white")
        self.label_before.place(relx=0.05, rely=0.2)

        self.canvas2 = tk.Canvas(self, width=300, height=20, bg="white", highlightthickness=0)
        self.canvas2.place(relx=0.3, rely=0.11)

        self.label_after = tk.Label(self, text="", font=("Courier", 14), bg="white", justify="left", anchor="nw")
        self.label_after.place(relx=0.32, rely=0.2)

        self.label_nawias = tk.Label(self, image=self.nawias_img, bg="white")
        self.label_nawias.place_forget()

    def show_input_data(self, a, b, c):
        wynik = f"{a} ; {b} ; {c}"
        self.label_before.config(text=wynik)

        self.canvas.delete("all")
        font = tkFont.Font(font=self.label_before.cget("font"))
        szerokosc = font.measure(wynik) + 5

        margin = 1
        y = 10
        self.canvas.create_line(margin, y - 8, margin, y + 8, width=2, fill="steelblue")
        self.canvas.create_line(margin + szerokosc, y - 8, margin + szerokosc, y + 8, width=2, fill="steelblue")
        self.canvas.create_line(margin, y, margin + szerokosc, y, width=4, fill="steelblue")

    def show_result(self, a_new, b_new, c_new, y_val, wybrane):
        kolumny = [a_new, b_new, c_new]
        linia1 = f"{a_new} ; {b_new} ; {c_new}"

        def spacje_do_kolumny(idx):
            return sum(len(kolumny[i]) + 3 for i in range(idx))

        offset = spacje_do_kolumny({"A": 0, "B": 1, "C": 2}[wybrane])
        linia_srednik = " " * offset + ";"
        linia_y = " " * offset + y_val
        self.label_after.config(text=f"{linia1}\n{linia_srednik}\n{linia_y}")

        self.canvas2.delete("all")
        font = tkFont.Font(font=self.label_after.cget("font"))
        szerokosc = font.measure(linia1) + 15

        margin = 10
        y = 10
        self.canvas2.create_line(margin, y - 8, margin, y + 8, width=2, fill="steelblue")
        self.canvas2.create_line(margin + szerokosc, y - 8, margin + szerokosc, y + 8, width=2, fill="steelblue")
        self.canvas2.create_line(margin, y, margin + szerokosc, y, width=4, fill="steelblue")

        tekst_przed = "".join(k + " ; " for k in kolumny[:{"A": 0, "B": 1, "C": 2}[wybrane]])
        szerokosc_srednika = font.measure(" ; ")
        x_label = self.label_after.winfo_x()
        y_label = self.label_after.winfo_y()
        nawias_x = x_label + font.measure(tekst_przed) - szerokosc_srednika + 22
        nawias_y = y_label + 5
        self.label_nawias.place(x=nawias_x + 1, y=nawias_y - 3)

class Lista(tk.Frame):
    def __init__(self, master, get_abc_callback, get_xy_callback, get_wybor_callback,
                 set_abc_callback, set_xy_callback, set_wybor_callback, on_load_callback):
        super().__init__(master)
        self.get_abc = get_abc_callback
        self.get_xy = get_xy_callback
        self.get_wybor = get_wybor_callback
        self.set_abc = set_abc_callback
        self.set_xy = set_xy_callback
        self.set_wybor = set_wybor_callback
        self.on_load = on_load_callback

        self.build()
        self.load_entries()

    def build(self):
        tk.Label(self, text="Zapis/odczyt", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        tk.Label(self, text="Nazwa:").pack(anchor="w", padx=10)
        self.entry_nazwa = tk.Entry(self)
        self.entry_nazwa.pack(padx=10, pady=(0, 10), fill="x")

        # Ramka na przyciski
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5, padx=10, fill="x")

        btn_zapisz = tk.Button(btn_frame, text="Zapisz", command=self.zapisz)
        btn_zapisz.pack(side="top", fill="x", pady=(0, 5))

        btn_usun = tk.Button(btn_frame, text="Usuń", command=self.usun)
        btn_usun.pack(side="top", fill="x")

        # Lista zapisów
        self.listbox = tk.Listbox(self)
        self.listbox.pack(padx=10, pady=5, fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def load_entries(self):
        self.listbox.delete(0, tk.END)
        self.entries = JsonSaver.load_data()
        for entry in self.entries:
            self.listbox.insert(tk.END, entry["nazwa"])

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        index = selection[0]
        entry = self.entries[index]
        self.set_abc(entry["a"], entry["b"], entry["c"])
        self.set_xy(entry["x"], entry["y"])
        self.set_wybor(entry["wybor"])

        if self.on_load:
            self.on_load()

    def zapisz(self):
        from tkinter import messagebox
        nazwa = self.entry_nazwa.get()
        if not nazwa.strip():
            messagebox.showwarning("Brak nazwy", "Podaj nazwę zapisu.")
            return

        a, b, c = self.get_abc()
        x, y = self.get_xy()
        wybor = self.get_wybor()

        entry = {
            "nazwa": nazwa.strip(),
            "a": a,
            "b": b,
            "c": c,
            "x": x,
            "y": y,
            "wybor": wybor
        }

        try:
            JsonSaver.save_entry(entry)
            messagebox.showinfo("Sukces", "Zapisano dane do pliku JSON.")
            self.load_entries()  # Odśwież listę po zapisie
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać danych: {e}")

    def usun(self):
        from tkinter import messagebox
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Brak wyboru", "Wybierz element do usunięcia.")
            return
        index = selection[0]
        entry = self.entries[index]

        # Potwierdzenie usunięcia
        if not messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć '{entry['nazwa']}'?"):
            return

        try:
            JsonSaver.delete_entry(entry["id"])
            messagebox.showinfo("Usunięto", f"Usunięto zapis '{entry['nazwa']}'.")
            self.load_entries()  # Odśwież listę po usunięciu
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się usunąć zapisu: {e}")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt MASI")
        self.root.geometry("1000x600")
        self.nawias_img = PhotoImage(file="nawias1.png")
        self.create_widgets()

    def create_widgets(self):
        # Top frames
        self.uniterm1 = Uniterm1Frame(self.root, self.on_pokaz_dane)
        self.uniterm1.place(relx=0, rely=0, relwidth=0.3, relheight=0.5)

        self.uniterm2 = Uniterm2Frame(self.root, self.on_zamien, self.uniterm1.get_values)
        self.uniterm2.place(relx=0.3, rely=0, relwidth=0.3, relheight=0.5)

        self.lista = Lista(
            self.root,
            get_abc_callback=self.uniterm1.get_values,
            get_xy_callback=self.get_xy,
            get_wybor_callback=self.get_wybor,
            set_abc_callback=self.set_abc,
            set_xy_callback=self.set_xy,
            set_wybor_callback=self.set_wybor,
            on_load_callback=self.on_wczytaj_zapisu
        )
        self.lista.place(relx=0.6, rely=0, relwidth=0.4, relheight=0.5)


        # Bottom
        self.bottom = BottomFrame(self.root, self.nawias_img)
        self.bottom.place(relx=0, rely=0.5, relwidth=1.0, relheight=0.5)

    def on_pokaz_dane(self, a, b, c):
        self.bottom.show_input_data(a, b, c)

    def on_zamien(self, x, y, wybrane, a, b, c):
        if wybrane == "A":
            a_new, b_new, c_new = x, b, c
        elif wybrane == "B":
            a_new, b_new, c_new = a, x, c
        self.bottom.show_result(a_new, b_new, c_new, y, wybrane)

    def get_xy(self):
        return self.uniterm2.entry_x.get(), self.uniterm2.entry_y.get()

    def get_wybor(self):
        return self.uniterm2.variable.get()

    def set_abc(self, a, b, c):
        self.uniterm1.entry_a.delete(0, tk.END)
        self.uniterm1.entry_b.delete(0, tk.END)
        self.uniterm1.entry_c.delete(0, tk.END)
        self.uniterm1.entry_a.insert(0, a)
        self.uniterm1.entry_b.insert(0, b)
        self.uniterm1.entry_c.insert(0, c)

    def set_xy(self, x, y):
        self.uniterm2.entry_x.delete(0, tk.END)
        self.uniterm2.entry_y.delete(0, tk.END)
        self.uniterm2.entry_x.insert(0, x)
        self.uniterm2.entry_y.insert(0, y)

    def set_wybor(self, wybor):
        self.uniterm2.variable.set(wybor)

    def on_wczytaj_zapisu(self):
        a, b, c = self.uniterm1.get_values()
        x, y = self.get_xy()
        wybor = self.get_wybor()

        self.bottom.show_input_data(a, b, c)
        if wybor == "A":
            a_new, b_new, c_new = x, b, c
        elif wybor == "B":
            a_new, b_new, c_new = a, x, c
        else:
            return
        self.bottom.show_result(a_new, b_new, c_new, y, wybor)

class JsonSaver:
    FILE_PATH = "dane.json"

    @staticmethod
    def load_data():
        if not os.path.exists(JsonSaver.FILE_PATH):
            return []
        with open(JsonSaver.FILE_PATH, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def save_entry(entry):
        data = JsonSaver.load_data()
        next_id = max([item["id"] for item in data], default=0) + 1
        entry_with_id = {"id": next_id, **entry}
        data.append(entry_with_id)
        with open(JsonSaver.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @staticmethod
    def delete_entry(entry_id):
        data = JsonSaver.load_data()
        data = [item for item in data if item["id"] != entry_id]
        with open(JsonSaver.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
