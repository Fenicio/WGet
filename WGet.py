import sublime
import sublime_plugin
import urllib
import threading
import urllib2
import html2text

class WGetApiCall(threading.Thread):
  def __init__(self, url, timeout):
    self.url = url
    self.timeout = timeout
    self.result = None
    threading.Thread.__init__(self)

  def run(self):
    try:
      request = urllib2.Request(self.url, None, headers={"User-Agent": "Sublime Text 2 WGet"})
      http_file = urllib2.urlopen(request, timeout=self.timeout)
      self.result = http_file.read()
      return
    except (urllib2.HTTPError) as (e):
      err = '%s: HTTP error %s WGet' % (__name__, str(e.code))
    except (urllib2.URLError) as (e):
      err = '%s: URL error %s WGet' % (__name__, str(e.reason))

    sublime.error_message(err)
    self.result = False

# La idea es que haga wget de una url, o curl, y que convierta lo recogido a codigo de texto
class WGetCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("URL to retrieve", "", self.run_wget_input,None,None)


  def run_wget_input(self,the_input):
    if the_input.startswith('http://') or the_input.startswith('https://'):
      pass
    else:
      the_input = 'http://' + the_input
    request = urllib2.Request(the_input, None, headers={"User-Agent": "Sublime Text 2 WGet"})
    http_file = urllib2.urlopen(request, timeout=10000)
    result = http_file.read()
    output_view = self.window.new_file()
    self.window.focus_view(output_view)
    edit = output_view.begin_edit('w_get', None)
    output_view.set_name('Wget: ' + the_input)
    output_view.insert(edit, 0, decode(result))
    output_view.end_edit(edit)


def decode(text):
  utfd = text.decode('utf-8')
  h = html2text.HTML2Text()
  return h.handle(utfd)

def wget(self, window_name, the_url):
  if the_url.startswith('http://') or the_url.startswith('https://'):
    pass
  else:
    the_url = 'http://' + the_url

  page_html = urllib.request.urlopen(the_url).read().decode('utf-8')
  h = html2text.HTML2Text()
  page_md = h.handle(page_html)

  output_view = self.window.new_file();
  self.window.focus_view(output_view)
  output_view.run_command("append", {"characters": page_md})
  output_view.set_name('Wget: ' + window_name)
  output_view.set_read_only(True)
  output_view.set_scratch(True)
