from typing import Dict, List, Union

import xlrd
from django.core.management.base import BaseCommand

from apps.marketplace.models import Category

FILE_PATH = './apps/marketplace/initial_data/google_categories.xls'


def parse_from_xls(path: str) -> List[Dict[str, Union[str, None]]]:
    """Parse from `.xls` file to list of dicts.

    Where key is child category name and value is parent category name.

    Args:
        path (str): Path to `.xls` file.

    Returns:
        list: List of dicts.
    """
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    relations = []
    for row_num in range(0, sh.nrows):
        row_values = sh.row_values(row_num)
        row_values = list(filter(lambda value: value != '', row_values))
        child = row_values[-1]
        parent = row_values[-2]
        if isinstance(parent, float):
            parent = None
        child_parent_relation = {child: parent}
        relations.append(child_parent_relation)
    return relations


def fill_in_db(relations: List[Dict[str, Union[str, None]]]):
    """Create Category objects and save it to db."""
    for relation in relations:
        for child_name, parent_name in relation.items():
            parent = None
            if parent_name:
                parent, _ = Category.objects.get_or_create(
                    name=parent_name,
                    defaults={'lft': 0, 'rght': 0, 'level': 0, 'tree_id': 0},
                )
            Category.objects.get_or_create(
                name=child_name,
                parent=parent,
                defaults={'lft': 0, 'rght': 0, 'level': 0, 'tree_id': 0},
            )


class Command(BaseCommand):
    help = 'Parse categories from `.xlsx` to database'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--path', type=str, default=FILE_PATH)

    def handle(self, *args, **options):
        path = options['path']
        relations = parse_from_xls(path)
        fill_in_db(relations)
        Category.objects.rebuild()
