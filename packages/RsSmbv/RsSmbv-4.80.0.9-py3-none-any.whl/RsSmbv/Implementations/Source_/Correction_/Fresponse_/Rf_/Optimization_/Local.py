from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Local:
	"""Local commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("local", core, parent)

	def set(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:LOCal \n
		For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG, triggers optimization for the current settings. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:LOCal')

	def set_with_opc(self) -> None:
		"""[SOURce<HW>]:CORRection:FRESponse:RF:OPTimization:LOCal \n
		For method RsSmbv.Source.Correction.Fresponse.Rf.Optimization.modeQHIG, triggers optimization for the current settings. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:FRESponse:RF:OPTimization:LOCal')
