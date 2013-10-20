import tempfile
import logging
import os
from sh import pandoc, git
import glob
from collections import namedtuple
from celery import task

CompilationOutput = namedtuple("compilation_result", ['output_dir', 'html', 'pdf'])

class FailedCompilation():
    pass

@task()
def compile_slides(git_repo, build_index=0):
    """
    """
    work_dir = tempfile.mkdtemp()

    pd = Pandoc(work_dir)
    git.clone(git_repo, '.', _cwd=work_dir)
    in_file = find_markdown(work_dir)

    html_out = str(build_index) + ".html"
    pdf_out = str(build_index) + ".pdf"
    try:
        pd.compile_html(in_file, html_out)
    except:
        logging.error("compilation fail for html")

    try:
        pd.compile_pdf(in_file, pdf_out)
    except:
        logging.error("compilation fail for pdf")

    return CompilationOutput(work_dir, html_out, pdf_out, )

def find_markdown(cwd):
    md_glob = os.path.join(cwd, '*.md')
    files = glob.glob(md_glob)
    return files[0]


class Pandoc:

    def __init__(self, cwd):
        self.cwd = cwd

    def compile_html(self, in_file, out_file):
        pandoc('--section-divs', '-r', 'markdown', in_file, '-t', 'html5', '-o', out_file, _cwd=self.cwd)
        #res = pandoc(in_file, out_file, _cwd=self.cwd)

    def compile_pdf(self, in_file, out_file):
        # pandoc -r markdown slides.md -t beamer -o out.pdf --slide-level=3 --toc --highlight-style=tango
        pandoc('-r', 'markdown', in_file, '-t', 'beamer', '-o', out_file, _cwd=self.cwd)
