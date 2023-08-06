from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 7 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def clone(self) -> 'File':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = File(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def day(self):
		"""day commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_day'):
			from .File_.Day import Day
			self._day = Day(self._core, self._base)
		return self._day

	@property
	def month(self):
		"""month commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_month'):
			from .File_.Month import Month
			self._month = Month(self._core, self._base)
		return self._month

	@property
	def prefix(self):
		"""prefix commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_prefix'):
			from .File_.Prefix import Prefix
			self._prefix = Prefix(self._core, self._base)
		return self._prefix

	@property
	def year(self):
		"""year commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_year'):
			from .File_.Year import Year
			self._year = Year(self._core, self._base)
		return self._year

	def get_number(self) -> int:
		"""HCOPy:FILE:[NAME]:AUTO:[FILE]:NUMBer \n
		Queries the number that is used as part of the file name for the next hard copy in automatic mode. At the beginning, the
		count starts at 0. The R&S SMBV100B searches the specified output directory for the highest number in the stored files.
		It increases this number by one to achieve a unique name for the new file. The resulting auto number is appended to the
		resulting file name with at least three digits. \n
			:return: number: integer Range: 0 to 999999
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:FILE:NUMBer?')
		return Conversions.str_to_int(response)

	def get_value(self) -> str:
		"""HCOPy:FILE:[NAME]:AUTO:FILE \n
		Queries the name of the automatically named hard copy file. An automatically generated file name consists of:
		<Prefix><YYYY><MM><DD><Number>.<Format>. You can activate each component separately, to individually design the file name. \n
			:return: file: string
		"""
		response = self._core.io.query_str('HCOPy:FILE:NAME:AUTO:FILE?')
		return trim_str_response(response)
