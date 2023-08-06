from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetitions:
	"""Repetitions commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repetitions", core, parent)

	def set(self, repetitions: int, frameIx=repcap.FrameIx.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:FRAMe<DI>:REPetitions \n
		The command defines the number of repetitions for the selected frame in GSM mode Frame (Double) . \n
			:param repetitions: integer Range: 1 to 500000
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')"""
		param = Conversions.decimal_value_to_str(repetitions)
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:REPetitions {param}')

	def get(self, frameIx=repcap.FrameIx.Default) -> int:
		"""[SOURce<HW>]:BB:GSM:FRAMe<DI>:REPetitions \n
		The command defines the number of repetitions for the selected frame in GSM mode Frame (Double) . \n
			:param frameIx: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frame')
			:return: repetitions: integer Range: 1 to 500000"""
		frameIx_cmd_val = self._base.get_repcap_cmd_value(frameIx, repcap.FrameIx)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:FRAMe{frameIx_cmd_val}:REPetitions?')
		return Conversions.str_to_int(response)
