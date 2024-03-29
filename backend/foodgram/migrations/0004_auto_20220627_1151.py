# Generated by Django 2.2.19 on 2022-06-27 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodgram', '0003_auto_20220627_1100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoriterecipe',
            options={'ordering': ('-updated_at',), 'verbose_name': 'Список избранного', 'verbose_name_plural': 'Списки избранного'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',), 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-updated_at',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ('-updated_at',), 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ('name',), 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
    ]
