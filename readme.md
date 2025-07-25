# Сборка
```shell
pyinstaller --noconfirm --onefile --windowed --add-data "Z:\Python\Projects\dialog_mortal_combat\textures;./textures/" --add-data "Z:\Python\Projects\dialog_mortal_combat\fonts;./fonts/"  "Z:\Python\Projects\dialog_mortal_combat\main.py"

```

### ВНИМАНИЕ! При сборке с ресурсами (картинки/звуки/шрифты) не забываем про _MEIPASS (см. utils.py)

- При использовании шрифтов в Pygame, указываем путь до файла с шрифтом, иначе после сборки упадет.