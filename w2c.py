import os, sys, time, logging, getpass, markdown
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler

# pip install git+https://github.com/mitya57/python-markdown-math.git

class myHandler(FileSystemEventHandler):
	print("Handler called \n")
	def on_modified(self, event):
		print("On_modified Called \n")
		dest_path = "./DESTFOLDER"
		# markdown.markdownFromFile(input='./Transphobia.md', output="bing.html")
		for filename in os.listdir(path_to_observe):
			if filename.endswith('.md'):
				root, ext = os.path.splitext(filename)
				new_html_file = root + ".html"
				
				src = os.path.join(path_to_observe, filename)
				dest = os.path.join(dest_path, new_html_file)

				print(f"Source: {src} \n")
				print(f"Destination: {dest} \n")

				with open(src, "r") as input_md:
					html = markdown.markdown(input_md.read(), 
											extensions=['mdx_math', 'footnotes'],
											)
					print("Md file opened \n")
				time_modified_raw = os.path.getmtime(src)
				edit_stamp = "<h4> Last Modified on " + time.ctime(time_modified_raw) +  " </h4>"
				index = html.find("</h1>")
				html = html[:index + len("</h 1>")] + edit_stamp + html[index + len("</h1>"):]

				# as the <script type="math/tex; mode=display"> ... </scrip> isn't being rendered by MathJax
				html = html.replace('<script type="math/tex; mode=display">', '$$')
				html = html.replace('</script>', '$$')

				with open(dest, "w") as output_file:
					output_file.write(html)
					print("Html file written \n")

				print("Task done!")


if __name__ == '__main__':

	userid = getpass.getuser()

	# logging.DEBUG (DEBUG is just a "const int") is different from logging.debug (method)
	logging.basicConfig(filename="activity.log", filemode="a", 
						level=logging.INFO, 
						format='%(asctime)s - %(process)d - ' + f'{userid} -' + ' %(message)s', 
						datefmt='%Y-%m-%d %H:%M:%S')	

	# take path from console or run in current working directory
	if len(sys.argv) > 1:
		path_to_observe = sys.argv[1]
	else: 
		path_to_observe = '.'	
	# print(path_to_observe)

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
