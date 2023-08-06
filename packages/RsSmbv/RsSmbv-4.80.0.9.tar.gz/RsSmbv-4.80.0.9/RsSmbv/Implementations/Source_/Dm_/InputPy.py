from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InputPy:
	"""InputPy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("inputPy", core, parent)

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.InputImpRf:
		"""[SOURce<HW>]:DM:INPut:IMPedance \n
		No command help available \n
			:return: impedance: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:DM:INPut:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.InputImpRf)

	def set_impedance(self, impedance: enums.InputImpRf) -> None:
		"""[SOURce<HW>]:DM:INPut:IMPedance \n
		No command help available \n
			:param impedance: No help available
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.InputImpRf)
		self._core.io.write(f'SOURce<HwInstance>:DM:INPut:IMPedance {param}')
