from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SuPolicy:
	"""SuPolicy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("suPolicy", core, parent)

	def set(self, sec_pass_word: str, update_policy: enums.UpdPolicyMode) -> None:
		"""SYSTem:SECurity:SUPolicy \n
		Configures the automatic signature verification for firmware installation. \n
			:param sec_pass_word: string
			:param update_policy: STRict| CONFirm| IGNore
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sec_pass_word', sec_pass_word, DataType.String), ArgSingle('update_policy', update_policy, DataType.Enum))
		self._core.io.write(f'SYSTem:SECurity:SUPolicy {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self) -> enums.UpdPolicyMode:
		"""SYSTem:SECurity:SUPolicy \n
		Configures the automatic signature verification for firmware installation. \n
			:return: update_policy: STRict| CONFirm| IGNore"""
		response = self._core.io.query_str(f'SYSTem:SECurity:SUPolicy?')
		return Conversions.str_to_scalar_enum(response, enums.UpdPolicyMode)
