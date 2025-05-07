import os, sys, time, logging, getpass, markdown, re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

# pip install git+https://github.com/mitya57/python-markdown-math.git

def get_meta_data(md_text):
	with open(md_text, "r") as file:
		raw_lines = file.readlines()

	if len(raw_lines) < 3:
		print("Not Enough Data! \n")
		return "NULL", "NULL"
	else:
		title = raw_lines[0].split(" ")[1].split("\n")[0]
		create_time = raw_lines[2].split(": ")[1].split("\n")[0]
		print(title + "\n")
		print(create_time)
		return title, create_time

def path_builder(filename, path_to_observe, dest_path, stub_path):
	# markdown.markdownFromFile(input='./Transphobia.md', output="bing.html")
	root, ext = os.path.splitext(filename)
	new_html_file = root + ".html"
	
	src_file = os.path.join(path_to_observe, filename)
	dest_file = os.path.join(dest_path, new_html_file)
	stub_file = os.path.join(stub_path, new_html_file)

	return src_file, dest_file, stub_file

def convert_to_html(src_file, converted_file):
	with open(src_file, "r") as input_md:
		html = markdown.markdown(input_md.read(), extensions=['mdx_math', 'footnotes'],)
		print("Md file opened \n")

	# our stub.html will have the title-card with the meta-data
	# we don't need to add the title and "Created on:" to our content.html
	html = "\n".join(html.split("\n")[2:])
	# # get the latest file modified time
	# time_modified_raw = os.path.getmtime(src_file) #
	
	# # create html to be used in the blog-post
	# edit_stamp = "<h4> Last Modified on " + time.ctime(time_modified_raw) +  " </h4>"
	
	# # place it in the correct place 
	# index = html.find("</h1>")
	# html = html[:index + len("</h1>")] + edit_stamp + html[index + len("</h1>"):]

	# as the <script type="math/tex; mode=display"> ... </scrip> isn't being rendered by MathJax
	html = html.replace('<script type="math/tex; mode=display">', '$$')
	html = html.replace('</script>', '$$')

	with open(converted_file, "w") as output_file:
		output_file.write(html)
		
	print("Html file updated !! \n")

def create_html_stub(path_to_stub_template, path_to_new_stub_file, md_file):
	with open(path_to_stub_template, "r") as file:
		html_template_content = file.read()
	
	print("Stub read! \n")
	
	title, create_time = get_meta_data(md_file)

	if title == "NULL" and create_time == "NULL":
		print("No meta-data found!")
		return None 
	else:
		print("title and create_time extracted! \n")

		html_template_content = re.sub(
			r'(title:\s*")[^"]*(")',
			rf'\1{title}\2',
			html_template_content
		)
		html_template_content = html_template_content.replace("PYTHON_CREATE_TIME", "\"" + create_time + "\"")
		
		with open(path_to_new_stub_file, "w") as file:
			file.write(html_template_content)

		print("Stub created! \n")

def modify_html_stub(path_to_old_stub_file, mod_time):
	with open(path_to_old_stub_file, "r") as file:
		old_stub = file.read()

	formatted_mod_time = time.strftime("%B %d, %Y %I:%M %p", time.localtime(mod_time))
	print(formatted_mod_time)
	
	old_stub = re.sub(
			r'(modified_on:\s*")[^"]*(")',
			rf'\1{formatted_mod_time}\2',
			old_stub
		)
    
	with open(path_to_old_stub_file, "w") as file:
		file.write(old_stub)

	print("Stub modified! \n")

class myHandler(FileSystemEventHandler):
	print("Handler called \n")
	
	def on_created(self, event):	
		print("On_create Called \n")
		for filename in os.listdir(path_to_observe):
			if filename.endswith('.md'):
				src, dest, stub_file = path_builder(filename, path_to_observe, dest_path, stub_path)
				if not os.path.isfile(dest):
					print(f"Target file does not exist so we will create it: {dest} \n")
					open(dest, "x")
					convert_to_html(src, dest)
				if not os.path.isfile(stub_file):
					print(f"We will also create the stub_file: {stub_file} \n")
					create_html_stub(stub_template, stub_file, src)

	def on_modified(self, event):
		print("On_modified Called \n")
		# markdown.markdownFromFile(input='./Transphobia.md', output="bing.html")
		for filename in os.listdir(path_to_observe):
			if filename.endswith('.md'):
				src, dest, stub_file = path_builder(filename, path_to_observe, dest_path, stub_path)

				if not os.path.isfile(dest):
					print(f"Target file does not exist so we will create it: {dest} \n")
					open(dest, "x")
					convert_to_html(src, dest)
				
				if not os.path.isfile(stub_file):
					print(f"We will also create the stub_file: {stub_file} \n")
					create_html_stub(stub_template, stub_file, src)
				
				if os.path.getmtime(src) > os.path.getmtime(dest):
					print(f"Source: {src} \n")
					print(f"Destination: {dest} \n")
					print(f"{src} is getting converted!")
					convert_to_html(src, dest)
					print(f"Now the {stub_file} is getting modified! \n")
					modify_html_stub(stub_file, os.path.getmtime(src))
				else:
					print(f"{src} has already been converted and up-to-date in {dest} \n")


if __name__ == '__main__':

	# take path from console or run in current working directory
	if len(sys.argv) == 4:
		path_to_observe = sys.argv[1]
		dest_path = sys.argv[2]
		stub_path = sys.argv[3]
	else:
		raise ValueError("Incorrect number of arguements. Usage: w2c.py <path_to_observe> <path_for_generated_html> <path_for_html_stub>")

	stub_template = "../r-log/assets/templates/stub-for-blog-posts.html"

	userid = getpass.getuser()

	# logging.DEBUG (DEBUG is just a "const int") is different from logging.debug (method)
	logging.basicConfig(filename="activity.log", filemode="a", 
						level=logging.INFO, 
						format='%(asctime)s - %(process)d - ' + f'{userid} -' + ' %(message)s', 
						datefmt='%Y-%m-%d %H:%M:%S')	


	log_handler_instance = LoggingEventHandler()
	event_handler_instance = myHandler()				# instantiate event handler
	observer_instance = Observer()					# instantiate observor
	
	# setup observor
	observer_instance.schedule(event_handler_instance, path_to_observe, recursive= True)
	observer_instance.start()	# start new thread then run() observor
	print("Observor has started in it's own thread \n")

	try:
		while True:
			time.sleep(1)
			print("\n Waiting for a sec")
	except KeyboardInterrupt:
		print("\nKeyboard interrupt! Cleaning up before exiting.")
		observer_instance.stop()
		observer_instance.join()
	finally:
		print("Exiting the program.")


# Logging levels

# DEBUG: detailed information, typically of interest only when diagnosing problems

# INFO: confirmation that things are working as expected

# WARNING[default]: an indication that something unexpected happened, or indicative of some problem in the future (e.g. 'disk space low'). The software is still working as expected.

# ERROR: due to a more serious problem, the software has not been able to perform some function

# CRITICAL: a serious error, indicating that the program itself may be unable to continue running	
