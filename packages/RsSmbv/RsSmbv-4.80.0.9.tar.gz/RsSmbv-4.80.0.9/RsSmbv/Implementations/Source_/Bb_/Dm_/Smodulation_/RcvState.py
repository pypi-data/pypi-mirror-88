from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RcvState:
	"""RcvState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rcvState", core, parent)

	# noinspection PyTypeChecker
	def get(self, rcv_state: enums.DmExtRcvStateType) -> enums.DmExtRcvStateType:
		"""[SOURce<HW>]:BB:DM:SMODulation:RCVState \n
		No command help available \n
			:param rcv_state: No help available
			:return: rcv_state: No help available"""
		param = Conversions.enum_scalar_to_str(rcv_state, enums.DmExtRcvStateType)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:DM:SMODulation:RCVState? {param}')
		return Conversions.str_to_scalar_enum(response, enums.DmExtRcvStateType)
