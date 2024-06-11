import os.path
import tkinter
from tkinter import colorchooser, ttk, filedialog, messagebox
import customtkinter
from PIL import Image, ImageTk, ImageDraw, ImageFont
from matplotlib import font_manager


BACKGROUND = "#393E46"
LABEL_FOREGROUND = "#F0F0F0"
BUTTON_BACKGROUND = "grey"


class Watermark:
    def __init__(self):
        self.font_family = []
        self.dict_font = {}
        font_system = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_system.sort()
        for f in font_system:
            self.dict_font[(f.split("\\")[-1].split(".")[0])] = f
            self.font_family.append(self.dict_font)

        self.font_size_list = [i for i in range(5, 1201)]

        # -------- Variables iniciales ---------
        self.font_type = "arial.ttf"
        self.watermarking_text = ""
        self.opacity = 255
        red = 255
        green = 255
        blue = 255
        self.fill = (red, green, blue, self.opacity)
        self.angle_rot = 0
        self.file_path = ""

    def show_text(self):
        """
        Muestra la marca de agua.
        """
        self.watermarking_text = watermarking_entry.get()
        self.show_image()

# -------- Procesado de imagen --------
    def choose_color(self):
        """
        Cambio de color.
        """
        try:
            color = colorchooser.askcolor()
            self.opacity = self.choose_opacity(255)
            self.fill = (color[0][0], color[0][1], color[0][2], self.opacity)
            color_button.config(background=color[1])
            self.show_image()
        except TypeError:
            pass

    def choose_opacity(self, value):
        """
        Cambia la opacidad de la marca de agua.
        """
        self.opacity = int(slider.get())
        self.show_image()
        return self.opacity

    def choose_font(self, *event):
        """
        Cambio de fuente.
        """
        new_font = font_combo_family.get()
        self.font_type = self.dict_font[new_font]
        self.show_image()

    def choose_size(self, *event):
        """
        Modifica el tamaño de letra.
        """
        self.font_size = int(font_combo_size.get())
        self.show_image()

# -------- Movimiento de la marca de agua con las flechas del teclado --------
    def move_top_botton(self, event):
        if event.keysym == "Up":
            self.coord_y = self.coord_y - 10
        if event.keysym == "Down":
            self.coord_y = self.coord_y + 10
        self.show_image()

    def move_left_right(self, event):
        if event.keysym == "Left":
            self.coord_x = self.coord_x - 10
        if event.keysym == "Right":
            self.coord_x = self.coord_x + 10
        self.show_image()

# -------- Movimiento de la marca de agua con las flechas del entorno gráfico --------
    def move_top_botton_button(self, movement):
        if movement == "Up":
            self.coord_y = self.coord_y - 10
        if movement == "Down":
            self.coord_y = self.coord_y + 10
        self.show_image()

    def move_left_right_button(self, movement):
        if movement == "Left":
            self.coord_x = self.coord_x - 10
        if movement == "Right":
            self.coord_x = self.coord_x + 10
        self.show_image()

# -------- Rotación de la marca de agua --------
    def rotate_right(self):
        self.angle_rot += 17
        self.show_image()

    def rotate_left(self):
        self.angle_rot += -17
        self.show_image()

# --------- Carga de imagen y texto --------
    def load_image(self):
        """
        Selecciona la foto a cargar.
        Obtiene la posición inicial en la que se mostrará el texto y el tamaño de la fuente.
        """
        self.file_path = filedialog.askopenfilename(filetypes=(("png", "*.png"), ("jpg, jpeg", "*.jpg"),
                                                               ("jpg, jpeg", "*.jpeg"), ("bmp", "*.bmp"),
                                                               ("gif", "*.gif"),
                                                               ("All images", "*.png *.jpg *.jpeg *.bmp *.gif")))

        new_image = Image.open(self.file_path)
        [self.image_size_width, self.image_size_height] = new_image.size
        self.coord_x = self.image_size_width // 2
        self.coord_y = self.image_size_height // 2
        self.font_size = self.image_size_width // 10
        font_combo_size.set(self.font_size)
        image_frame.grid_forget()
        self.show_image()

    def save(self):
        """
        Guarda la imagen.
        """
        file = filedialog.asksaveasfilename(filetypes=(("png", "*.png"), ("jpg, jpeg", "*.jpg"),
                                                       ("jpg, jpeg", "*.jpeg"), ("bmp", "*.bmp"), ("gif", "*.gif")))

        if file:
            path = os.path.abspath(file)
            try:
                self.image.save(path, quality=95)
            except OSError:
                rgb_image = self.image.convert("RGB")
                rgb_image.save(path, quality=95)
            except ValueError:
                self.image.save(path + ".png", quality=95)
            except AttributeError:
                messagebox.showerror("Image error", "There is no image. Must load an image.")

    def image_resize(self):
        """
        Redimensiona la imagen a mostrar.
        :return: devuelve la imagen con las nuevas dimensiones.
        """
        new_width = self.image_size_width
        new_height = self.image_size_height

        if self.image_size_width > 500:
            new_width = 500
            r = self.image_size_width / 500  # razón de proporcionalidad: medida mayor entre medida menor
            new_height = int(self.image_size_height / r)
        img_resize = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return ImageTk.PhotoImage(img_resize)

    def show_image(self):
        """
        Abre la imagen y crea la capa de texto.
        Muestra la imagen en la etiqueta "image_label".
        """
        if self.file_path != "":
            with Image.open(self.file_path) as self.image:
                self.fill = (self.fill[0], self.fill[1], self.fill[2], self.opacity)
                text = Image.new(mode="RGBA", size=self.image.size, color=(255, 255, 255, 0))
                fnt = ImageFont.truetype(self.font_type, self.font_size)
                draw_text = ImageDraw.Draw(text)
                draw_text.text((self.coord_x, self.coord_y), self.watermarking_text, font=fnt, fill=self.fill)
                image_rotated = text.rotate(self.angle_rot, resample=Image.BICUBIC, center=(self.coord_x, self.coord_y))
                self.image.paste(image_rotated, image_rotated)

            img_tk = self.image_resize()
            image_label.config(image=img_tk)
            image_label.image = img_tk


watermark = Watermark()
watermark.show_image()

# --------- Inicializa la ventana --------
window = tkinter.Tk()
window.title("Image Watermarking Desktop App")
window.minsize(width=100, height=400)
window.maxsize(width=1050, height=1900)
window.config(padx=10, pady=10, background=BACKGROUND)

# -------- Frame inicial en el que se mostrará la imagen ---------
image_frame = tkinter.Frame(width=300, height=300, relief="raised", borderwidth=2)
image_frame.grid(row=0, column=0, rowspan=15)

# --------- Etiqueta en la que se cargará la imagen ---------
image_label = tkinter.Label()
image_label.grid(row=0, column=0, rowspan=15)
label = tkinter.Label(text="arena", font=('Segoe UI', 7), background=BACKGROUND, foreground=LABEL_FOREGROUND)
label.grid(row=16, column=0, sticky="w")

# -------- Botón de carga ---------
load = tkinter.Button(text="Load image", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                      command=watermark.load_image)
load.grid(row=0, column=3, pady=15, padx=10, ipadx=5, sticky="w")

# -------- Marca de agua ---------
watermarking_label = tkinter.Label(text="Watermark", background=BACKGROUND, foreground=LABEL_FOREGROUND)
watermarking_label.grid(row=1, column=2, pady=5, padx=10, ipadx=5, sticky="e")
watermarking_entry = tkinter.Entry(width=32, background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND)
watermarking_entry.grid(row=1, column=3, pady=5, padx=10, sticky="w", columnspan=6)
watermarking_button = tkinter.Button(text="Show", background=BUTTON_BACKGROUND,
                                     foreground=LABEL_FOREGROUND, command=watermark.show_text)
watermarking_button.grid(row=1, column=7, pady=5, padx=10, ipadx=5, sticky="w")

# -------- Color ---------
color_label = tkinter.Label(text="Color", width=5, height=1, background=BACKGROUND, foreground=LABEL_FOREGROUND)
color_label.grid(row=2, column=2, pady=5, padx=10, sticky="e")
color_button = tkinter.Button(text="  ", background="white", command=watermark.choose_color)
color_button.grid(row=2, column=3, pady=5, padx=10, ipadx=5, sticky="w")

# -------- Opacidad ---------
slider_label = tkinter.Label(text="Opacity", background=BACKGROUND, foreground=LABEL_FOREGROUND)
slider_label.grid(row=3, column=2, pady=5, padx=10, ipadx=5, sticky="e")
slider = customtkinter.CTkSlider(window, from_=0, to=255, button_color="#7F8487", command=watermark.choose_opacity)
slider.set(255)
slider.grid(row=3, column=3, pady=5, padx=5, sticky="w", columnspan=3)

# -------- Tipo de fuente ---------
combo_family_label = tkinter.Label(text="Font", background=BACKGROUND, foreground=LABEL_FOREGROUND)
combo_family_label.grid(row=5, column=2, pady=5, padx=10, ipadx=5, sticky="e")
font_combo_family = ttk.Combobox(window, values="\n".join(watermark.dict_font.keys()), width=28)
font_combo_family.set("Arial")
font_combo_family.bind("<<ComboboxSelected>>", watermark.choose_font)
font_combo_family.grid(row=5, column=3, pady=5, padx=10, sticky="w", columnspan=4)

# -------- Tamaño de la fuente ---------
combo_size_label = tkinter.Label(text="Size", background=BACKGROUND, foreground=LABEL_FOREGROUND)
combo_size_label.grid(row=6, column=2, pady=5, padx=10, ipadx=5, sticky="e")
font_combo_size = ttk.Combobox(window, values=watermark.font_size_list, width=5)
font_combo_size.bind("<<ComboboxSelected>>", watermark.choose_size)
font_combo_size.grid(row=6, column=3, pady=5, padx=10, sticky="w")

# -------- Movimiento ---------
button_top = tkinter.Button(text="⬆", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                            command=lambda movement="Up": watermark.move_top_botton_button(movement))
button_top.grid(row=7, column=4, pady=5, padx=5, ipadx=5, ipady=3, sticky="s")

button_botton = tkinter.Button(text="⬇", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                               command=lambda movement="Down": watermark.move_top_botton_button(movement))
button_botton.grid(row=9, column=4, pady=5, padx=5, ipadx=5, ipady=3, sticky="n")

button_right = tkinter.Button(text="⮕", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                              command=lambda movement="Right": watermark.move_left_right_button(movement))
button_right.grid(row=8, column=5, pady=5, padx=5, ipadx=5, ipady=3, sticky="w")

button_left = tkinter.Button(text="⬅", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                             command=lambda movement="Left": watermark.move_left_right_button(movement))
button_left.grid(row=8, column=3, pady=5, padx=5, ipadx=5, ipady=3, sticky="e")

# -------- Movimiento mediante teclado ---------
window.bind("<KeyPress-Up>", watermark.move_top_botton)
window.bind("<KeyPress-Down>", watermark.move_top_botton)
window.bind("<KeyPress-Right>", watermark.move_left_right)
window.bind("<KeyPress-Left>", watermark.move_left_right)

# -------- Rotación ---------
button_rotate = tkinter.Button(text="↺", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                               command=watermark.rotate_right)
button_rotate.grid(row=9, column=2, ipadx=5, ipady=3, sticky="e")

button_rotate = tkinter.Button(text="↻", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                               command=watermark.rotate_left)
button_rotate.grid(row=9, column=3, ipadx=5, ipady=3, sticky="w")


# -------- Guarda la imagen ---------
button_save = tkinter.Button(window, text="Save", background=BUTTON_BACKGROUND, foreground=LABEL_FOREGROUND,
                             command=lambda: watermark.save())
button_save.grid(row=16, column=7, pady=5, padx=10, ipadx=5, sticky="e")


window.mainloop()
