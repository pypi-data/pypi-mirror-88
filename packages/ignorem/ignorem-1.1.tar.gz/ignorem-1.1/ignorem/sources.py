import re
from urllib.request import urlopen
from ignorem import config

_REPO_LIST = [
	"https://raw.githubusercontent.com/itsmaxymoo/ignorem/main/SOURCES"
]
_got_sources = False
_sources = []


def get_external_repos():
	external_repo = config.get("repos")
	if not isinstance(external_repo, list):
		config.store("repos", [])

	return external_repo


def _get_all_sources():
	global _got_sources
	global _sources
	global _REPO_LIST

	# Don't fetch sources if already did once per-program-execution
	if _got_sources:
		return _sources

	big_list = ""

	# Download each repo
	for r in _REPO_LIST + get_external_repos():
		try:
			with urlopen(r) as remote:
				big_list += "\n" + remote.read().decode("UTF-8")
		except:
			print("WARN: Repo unavailable: " + r)

	# Remove unnecessary newlines, split into array
	big_list = re.sub(r"^(?:[\t ]*(?:\r?\n|\r))+", "", big_list)
	big_list = big_list.splitlines()

	# Remove invalid source entries
	for s in big_list:
		if len(s.split(" ")) != 2:
			print("ERROR: Invalid source entry: " + s)
			big_list.remove(s)

	# Convert array of sources into dictionary
	_sources = {}
	for s in big_list:
		s = s.split(" ")
		_sources[s[0]] = s[1]
	_got_sources = True
	return _sources


def query():
	_get_all_sources()
	return sorted(list(_sources.keys()))


def fetch_ignore(name):
	_get_all_sources()

	if name not in _sources:
		return "# ERROR: gitignore \"" + name + "\" not found!"

	with urlopen(_sources[name]) as remote:
		return remote.read().decode("UTF-8")


def add_source(url):
	r = get_external_repos()

	if url not in r:
		r.append(url)

	config.store("repos", r)


def remove_source(url):
	r = get_external_repos()

	if url in r:
		r.remove(url)
		config.store("repos", r)
		return True

	return False
