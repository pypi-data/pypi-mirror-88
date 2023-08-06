from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("power", core, parent)

	def get_continuous(self) -> bool:
		"""INITiate<HW>:[POWer]:CONTinuous \n
		Switches the local state of the continuous power measurement by R&S NRP power sensors on and off. Switching off local
		state enhances the measurement performance during remote control. The remote measurement is triggered with
		:​READ<ch>[:​POWer]?) . This command also returns the measurement results. The local state is not affected, measurement
		results can be retrieved with local state on or off. \n
			:return: continuous: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('INITiate<HwInstance>:POWer:CONTinuous?')
		return Conversions.str_to_bool(response)

	def set_continuous(self, continuous: bool) -> None:
		"""INITiate<HW>:[POWer]:CONTinuous \n
		Switches the local state of the continuous power measurement by R&S NRP power sensors on and off. Switching off local
		state enhances the measurement performance during remote control. The remote measurement is triggered with
		:​READ<ch>[:​POWer]?) . This command also returns the measurement results. The local state is not affected, measurement
		results can be retrieved with local state on or off. \n
			:param continuous: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(continuous)
		self._core.io.write(f'INITiate<HwInstance>:POWer:CONTinuous {param}')
