from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.PowSensFiltType, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:FILTer:TYPE \n
		Selects the filter mode. The filter length is the multiplier for the time window and thus directly affects the
		measurement time. \n
			:param type_py: AUTO| USER| NSRatio AUTO Automatically selects the filter length, depending on the measured value. The higher the power, the shorter the filter length, and vice versa. USER Allows you to set the filter length manually. As the filter-length takes effect as a multiplier of the measurement time, you can achieve constant measurement times. NSRatio Selects the filter length (averaging factor) according to the criterion that the intrinsic noise of the sensor (2 standard deviations) does not exceed the specified noise content. You can define the noise content with command FILTer:NSRatio. Note: To avoid long settling times when the power is low, you can limit the averaging factor limited with the 'timeout' parameter (FILTer:NSRatio:MTIMe) .
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.PowSensFiltType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.PowSensFiltType:
		"""SENSe<CH>:[POWer]:FILTer:TYPE \n
		Selects the filter mode. The filter length is the multiplier for the time window and thus directly affects the
		measurement time. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')
			:return: type_py: AUTO| USER| NSRatio AUTO Automatically selects the filter length, depending on the measured value. The higher the power, the shorter the filter length, and vice versa. USER Allows you to set the filter length manually. As the filter-length takes effect as a multiplier of the measurement time, you can achieve constant measurement times. NSRatio Selects the filter length (averaging factor) according to the criterion that the intrinsic noise of the sensor (2 standard deviations) does not exceed the specified noise content. You can define the noise content with command FILTer:NSRatio. Note: To avoid long settling times when the power is low, you can limit the averaging factor limited with the 'timeout' parameter (FILTer:NSRatio:MTIMe) ."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SENSe{channel_cmd_val}:POWer:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.PowSensFiltType)
