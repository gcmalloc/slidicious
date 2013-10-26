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
        with open("src/assets/github_hook.json") as f:
            self.github_hook_data = dict()
            self.github_hook_data['payload'] = f.read()

    def test_(self):
        resp = self.app.post('/hook', data=dict(self.github_hook_data))
	self.assertEqual(resp.status_code, 200)

    def test_root(self):
        resp = self.app.get('/')
	self.assertEqual(resp.status_code, 200)


class TestSlideBuild(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_template = os.path.join(self.temp_dir, "555")

    def test_pdf(self):
        task.compile_slides("https://github.com/gcmalloc/fabric_presentation.git", self.temp_template)
        generated_files = os.listdir(self.temp_dir)
        self.assertIn("555.html", generated_files)
        self.assertIn("555.pdf", generated_files)
        self.assertEqual(len(generated_files), 2)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
