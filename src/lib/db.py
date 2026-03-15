import os
import shutil
import jpype
import jaydebeapi

# Configuration
MDB_SNAPSHOT = '/tmp/snapshot.mdb'
JAR_DIR = './lib'

jars = [f'{JAR_DIR}/{x}' for x in os.listdir(JAR_DIR) if x.endswith('.jar')]
jars.append('./ucanaccess.jar')

# Start JVM
if not jpype.isJVMStarted():
    # Force JVM encoding
    jpype.startJVM(
        jpype.getDefaultJVMPath(),
        '-Dfile.encoding=UTF-8',
        '-Duser.language=ko',
        '-Duser.country=KR',
        classpath=jars
    )

class MDBManager:
    """
    Manager for MDB access via Ucanaccess.
    Ensures safe snapshotting and clean connection handling.
    """
    def __init__(self, mdb_path: str, mdb_password: str):
        self._mdb_path = mdb_path
        self._mdb_pw = mdb_password
        self._last_mtime = 0
        self.conn = None

    def _sync_snapshot(self) -> bool:
        """Syncs the MDB file to a temporary snapshot if modified."""
        current_mtime = os.path.getmtime(self._mdb_path)

        if current_mtime > self._last_mtime:
            # Check if snapshot exists and remove it
            if os.path.exists(MDB_SNAPSHOT):
                os.remove(MDB_SNAPSHOT)

            # Copy with meta-data to keep track of changes
            shutil.copy2(self._mdb_path, MDB_SNAPSHOT)
            self._last_mtime = current_mtime
            return True
        return False

    def connect(self) -> jaydebeapi.Connection:
        """Establishes a connection to the snapshot MDB."""
        self._sync_snapshot()
        conn_str = (
            f"jdbc:ucanaccess://{MDB_SNAPSHOT};"
            f"password={self._mdb_pw};"
            "readonly=true;ignoreCase=true"
        )
        # Use empty list for jars if already handled by jpype.startJVM
        self.conn = jaydebeapi.connect(
            'net.ucanaccess.jdbc.UcanaccessDriver',
            conn_str,
            ['', '']
        )
        return self.conn

    def query(self, sql: str, params: tuple = ()) -> list:
        """Executes a query and returns results safely."""
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)

            if cursor.description is None:
                return []

            columns = [str(column[0]).strip() for column in cursor.description]
            results = []

            for row in cursor.fetchall():
                processed_row = [
                    str(v) if v is not None and "java.lang" in str(type(v)) else v
                    for v in row
                ]
                results.append(dict(zip(columns, processed_row)))

            return results
        finally:
            cursor.close()
            conn.close()