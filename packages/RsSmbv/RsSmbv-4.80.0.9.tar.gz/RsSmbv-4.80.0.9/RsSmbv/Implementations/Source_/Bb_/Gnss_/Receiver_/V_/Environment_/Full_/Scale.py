from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scale:
	"""Scale commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("scale", core, parent)

	def set(self, reference_scale: enums.RefScale, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:SCALe \n
		Defines whether the obstacles' positions are defined as distance (in km) or as time (in s) . \n
			:param reference_scale: TIME| DISTance
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(reference_scale, enums.RefScale)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:SCALe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.RefScale:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:FULL:SCALe \n
		Defines whether the obstacles' positions are defined as distance (in km) or as time (in s) . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: reference_scale: TIME| DISTance"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:FULL:SCALe?')
		return Conversions.str_to_scalar_enum(response, enums.RefScale)
