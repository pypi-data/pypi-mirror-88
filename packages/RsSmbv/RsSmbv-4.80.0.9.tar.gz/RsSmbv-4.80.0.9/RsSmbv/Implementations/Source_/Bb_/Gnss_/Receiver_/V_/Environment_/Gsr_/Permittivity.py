from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Permittivity:
	"""Permittivity commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("permittivity", core, parent)

	def set(self, permittyvity: float, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:PERMittivity \n
		Sets the surface permittivity. \n
			:param permittyvity: float Range: 1 to 100
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.decimal_value_to_str(permittyvity)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:PERMittivity {param}')

	def get(self, stream=repcap.Stream.Default) -> float:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:PERMittivity \n
		Sets the surface permittivity. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: permittyvity: float Range: 1 to 100"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:PERMittivity?')
		return Conversions.str_to_float(response)
