from os import remove,devnull
from os.path import join as path_join
from sys import executable
from zipfile import ZipFile
from tempfile import NamedTemporaryFile
from platform import machine,system as get_system
from subprocess import call

def reload_modules():
	try:from importlib import reload
	except:from imp import reload
	import site
	reload(site)
def install(driver):
	system=get_system()
	if system not in ['Windows','Linux','Darwin']:
		print('[ERROR] %s is not supported.'%system)
	arch=machine()[-2:].replace('86','32')
	print('[INFO] Detected %sbit architecture'%arch)
	with open(devnull,'wb') as NULL:
		if call([executable,'-m','pip'],stdout=NULL,stderr=NULL):
			print('[INFO] PIP is not installed.')
			with NamedTemporaryFile() as file:
				file.write(urlopen('https://raw.githubusercontent.com/pypa/get-pip/master/get-pip.py').read())
				file.flush()
				print('[INFO] Starting installation.')
				call([executable,file.name,'--user'])
		commands=[]
		print('[INFO] Starting driver installation.')
		if driver:
			call([executable,'-m','pip','install','wget','--user'])
			reload_modules()
			from wget import download
			print('Select browser for webdriver:')
			if arch=='64':
				for i,browser in enumerate(['Google Chrome','Mozilla Firefox','All']):
					print('%d) %s'%(i+1,browser))
			while True:
				choice=input('#? ') if arch=='64' else '2'
				if choice in [str(x+1) for x in range(3)]:
					files_links=[]
					if choice=='1' or choice=='3':
						driver_version=urlopen('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').read().decode()
						if system=='Windows':
							files_links.append('https://chromedriver.storage.googleapis.com/%s/chromedriver_win32.zip'%driver_version)
						elif system=='Linux':
							files_links.append('https://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip'%driver_version)
						else:
							files_links.append('https://chromedriver.storage.googleapis.com/%s/chromedriver_mac64.zip'%driver_version)
					if choice=='2' or choice=='3':
						driver_version='v0.25.0'
						if system=='Windows':
							files_links.append('https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-win{1}.zip'.format(driver_version,arch))
						elif system=='Linux':
							files_links.append('https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-linux{1}.tar.gz'.format(driver_version,arch))
						else:
							files_links.append('https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-macos.tar.gz'.format(driver_version))
					for file_link in files_links:
						print('[INFO] Downloading webdriver from: %s'%file_link)
						download(file_link)
						filename=file_link.split('/')[-1]
						if filename.endswith('.zip'):
							from zipfile import ZipFile
							open_archive=ZipFile
						else:
							from tarfile import TarFile
							open_archive=TarFile.open
						with open_archive(filename) as file:
							if system=='Windows':
								file.extractall(path_join(environ['APPDATA'],'DeBos','drivers'))
							else:
								file.extractall(path_join(environ['HOME'],'.DeBos','drivers'))
						remove(filename)
						if system!='Windows':
							call(['chmod','u+x',path_join(environ['HOME'],'.DeBos','drivers','*driver')])
				else:continue
				break
		exit_code=call([executable,'-m','pip','install','-Ur','requirements.txt','--user'])
		if exit_code:exit(exit_code)

if __name__=='__main__':
	try:
		try:input=raw_input
		except NameError:pass
		print('[INFO] Bot is not installed.')
		print('[INFO] Starting installation.')
		install(argv[1])
		print('[INFO] Successfully installed %s.'%argv[0])
		INSTALLED=True
		reload_modules()
		print('[INFO] Starting bot.')
	except KeyboardInterrupt:exit(0)
	except:exit(1)
