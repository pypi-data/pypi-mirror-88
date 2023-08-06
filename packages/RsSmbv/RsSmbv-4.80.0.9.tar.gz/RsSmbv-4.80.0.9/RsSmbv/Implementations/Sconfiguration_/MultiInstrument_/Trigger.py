from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	# noinspection PyTypeChecker
	def get_synchronization(self) -> enums.MultInstSyncState:
		"""SCONfiguration:MULTiinstrument:TRIGger:SYNChronization \n
		Queries if synchronization is achieved. \n
			:return: sync_state: SYNC| NOSYnc
		"""
		response = self._core.io.query_str('SCONfiguration:MULTiinstrument:TRIGger:SYNChronization?')
		return Conversions.str_to_scalar_enum(response, enums.MultInstSyncState)
