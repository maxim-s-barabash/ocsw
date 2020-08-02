import unittest
from datetime import date, datetime

from ocsw.utils.table import ObjTable, PropTable


class TestObjTable(unittest.TestCase):
    def test_table_common(self):

        columns = [
            dict(field="id", title="ID", width=5),
            dict(field="name", title="NAME"),
            dict(
                field="creationDate",
                title="CREATION DATE",
                render=lambda d, c: datetime.utcfromtimestamp(d[c["field"]]),
                width=10,
            ),
            dict(
                field="synced",
                title="SYNCED",
                align=">",
                render=lambda d, c: "yes" if d[c["field"]] else "no",
            ),
        ]
        data = [
            dict(id=1, name="Name 1", creationDate=1500000000, synced=True),
            dict(id=2, name="Name 2", creationDate=1400000000, synced=False),
            dict(id=3, name="Name 3", creationDate=1200000000, synced=0),
        ]
        table = ObjTable(data=data, columns=columns)
        snapshot = (
            "ID      NAME     CREATION     SYNCED\n"
            "                 DATE               \n"
            "1       Name 1   2017-07-14      yes\n"
            "                 02:40:00           \n"
            "2       Name 2   2014-05-13       no\n"
            "                 16:53:20           \n"
            "3       Name 3   2008-01-10       no\n"
            "                 21:20:00           "
        )
        self.assertEqual(str(table), snapshot)

    def test_props_table_common(self):

        item = {"date": 1595577615.600, "model": "MODEL-1234"}
        props_row = [
            {"name": "date", "label": "Date", "render": date.fromtimestamp},
            {"name": "model", "label": "Model"},
        ]
        table = PropTable(item, props_row)
        snapshot = "Date    2020-07-24\nModel   MODEL-1234"
        self.assertEqual(str(table), snapshot)


if __name__ == "__main__":
    unittest.main()
