import random
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from faker import Faker
from PIL import Image

# Регистрация шрифта Times New Roman
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))
pdfmetrics.registerFont(TTFont('Times-Bold', 'timesbd.ttf'))

# Создание PDF-документа
c = canvas.Canvas("output.pdf", pagesize=A4)

# Настройки для выравнивания текста и рамки
width, height = A4
margin = 0.7 * cm  # Уменьшение отступа для размещения 8 пропусков на странице
box_width = (width - 3 * margin) / 2  # Ширина одного пропуска (с учётом промежутков)
box_height = (height - 5 * margin) / 4  # Высота одного пропуска (с учётом промежутков)

# Фейковые данные
fake = Faker()

# Загрузка и конвертация логотипа
logo_path = "logo.png"  # Замените на путь к вашему логотипу

# Открытие изображения с помощью PIL
logo_image = Image.open(logo_path)
# Создание белого фона
background = Image.new("RGB", logo_image.size, (255, 255, 255))
# Наложение логотипа на белый фон
background.paste(logo_image, mask=logo_image.split()[3])  # Использование альфа-канала как маски
# Сохранение конвертированного изображения
prelogo_path = "prelogo.png"
background.save(prelogo_path)

# Загрузка конвертированного логотипа
logo = ImageReader(prelogo_path)
logo_width = 2 * cm
logo_height = 2 * cm

for row in range(4):  # Четыре строки пропусков
    for col in range(2):  # Два столбца пропусков

        x0 = margin + col * (box_width + margin)
        y0 = height - margin - (row + 1) * box_height - row * margin

        # Рисование прямоугольника (рамка)
        c.rect(x0, y0, box_width, box_height)

        # Выравнивание текста по центру прямоугольника
        text_x = x0 + box_width / 2
        text_y = y0 + box_height - 2 * margin

        # Добавление логотипа в левый верхний угол
        c.drawImage(logo, x0 + margin / 2, y0 + box_height - logo_height - margin / 2, logo_width, logo_height)

        # Случайные данные для пропуска
        name = fake.name()
        date_time = fake.date_time_this_year().strftime("%d.%m.%y с %H:%M до 20:00")
        supervisor = f"Ст.воcп. {fake.name()}"

        # Текст в самом верху
        c.setFont('Times-Roman', 6)
        c.drawCentredString(text_x, y0 + box_height - margin / 2, "Общество с ограниченной ответственностью управляющая компания")
        c.drawCentredString(text_x, y0 + box_height - margin - 0.1 * cm, "«КРЫМ-ИНВЕСТ-ТУР»")
        c.drawCentredString(text_x, y0 + box_height - margin - 0.6 * cm, "Республика Крым, г.Евпатория, пгт.Заозёрное")
        c.drawCentredString(text_x, y0 + box_height - margin - 1.0 * cm, "Аллея дружбы 11 А")
        c.drawCentredString(text_x, y0 + box_height - margin - 1.5 * cm, "Детский оздоровительный лагерь «Парус»")

        text_lines = [
            "ПРОПУСК",
            name,
            date_time,
            supervisor
        ]

        text_y -= 3 * margin

        for i, line in enumerate(text_lines):
            if i == 0:
                c.setFont('Times-Bold', 16)  # Установка жирного шрифта для "ПРОПУСК"
            else:
                c.setFont('Times-Roman', 10)  # Установка обычного шрифта для остальных строк
            c.drawCentredString(text_x, text_y, line)
            text_y -= margin  # Увеличение отступа между строками

            # Добавление линии под name, date_time и supervisor
            if i > 0:
                c.line(text_x - box_width / 4, text_y + margin / 1.5, text_x + box_width / 4, text_y + margin / 1.5)

# Закрытие и сохранение PDF-документа
c.save()
