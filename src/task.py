import tempfile
import logging
import os
from sh import pandoc, git
import glob
import shutil
from collections import namedtuple
from celery import Celery

CompilationOutput = namedtuple("task", ['output_dir', 'html', 'pdf'])

class FailedCompilation():
    pass

celery = Celery('task', broker=os.environ.get('CLOUDAMQP_URL', 'redis://127.0.0.1'))

@celery.task()
def compile_slides(git_repo, base_path):
    """
    """
    work_dir = tempfile.mkdtemp()
    logging.debug("will work in {}".format(work_dir))

    pd = Pandoc(work_dir)
    git.clone(git_repo, '.', _cwd=work_dir)
    in_file = find_markdown(work_dir)
    #ensure that the directory exists
    base_dir = os.path.dirname(base_path)
    try:
        os.makedirs(base_dir)
    except OSError:
        logging.warn("directory {} already exists".format(base_dir))

    html_out = str(base_path) + ".html"
    pdf_out = str(base_path) + ".pdf"

    try:
        logging.debug("compiling the html output")
        logging.debug(html_out)
        pd.compile_html(in_file, html_out)
    except Exception as e:
        logging.error("compilation fail for html")
        logging.error(str(e))

    try:
        logging.debug("compiling the pdf output")
        logging.debug(pdf_out)
        pd.compile_pdf(in_file, pdf_out)
    except Exception as e:
        logging.error("compilation fail for pdf")
        logging.error(str(e))

    logging.debug("Cleaning working directory")
    shutil.rmtree(work_dir)


def find_markdown(cwd):
    md_glob = os.path.join(cwd, '*.md')
    files = glob.glob(md_glob)
    for file in files:
        if not "README" in file:
            return file


class Pandoc:

    def __init__(self, cwd):
        self.cwd = cwd

    def compile_html(self, in_file, out_file):
        pandoc('--section-divs', '-r', 'markdown', in_file, '-t', 'html5', '-o', out_file, _cwd=self.cwd)
        #res = pandoc(in_file, out_file, _cwd=self.cwd)

    def compile_pdf(self, in_file, out_file):
        # pandoc -r markdown slides.md -t beamer -o out.pdf --slide-level=3 --toc --highlight-style=tango
        pandoc('-r', 'markdown', in_file, '-t', 'beamer', '-o', out_file, _cwd=self.cwd)
