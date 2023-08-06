from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vehicle:
	"""Vehicle commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vehicle", core, parent)

	def set(self, vehicle: enums.RefVehicle, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:VEHicle \n
		No command help available \n
			:param vehicle: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')"""
		param = Conversions.enum_scalar_to_str(vehicle, enums.RefVehicle)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:VEHicle {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.RefVehicle:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:VEHicle \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: vehicle: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:VEHicle?')
		return Conversions.str_to_scalar_enum(response, enums.RefVehicle)
