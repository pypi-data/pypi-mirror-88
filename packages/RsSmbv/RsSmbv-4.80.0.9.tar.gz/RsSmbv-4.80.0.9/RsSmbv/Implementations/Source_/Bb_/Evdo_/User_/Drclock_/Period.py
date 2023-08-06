from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Period:
	"""Period commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("period", core, parent)

	def set(self, period: enums.EvdoDrcPer, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:PERiod \n
		Sets the period (measured in slots) of time between successive transmissions of the DRC (Data Rate Control) Lock bit for
		the selected user. Note: A value of zero disables the DRC Lock subchannel and the MAC RPC channel of the selected user is
		not punctured with the DRC Lock subchannel. \n
			:param period: DP0| DP4| DP8| DP16
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(period, enums.EvdoDrcPer)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:PERiod {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoDrcPer:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:PERiod \n
		Sets the period (measured in slots) of time between successive transmissions of the DRC (Data Rate Control) Lock bit for
		the selected user. Note: A value of zero disables the DRC Lock subchannel and the MAC RPC channel of the selected user is
		not punctured with the DRC Lock subchannel. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: period: DP0| DP4| DP8| DP16"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:PERiod?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoDrcPer)
