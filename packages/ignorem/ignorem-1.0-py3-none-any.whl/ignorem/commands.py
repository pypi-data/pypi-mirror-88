import ignorem
from ignorem.gitignore import GitIgnore, GitIgnoreManager
from ignorem import sources


def _command_help():
	# Command list tuple format : name, description, requires gitignore list?
	commands = [
		("help", "Displays this text.", False),
		("list", "Lists gitignores enabled in the .gitignore file.", False),
		("query", "Query all available gitignores.", False),
		("add", "Adds or updates the specificed gitignores to the .gitignore file.", True),
		("remove", "Removes the specificed gitignores from the .gitignore file.", True),
		("update", "Updates all installed gitignores.", False)
	]
	command_text = ""

	for c in commands:
		command_text += "\t" + c[0] + ("\t\t" if len(c[0]) < 4 else "\t") + ("*" if c[2] else "") + c[1] +"\n"
	command_text = command_text.rstrip()

	help_text = """{0} ({1}) version {2} by {3}

{4}
{5}

Usage:
\t{6} {{ help | list | list-all | add | remove | update }} [gitignores]...

Commands:
{7}
* = Requires gitignore argument(s)"""

	help_text = help_text.format(
		ignorem.PROGRAM_NAME,
		ignorem.PROGRAM_NAME_FULL,
		ignorem.PROGRAM_VERSION,
		ignorem.PROGRAM_AUTHOR,
		ignorem.PROGRAM_DESCRIPTION,
		ignorem.PROGRAM_URL,
		ignorem.PROGRAM_CMD,
		command_text
	)
	print(help_text.expandtabs(4))


def _command_list():
	g = GitIgnoreManager.read()
	installed = g.get_installed()
	if len(installed) > 0:
		print("Installed gitignore(s): " + ", ".join(installed))
	else:
		print("No ignorem installed gitignore(s) at: " + ignorem.gitignore.GITIGNORE_PATH)
		if g.is_has_loose_gitignore():
			print("(gitignore NOT empty!)")


def _command_query():
	available = sources.query()
	for s in available:
		print(s)


def _command_add(ignores):
	g = GitIgnoreManager.read()

	for i in ignores:
		if i in sources.query():
			g.add(i)
		else:
			ignores.remove(i)
			print("ERROR: No known gitignore: \"" + i + "\"!")

	if ignores:
		print("Installed gitignore(s): " + ", ".join(ignores))

	GitIgnoreManager.write(g)


def _command_remove(ignores):
	g = GitIgnoreManager.read()

	for i in ignores:
		if not g.remove(i):
			ignores.remove(i)
			print("ERROR: Gitignore \"" + i + "\" not installed!")

	if ignores:
		print("Removed gitignore(s): " + ", ".join(ignores))

	GitIgnoreManager.write(g)


def _command_update():
	g = GitIgnoreManager.read()

	GitIgnoreManager.write(g)

	print("Updated gitignore(s).")
