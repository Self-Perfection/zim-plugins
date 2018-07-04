# Copyright 2018 Alexander Meshcheryakov <alexander.s.m@gmail.com>
#
# Plugin to store note tags in file extended attributes.

import logging

logger = logging.getLogger('zim.plugins.xattr_tags')

from zim.plugins import PluginClass, ObjectExtension, extends
from zim.signals import SIGNAL_AFTER

try:
	import xattr
except ImportError:
	xattr = None


class XattrPlugin(PluginClass):

	plugin_info = {
		'name': _('Xattr tags'), # T: plugin name
		'description': _('''\
This plugin saves note tags in file extended attributes.

This makes tags visible in KDE file manager.
'''), # T: plugin description
		'author': 'Alexander Meshcheryakov',
	}

	#~ plugin_preferences = (
		# key, type, label, default
	#~ )

	@classmethod
	def check_dependencies(klass):
		return bool(xattr), [('python-xattr', not xattr is None, True)]


@extends('Notebook')
class NotebookExtension(ObjectExtension):

	def __init__(self, plugin, notebook):
		self.connectto_all(notebook, ('stored-page',), order=SIGNAL_AFTER)

	def on_stored_page(self, notebook, path):
		tags = list(notebook.tags.list_tags(path))
		if tags:
			tags = map(lambda x: x.name, tags)
			tags = ','.join(tags).encode('utf-8')
			logger.debug('Writing tags %s to %s', tags, path.source_file)
			xattr.setxattr(str(path.source_file),'user.xdg.tags',tags)
