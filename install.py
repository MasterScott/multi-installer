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
		logv('[ERROR] %s is not supported.'%system)
	arch=machine()[0][-2:]
	with open(devnull,'wb') as NULL:
		if call([executable,'-m','pip'],stdout=NULL,stderr=NULL):
			logv('[INFO] PIP is not installed.')
			with NamedTemporaryFile() as file:
				file.write(urlopen('https://raw.githubusercontent.com/pypa/get-pip/master/get-pip.py').read())
				file.flush()
				logv('[INFO] Starting installation.')
				call([executable,file.name,'--user'])
		commands=[]
		if driver:
			call([executable,'-m','pip','install','wget','--user'])
			reload_modules()
			from wget import download
			if arch=='64':
				for i,browser in enumerate(['Google Chrome','Mozilla Firefox']):
					logv('%d) %s'%(i+1,browser))
			while True:
				choice=input('#? ') if arch=='64' else '2'
				if choice=='1' or choice=='2':
					if choice=='1':
						driver_version=urlopen('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').read().decode()
						if system=='Windows':
							file_link='https://chromedriver.storage.googleapis.com/%s/chromedriver_win32.zip'%driver_version
						elif system=='Linux':
							file_link='https://chromedriver.storage.googleapis.com/%s/chromedriver_linux64.zip'%driver_version
						else:
							file_link='https://chromedriver.storage.googleapis.com/%s/chromedriver_mac64.zip'%driver_version
					if choice=='2':
						driver_version='v0.24.0'
						if system=='Windows':
							file_link='https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-win{1}.zip'.format(driver_version,arch)
						elif system=='Linux':
							file_link='https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-linux{1}.tar.gz'.format(driver_version,arch)
						else:
							file_link='https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-macos.tar.gz'.format(driver_version)
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
						if choice=='1':
							call(['chmod','u+x',path_join(environ['HOME'],'.DeBos','drivers','chromedriver')])
						else:
							call(['chmod','u+x',path_join(environ['HOME'],'.DeBos','drivers','geckodriver')])
				else:continue
				break
		exit_code=call([executable,'-m','pip','install','-Ur','requirements.txt','--user'])
		if exit_code:exit(exit_code)

if __name__=='__main__':
	try:
		try:input=raw_input
		except NameError:pass
		logv('[INFO] Bot is not installed.')
		logv('[INFO] Starting installation.')
		install(argv[1])
		logv('[INFO] Successfully installed %s.'%argv[0])
		INSTALLED=True
		reload_modules()
		logv('[INFO] Starting bot.')
	except KeyboardInterrupt:exit(0)
	except:exit(1)
