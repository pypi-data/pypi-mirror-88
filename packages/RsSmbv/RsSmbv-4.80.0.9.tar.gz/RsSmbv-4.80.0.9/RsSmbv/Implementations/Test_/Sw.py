from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sw:
	"""Sw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sw", core, parent)

	# noinspection PyTypeChecker
	class ScmdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Scmd: str: No parameter help available
			- What_Is_This: str: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_str('Scmd'),
			ArgStruct.scalar_str('What_Is_This')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Scmd: str = None
			self.What_Is_This: str = None

	def get_scmd(self) -> ScmdStruct:
		"""TEST<HW>:SW:SCMD \n
		No command help available \n
			:return: structure: for return value, see the help for ScmdStruct structure arguments.
		"""
		return self._core.io.query_struct('TEST<HwInstance>:SW:SCMD?', self.__class__.ScmdStruct())

	def set_scmd(self, value: ScmdStruct) -> None:
		"""TEST<HW>:SW:SCMD \n
		No command help available \n
			:param value: see the help for ScmdStruct structure arguments.
		"""
		self._core.io.write_struct('TEST<HwInstance>:SW:SCMD', value)
