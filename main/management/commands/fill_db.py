import csv
import os
from django.core.files import File
from django.core.management.base import BaseCommand

from main.constants import VOLUME_CHOICES
from main.models import Product


class Command(BaseCommand):
    help = 'Импортирует данные из CSV файлов'
    count = 0

    def handle(self, *args, **options):
        img_dir = 'fill_db/img/'
        
        with open('fill_db/products.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                number_of_product, image_filename, show, small_image_filename, volume, price, name = row
                
                try:
                    volume = int(volume)
                    if volume not in dict(VOLUME_CHOICES).keys():
                        print(f'Объём {volume} недопустим для продукта №{number_of_product}.')
                        continue

                    price = float(price)
                    if price <= 0:
                        print(f'Цена {price} должна быть положительной для продукта №{number_of_product}.')
                        continue

                    image_path = os.path.join(img_dir, image_filename)
                    small_image_path = os.path.join(img_dir, small_image_filename)

                    with open(image_path, 'rb') as image_file, open(small_image_path, 'rb') as small_image_file:
                        product, created = Product.objects.get_or_create(
                            number_of_product=number_of_product,
                            name=name,
                            defaults={
                                'show': show.lower() == 'true',
                                'volume': volume,
                                'price': price,
                            }
                        )
                        product.picture_of_product.save(image_filename, File(image_file))
                        product.picture_of_product_small.save(small_image_filename, File(small_image_file))

                        if created:
                            print(f'Продукт №{number_of_product} создан успешно.')
                        else:
                            print(f'Продукт №{number_of_product} уже существует и был обновлен.')

                except FileNotFoundError as e:
                    print(f'Изображение не найдено: {e}')
                except ValueError as e:
                    print(f'Ошибка в данных для продукта №{number_of_product}: {e}')
                except Exception as e:
                    print(f'Ошибка при обработке продукта №{number_of_product}: {e}')
