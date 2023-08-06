from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Max:
	"""Max commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("max", core, parent)

	def set(self, max_iterations: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DPD<ST>:OUTPut:ITERations:MAX \n
		Sets the maximum number of performed iterations to achieving the required error set with method RsSmbv.Source.Iq.Dpd.
		Output.Error.Max.set. \n
			:param max_iterations: integer Range: 1 to 10
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')"""
		param = Conversions.decimal_value_to_str(max_iterations)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:OUTPut:ITERations:MAX {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:IQ:DPD<ST>:OUTPut:ITERations:MAX \n
		Sets the maximum number of performed iterations to achieving the required error set with method RsSmbv.Source.Iq.Dpd.
		Output.Error.Max.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Dpd')
			:return: max_iterations: integer Range: 1 to 10"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DPD{stream_cmd_val}:OUTPut:ITERations:MAX?')
		return Conversions.str_to_int(response)
