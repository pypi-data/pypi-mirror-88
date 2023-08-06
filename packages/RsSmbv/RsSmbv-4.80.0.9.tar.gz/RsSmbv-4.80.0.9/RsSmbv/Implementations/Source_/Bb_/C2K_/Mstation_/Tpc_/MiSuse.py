from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MiSuse:
	"""MiSuse commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("miSuse", core, parent)

	def set(self, mis_use: bool, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:MISuse \n
		The command activates/deactives the use of the power control data for controlling the mobile station output power. On the
		uplink, the power control bits are used exclusively for controlling the mobile station output power. Power control
		puncturing is not defined for controlling the base station power. The bit pattern (see commands BB:C2K:MSTation<n>:TPC...
		) of the power control bits w is used to control the channel power. A '1' leads to an increase of channel powers, a '0'
		to a reduction of channel powers. Channel power is limited to the range 0 dB to -80 dB. The step width of the change is
		defined with the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Pstep.set. \n
			:param mis_use: 0| 1| OFF| ON
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.bool_to_str(mis_use)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:MISuse {param}')

	def get(self, stream=repcap.Stream.Default) -> bool:
		"""[SOURce<HW>]:BB:C2K:MSTation<ST>:TPC:MISuse \n
		The command activates/deactives the use of the power control data for controlling the mobile station output power. On the
		uplink, the power control bits are used exclusively for controlling the mobile station output power. Power control
		puncturing is not defined for controlling the base station power. The bit pattern (see commands BB:C2K:MSTation<n>:TPC...
		) of the power control bits w is used to control the channel power. A '1' leads to an increase of channel powers, a '0'
		to a reduction of channel powers. Channel power is limited to the range 0 dB to -80 dB. The step width of the change is
		defined with the command method RsSmbv.Source.Bb.C2K.Mstation.Tpc.Pstep.set. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: mis_use: 0| 1| OFF| ON"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:C2K:MSTation{stream_cmd_val}:TPC:MISuse?')
		return Conversions.str_to_bool(response)
