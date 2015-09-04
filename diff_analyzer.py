__author__ = 'DeysAdmin'

import os
import markup

CSS_B_RED = "<b class=\"red\">"
CSS_B_GREEN = "<b class=\"green\">"
CSS_B_END = "</b>"
CSS_DIV_CHANGES = "<div class=\"changes\">"
CSS_DIV_END = "</div>"
CSS_PRE = "<pre class=\"prettyprint\">"
CSS_PRE_END = "</pre>"


def diff_parser():
	files = []				# has list of file_changes
	file_changes = []		# has list of change
	# file_name = ""
	# change = dict()				# has left and right
	left = ""
	right = ""
	for line in open(os.getcwd()+"\\changes.diff"):
		''' the line comes with the new line char (\n) at the end'''
		if line.startswith("diff --git"):
			# should get executed when a new file is encountered in diff log
			if (left is not "") and (right is not ""):		# if there are changes then conclude it
				#----Conclude Change--------------#
				left += CSS_PRE_END
				right += CSS_PRE_END
				change = dict()
				change['left'] = left
				change['right'] = right
				file_changes.append(change)
				#---------------------------------#
				files.append(file_changes)
				# once stored into the files then clear varibles lower than files
				file_changes = []
				# change = {}
				left = ""
				right = ""

		elif line.startswith("@@ "):
			# store the old changes when a new change is encountered
			if (left is not "") and (right is not ""):
				#----Conclude Change--------------#
				left += CSS_PRE_END
				right += CSS_PRE_END
				change = dict()
				change['left'] = left
				change['right'] = right
				file_changes.append(change)
				#---------------------------------#

			# initialize the left and right (clear)
			left = ""
			right = ""
			left += CSS_PRE
			right += CSS_PRE
			left += line
			right += line
		elif line.startswith("---") or line.startswith("+++") or line.startswith("index ") or line.startswith("\\ No newline at end of file") or line.startswith("new file mode") or line.startswith("deleted file mode"):
			# do not store anything for the above cases
			if line.startswith("--- a/") or line.startswith("+++ b/"):
				# logic to store the file name
				file_name = line.rstrip().split("/", 1)[1]
				file_changes.append(file_name)
		elif line.startswith("-"):
			# removing the new line char, will be added after css ends
			line = line.rstrip("\n")
			# replacing the single - with space (not blank), in order to preserve indentation
			line = line.replace("-", " ", 1)
			# replacing the single - with space (not blank), in order to preserve indentation
			right += CSS_B_RED + line + CSS_B_END + "\n"
		elif line.startswith("+"):
			line = line.rstrip("\n")
			# replacing the single - with space (not blank), in order to preserve indentation
			line = line.replace("+", " ", 1)
			left += CSS_B_GREEN + line + CSS_B_END + "\n"
		else:
			left += line
			right += line

	#----Conclude Change--------------#
	left += CSS_PRE_END
	right += CSS_PRE_END
	# create new dict
	change = dict()
	change['left'] = left
	change['right'] = right
	file_changes.append(change)
	#---------------------------------#
	files.append(file_changes)
	return files

def raw_display(files):
	for file in files:
		for change in file:
			print "LEFT"
			print change['left']
			print "RIGHT"
			print change['right']


def create_html_diff(files):
	"""
	"""
	p = markup.page()
	p.html.open()
	p.script(src='https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js')
	p.script.close()
	p.style(inline_css)
	p.body.open()
	p.h1("Diff Viewer")
	p.div.open(class_='outer center')
	for file_changes in files:
		p.h3(file_changes[0])
		p.table.open(class_="center")
		p.tr.open()
		p.th(("Current", "Old"), class_="test")
		p.tr.close()
		for change in file_changes:
			if type(change) == dict:
				p.tr.open()
				p.td((change['left'], change['right']))
				p.tr.close()
		p.table.close()
	p.div.close()
	p.body.close()
	fl = open(os.getcwd()+"\\diffs.html", "w+")
	fl.write(str(p))
	print "Generated diffs.html in the current folder."
	fl.close()


inline_css = """
body {
    background-color: white;
    font-family: sans-serif;
}
b.red {color: black;
background-color: #FFABAB;
}
b.green {color: black;
background-color: #85ce9d;
}
.changes {
	margin: 10px;
	background-color: #EFF3F7;
    padding: 5px;
    width: 440px;
    overflow: auto;
}
.outer {
    background-color: #D7D7E3;
    border: 2px solid black;
    width: 98%;
    padding-bottom: 20px;   
}
.center {
    margin-left: auto;
    margin-right: auto;
}
table { border: 1px solid black;
    border-collapse: collapse;
    table-layout: fixed;
    width: 98%;
}

th {
    background-color: #5C5CE6;
    color: white;
}
td, th {border: 1px solid black;
vertical-align: top;
}
h3 {
    padding: 10px;
    margin: 20px 0px 0px 0px;
}
h1 {
    text-align: center;
}

pre {
    overflow-x: auto; 
    background-color: #FCFDFE;
    margin: 1px;
}
"""

if __name__ == '__main__':
	files = diff_parser()
	create_html_diff(files)




"""
diff --git a/hooks.txt b/hooks.txt
index 15b2ff6..a55bdc2 100644
--- a/hooks.txt
+++ b/hooks.txt
@@ -395,6 +395,8 @@ class HookManager(object):
     '''
     #Registers the given function as the callback for this mouse event type. Use the
     #MouseLeftDbl property as a shortcut.
+    also clicks
+    also fsdf

     @param func: Callback function
     @type func: callable
@@ -423,7 +425,6 @@ class HookManager(object):
     MouseRightDown property as a shortcut.

     @param func: Callback function
-    @type func: callable
     '''
     if func is None:
       self.disconnect(self.mouse_funcs, HookConstants.WM_RBUTTONDOWN)
"""