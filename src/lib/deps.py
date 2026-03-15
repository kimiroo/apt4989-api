from lib.db import MDBManager
import os

# Load env var
MDB_PATH = os.environ.get('MDB_PATH', '')
MDB_PASSWORD = os.environ.get('MDB_PASSWORD', '')

# Create singleton instance
mdb_instance = MDBManager(MDB_PATH, MDB_PASSWORD)

# Dependency injection
def get_mdb():
    return mdb_instance