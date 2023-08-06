from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Error:
	"""Error commands group definition. 9 total commands, 2 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("error", core, parent)

	def clone(self) -> 'Error':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Error(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def code(self):
		"""code commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_code'):
			from .Error_.Code import Code
			self._code = Code(self._core, self._base)
		return self._code

	@property
	def history(self):
		"""history commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_history'):
			from .Error_.History import History
			self._history = History(self._core, self._base)
		return self._history

	def get_all(self) -> str:
		"""SYSTem:ERRor:ALL \n
		Queries the error/event queue for all unread items and removes them from the queue. \n
			:return: all: string Error/event_number,'Error/event_description[;Device-dependent info]' A comma separated list of error number and a short description of the error in FIFO order. If the queue is empty, the response is 0,'No error' Positive error numbers are instrument-dependent. Negative error numbers are reserved by the SCPI standard. Volatile errors are reported once, at the time they appear. Identical errors are reported repeatedly only if the original error has already been retrieved from (and hence not any more present in) the error queue.
		"""
		response = self._core.io.query_str('SYSTem:ERRor:ALL?')
		return trim_str_response(response)

	def get_count(self) -> str:
		"""SYSTem:ERRor:COUNt \n
		Queries the number of entries in the error queue. \n
			:return: count: integer 0 The error queue is empty.
		"""
		response = self._core.io.query_str('SYSTem:ERRor:COUNt?')
		return trim_str_response(response)

	def get_static(self) -> str:
		"""SYSTem:ERRor:STATic \n
		Returns a list of all errors existing at the time when the query is started. This list corresponds to the display on the
		info page under manual control. \n
			:return: static_errors: string
		"""
		response = self._core.io.query_str('SYSTem:ERRor:STATic?')
		return trim_str_response(response)

	def get_next(self) -> str:
		"""SYSTem:ERRor:[NEXT] \n
		Queries the error/event queue for the oldest item and removes it from the queue. \n
			:return: next_py: string Error/event_number,'Error/event_description[;Device-dependent info]' Error number and a short description of the error. If the queue is empty, the response is 0,'No error' Positive error numbers are instrument-dependent. Negative error numbers are reserved by the SCPI standard. Volatile errors are reported once, at the time they appear. Identical errors are reported repeatedly only if the original error has already been retrieved from (and hence not any more present in) the error queue.
		"""
		response = self._core.io.query_str('SYSTem:ERRor:NEXT?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SYSTem:ERRor \n
		Queries the error/event queue for the oldest item and removes it from the queue. \n
			:return: dummy: string Error/event_number,'Error/event_description[;Device-dependent info]' Error number and a short description of the error. If the queue is empty, the response is 0,'No error' Positive error numbers are instrument-dependent. Negative error numbers are reserved by the SCPI standard. Volatile errors are reported once, at the time they appear. Identical errors are reported repeatedly only if the original error has already been retrieved from (and hence not any more present in) the error queue.
		"""
		response = self._core.io.query_str('SYSTem:ERRor?')
		return trim_str_response(response)
