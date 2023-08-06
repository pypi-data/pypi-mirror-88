from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Qwset:
	"""Qwset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("qwset", core, parent)

	def set(self, qw_set: int, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:QWSet \n
		The command selects the quasi orthogonal Walsh code set. The standard defines three different sets. The quasi-orthogonal
		Walsh codes are used for a given channel if method RsSmbv.Source.Bb.C2K.Bstation.Cgroup.Coffset.Qwcode.State.set is ON. \n
			:param qw_set: integer Range: 1 to 3
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')"""
		param = Conversions.decimal_value_to_str(qw_set)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:QWSet {param}')

	def get(self, stream=repcap.Stream.Default) -> int:
		"""[SOURce<HW>]:BB:C2K:BSTation<ST>:QWSet \n
		The command selects the quasi orthogonal Walsh code set. The standard defines three different sets. The quasi-orthogonal
		Walsh codes are used for a given channel if method RsSmbv.Source.Bb.C2K.Bstation.Cgroup.Coffset.Qwcode.State.set is ON. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:return: qw_set: integer Range: 1 to 3"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:BSTation{stream_cmd_val}:QWSet?')
		return Conversions.str_to_int(response)
