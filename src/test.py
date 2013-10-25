#!/usr/bin/env python
import os
import shutil
import task
import app
import unittest
import tempfile

class AppTest(unittest.TestCase):

    """Test case template""
    def __init__(self, arg):
    """
    def setUp(self):
        self.app = app.app.test_client()

    def test_(self):
        resp = self.app.post('/hook', data={'repository':'google.ch'})
	self.assertEqual(resp.status_code, 200)

    def test_root(self):
        resp = self.app.get('/', payload={'payload':{}})
	self.assertEqual(resp.status_code, 400)


class TestSlideBuild(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_template = os.path.join(self.temp_dir, "555")

    def test_pdf(self):
        ret = task.compile_slides("https://github.com/gcmalloc/fabric_presentation.git", self.temp_dir)
        self.tmp_dir = ret.output_dir
        self.assertIsInstance(ret, task.CompilationOutput)
        self.assertEqual(ret.html, '555.html')
        self.assertEqual(ret.pdf, '555.pdf')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
