import os
import os.path as op
import psutil
import logging
import tempfile
import shutil
import pytest
import datapkg

logger = logging.getLogger(__name__)


def setup_module():
    tempdir = op.join(op.splitext(__file__)[0], 'tmp')
    os.makedirs(tempdir, exist_ok=True)
    tempfile.tempdir = tempdir


def teardown_module():
    shutil.rmtree(tempfile.gettempdir())


def test_start_mysql():
    datadir = op.join(tempfile.gettempdir(), 'mysql_db')
    os.makedirs(datadir, exist_ok=True)
    # Start
    mysqld = datapkg.MySQLDaemon(datadir=datadir)
    mysqld.install_db()
    mysqld.start()
    assert mysqld._mysqld_process is not None
    pid = mysqld._mysqld_process.pid
    logger.debug("Process id: {}, status: {}".format(pid, psutil.Process(pid).status()))
    # Stop
    mysqld.stop()
    assert mysqld._mysqld_process is None
    with pytest.raises(psutil.NoSuchProcess):
        psutil.Process(pid)