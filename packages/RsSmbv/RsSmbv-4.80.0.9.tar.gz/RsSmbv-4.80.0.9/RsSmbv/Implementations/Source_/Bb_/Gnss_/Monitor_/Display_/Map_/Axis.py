from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Axis:
	"""Axis commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("axis", core, parent)

	def set(self, axis_type: enums.AxisType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:MAP:AXIS \n
		Changes the axis type in the 'Map View' display. \n
			:param axis_type: GRID| CIRCles
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')"""
		param = Conversions.enum_scalar_to_str(axis_type, enums.AxisType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:MAP:AXIS {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.AxisType:
		"""[SOURce<HW>]:BB:GNSS:MONitor<CH>:DISPlay:MAP:AXIS \n
		Changes the axis type in the 'Map View' display. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Monitor')
			:return: axis_type: GRID| CIRCles"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:MONitor{channel_cmd_val}:DISPlay:MAP:AXIS?')
		return Conversions.str_to_scalar_enum(response, enums.AxisType)
