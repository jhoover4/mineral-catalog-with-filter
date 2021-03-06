# Generated by Django 2.0.3 on 2018-03-31 18:15
import json
import os
import re

from django.db import migrations


def save_categories(apps, data):
    Category = apps.get_model('mineral_detail', 'Category')

    split_pattern = re.compile(r'and|,(?:\W)?', re.IGNORECASE)

    category_ids = []

    for category_name in re.split(split_pattern, data['category']):
        name = str.strip(category_name).capitalize()

        try:
            get_category = Category.objects.get(name=name)
        except Category.DoesNotExist:
            if name:
                get_category = Category.objects.create(name=name)
            else:
                try:
                    get_category = Category.objects.get(name='None')
                except Category.DoesNotExist:
                    get_category = Category.objects.create()
            get_category.save()

        category_ids.append(get_category.pk)

    return category_ids


def read_json(apps, schema_editor):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    json_file = parent_dir + "/minerals.json"

    data = json.load(open(json_file))

    Mineral = apps.get_model('mineral_detail', 'Mineral')
    Group = apps.get_model('mineral_detail', 'Group')
    for d in data:
        group_name = str.strip(d['group'])
        try:
            get_group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            get_group = Group.objects.create(name=group_name)
            get_group.save()

        category_ids = save_categories(apps, d)

        new_mineral = Mineral(
            name=d['name'],
            image_filename=d['image filename'],
            image_caption=d['image caption'],
            group=get_group,
        )

        if 'formula' in d:
            new_mineral.formula = d['formula']
        if 'strunz classification' in d:
            new_mineral.strunz = d['strunz classification']
        if 'crystal system' in d:
            new_mineral.crystal_system = d['crystal system']
        if 'unit cell' in d:
            new_mineral.unit_cell = d['unit cell']
        if 'color' in d:
            new_mineral.color = d['color']
        if 'crystal symmetry' in d:
            new_mineral.crystal_symmetry = d['crystal symmetry']
        if 'cleavage' in d:
            new_mineral.cleavage = d['cleavage']
        if 'mohs scale hardness' in d:
            new_mineral.mohs_scale = d['mohs scale hardness']
        if 'luster' in d:
            new_mineral.luster = d['luster']
        if 'streak' in d:
            new_mineral.streak = d['streak']
        if 'diaphaneity' in d:
            new_mineral.diaphaneity = d['diaphaneity']
        if 'optical_prop' in d:
            new_mineral.optical_prop = d['optical properties']

        new_mineral.save()
        new_mineral.categories.add(*category_ids)


class Migration(migrations.Migration):
    dependencies = [
        ('mineral_detail', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(read_json),
    ]
