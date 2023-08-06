from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("length", core, parent)

	def set(self, length: enums.EvdoDrcLenDn, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:LENGth \n
		Sets the number of DRC (Data Rate Control) Lock periods that the state of the DRC Lock for the selected user is held
		constant. Note: Changes in the DRC Lock state are only considered at the interval defined by the parameter DRC Lock
		Length. A value of one allows updating of the DRC Lock bit at anytime. \n
			:param length: DL1| DL4| DL8| DL16| DL32| DL64
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(length, enums.EvdoDrcLenDn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:LENGth {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.EvdoDrcLenDn:
		"""[SOURce<HW>]:BB:EVDO:USER<ST>:DRCLock:LENGth \n
		Sets the number of DRC (Data Rate Control) Lock periods that the state of the DRC Lock for the selected user is held
		constant. Note: Changes in the DRC Lock state are only considered at the interval defined by the parameter DRC Lock
		Length. A value of one allows updating of the DRC Lock bit at anytime. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: length: DL1| DL4| DL8| DL16| DL32| DL64"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EVDO:USER{stream_cmd_val}:DRCLock:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoDrcLenDn)
