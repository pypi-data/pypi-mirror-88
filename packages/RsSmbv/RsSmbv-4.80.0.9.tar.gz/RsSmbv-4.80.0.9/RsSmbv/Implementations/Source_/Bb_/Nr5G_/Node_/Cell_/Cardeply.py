from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cardeply:
	"""Cardeply commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cardeply", core, parent)

	def set(self, carrier_depl: enums.Nr5GcarDep, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CARDeply \n
		Selects one of the frequency ranges, specified for 5G NR transmission. \n
			:param carrier_depl: FR1LT3| FR1GT3| FR2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(carrier_depl, enums.Nr5GcarDep)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CARDeply {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.Nr5GcarDep:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:CARDeply \n
		Selects one of the frequency ranges, specified for 5G NR transmission. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: carrier_depl: FR1LT3| FR1GT3| FR2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:CARDeply?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5GcarDep)
