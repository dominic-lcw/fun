"""
    duckdb.py
    =============

    This provides a user interface for duckdb.
    It also serves as syntax reminder.

"""
import duckdb

class DuckDB:

    def __init__(self, db: str = ":memory:"):
        self.db = duckdb.connect(db)

    def sql(self, query: str):
        return self.db.sql(query)

    # region: S3 Methods
    @property
    def s3_parse(self):
        """ Parse for S3 Credentials """
        pass

    def get(self, bucket: str, path: str, table: str):
        """ Get data from S3 """
        pass

    def put(self, table:str, bucket: str, path: str):
        """ Put data to S3 """
        pass
    # endregion


class Duck(DuckDB):
    """ Alias for DuckDB """
    pass