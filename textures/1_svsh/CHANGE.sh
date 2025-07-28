#!/bin/bash

# Проверяем, установлен ли ImageMagick
if ! command -v convert &> /dev/null
then
  echo "ImageMagick не установлен. Пожалуйста, установите его (например, 'sudo apt install imagemagick')."
  exit 1
fi

# Задаем желаемую высоту
height=175

# Создаем временную директорию
temp_dir=$(mktemp -d)
if [ -z "$temp_dir" ]; then
  echo "Не удалось создать временную директорию."
  exit 1
fi

echo "Создана временная директория: $temp_dir"

# Перебираем все PNG-файлы в текущей директории
for file in *.png; do
  # Проверяем, что это действительно файл
  if [ -f "$file" ]; then
    # Получаем текущую ширину и высоту изображения
    width=$(identify -format "%w" "$file")
    original_height=$(identify -format "%h" "$file")

    # Вычисляем новую ширину, сохраняя пропорции
    new_width=$(echo "scale=4; $height * $width / $original_height" | bc)
    new_width=$(printf "%.0f" $new_width)  # Округляем до целого числа

    # Создаем имя выходного файла во временной директории
    temp_file="$temp_dir/${file%.png}_resized.png"

    # Изменяем размер изображения с помощью ImageMagick
    convert "$file" -resize "x${height}" "$temp_file"

    # Проверяем, успешно ли создался новый файл во временной директории
    if [ -f "$temp_file" ]; then
      echo "Изменен размер: $file -> $temp_file (Новая ширина: ${new_width}px, Новая высота: ${height}px)"

      # Перемещаем файл из временной директории в текущую
      mv "$temp_file" "${file%.png}_resized.png"

      # Проверяем, успешно ли перемещен файл
      if [ -f "${file%.png}_resized.png" ]; then
        # **УДАЛЯЕМ ОРИГИНАЛЬНЫЙ ФАЙЛ!  УБЕДИТЕСЬ, ЧТО ЭТО ТО, ЧЕГО ВЫ ХОТИТЕ!**
        rm "$file"
        echo "Удален оригинальный файл: $file"
      else
        echo "Ошибка при перемещении файла из временной директории: $temp_file"
      fi
    else
      echo "Ошибка при изменении размера файла: $file"
    fi
  fi
done

# Удаляем временную директорию
rm -rf "$temp_dir"
echo "Удалена временная директория: $temp_dir"

echo "Готово!"

