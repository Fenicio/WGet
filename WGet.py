import sublime
import sublime_plugin
import urllib
import threading
import urllib2
import html2text
import encodings.idna
import unicodedata

class WGetApiCall(threading.Thread):
  def __init__(self, sel, url):
    self.sel = sel
    self.url = url
    threading.Thread.__init__(self)

  def run(self):
    wget(self.sel, self.url)

# La idea es que haga wget de una url, o curl, y que convierta lo recogido a codigo de texto
class WGetCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("URL to retrieve", "", self.run_wget_input,None,None)

  def run_wget_input(self,input):
    deunicoded = input.encode('ascii','ignore')
    wget_async(self, deunicoded)


def decode(text):
  utfd = text.decode('utf-8')
  h = html2text.HTML2Text()
  try :
    return h.handle(utfd)
  except:
    return utfd

def wget(self, input):
  if input.startswith('http://') or input.startswith('https://'):
    pass
  else:
    input = 'http://' + input
  request = urllib2.Request(input, None, headers={"User-Agent": "Sublime Text 2 WGet"})
  http_file = urllib2.urlopen(request, timeout=16000)
  result = http_file.read()
  output_view = self.window.new_file()
  self.window.focus_view(output_view)
  edit = output_view.begin_edit('w_get', None)
  output_view.set_name('Wget: ' + input)
  output_view.insert(edit, 0, decode(result))
  output_view.end_edit(edit)


def wget_async(self, url):
#  thread = WGetApiCall(self, url)
#  thread.start()
  sublime.set_timeout(lambda: wget(self, url), 0)
