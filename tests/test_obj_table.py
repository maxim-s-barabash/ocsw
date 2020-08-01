import unittest
from datetime import datetime

from ocsw.utils.table import ObjTable


class TestObjTable(unittest.TestCase):

    @unittest.skip("local time")
    def test_table_common(self):

        columns = [
            dict(field="id", title="ID", width=5),
            dict(field="name", title="NAME"),
            dict(
                field="creationDate",
                title="CREATION DATE",
                render=lambda d, c: datetime.fromtimestamp(d[c["field"]]),
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
            "                 05:40:00           \n"
            "2       Name 2   2014-05-13       no\n"
            "                 19:53:20           \n"
            "3       Name 3   2008-01-10       no\n"
            "                 23:20:00           "
        )
        self.assertEqual(str(table), snapshot)


if __name__ == "__main__":
    unittest.main()
