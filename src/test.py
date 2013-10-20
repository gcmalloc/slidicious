#!/usr/bin/env python
import shutil
import task
import app
import unittest

class AppTest(unittest.TestCase):

    """Test case template""
    def __init__(self, arg):
    """
    def setUp(self):
        #self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        #flaskr.app.config['TESTING'] = True
        self.app = app.app.test_client()
        #flaskr.init_db()

    def test_(self):
        resp = self.app.post('/hook', data={'repository':'google.ch'})
	self.assertEqual(resp.status_code, 200)

    def test_root(self):
        resp = self.app.get('/', {})
	self.assertEqual(resp.status_code, 200)


class TestSlideBuild(unittest.TestCase):

    def test_pdf(self):
        ret = task.compile_slides("https://github.com/gcmalloc/fabric_presentation.git", build_index=555)
        self.tmp_dir = ret.output_dir
        self.assertIsInstance(ret, task.CompilationOutput)
        self.assertEqual(ret.html, '555.html')
        self.assertEqual(ret.pdf, '555.pdf')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
