from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:STATe \n
		The command activates or deactivates channel coding for the PCPCH. When channel coding is active, the symbol rate is
		limited to the range between 15 and 120 ksps. Values above this limit are automatically set to 120 ksps. \n
			:return: state: ON| OFF
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:STATe \n
		The command activates or deactivates channel coding for the PCPCH. When channel coding is active, the symbol rate is
		limited to the range between 15 and 120 ksps. Values above this limit are automatically set to 120 ksps. \n
			:param state: ON| OFF
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:STATe {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.ChanCodTypeEnhPcpc:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. \n
			:return: type_py: TB168| TB360 TB168 CPCH RMC (TB size 168 bits) TB360 CPCH RMC (TB size 360 bits)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ChanCodTypeEnhPcpc)

	def set_type_py(self, type_py: enums.ChanCodTypeEnhPcpc) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. \n
			:param type_py: TB168| TB360 TB168 CPCH RMC (TB size 168 bits) TB360 CPCH RMC (TB size 360 bits)
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.ChanCodTypeEnhPcpc)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:PCPCh:CCODing:TYPE {param}')
