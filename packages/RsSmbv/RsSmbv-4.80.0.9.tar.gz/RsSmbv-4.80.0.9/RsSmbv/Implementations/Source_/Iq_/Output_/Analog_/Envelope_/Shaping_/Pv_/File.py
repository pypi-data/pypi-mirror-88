from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 4 total commands, 0 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:CATalog \n
		Queries the available table shaping files in the default directory. Only files with the file extension *.iq_lut or *.
		iq_lutpv are listed. \n
			:return: catalog: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:CATalog?')
		return Conversions.str_to_str_list(response)

	def get_data(self) -> List[float]:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:DATA \n
		Defines the shaping function in a raw data format. See also IQ:ENVelope:SHAPing:PV:FILE:NEW. \n
			:return: ipartq_out_env_shape_data_pv: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:DATA?')
		return response

	def set_data(self, ipartq_out_env_shape_data_pv: List[float]) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:DATA \n
		Defines the shaping function in a raw data format. See also IQ:ENVelope:SHAPing:PV:FILE:NEW. \n
			:param ipartq_out_env_shape_data_pv: No help available
		"""
		param = Conversions.list_to_csv_str(ipartq_out_env_shape_data_pv)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:DATA {param}')

	def set_new(self, iq_out_env_shape_data_pv_new_file: List[float]) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:NEW \n
		Stores the shaping values into a file with the selected file name and loads it. The file is stored in the default
		directory or in the directory specified with the absolute file path. If the file does not yet exist, a new file is
		created. The file extension is assigned automatically. \n
			:param iq_out_env_shape_data_pv_new_file: No help available
		"""
		param = Conversions.list_to_csv_str(iq_out_env_shape_data_pv_new_file)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:NEW {param}')

	def get_select(self) -> str:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:[SELect] \n
		Selects an envelope shaping file (extension *.iq_lut or *.iq_lutpv) . \n
			:return: filename: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:SELect?')
		return trim_str_response(response)

	def set_select(self, filename: str) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:ENVelope:SHAPing:PV:FILE:[SELect] \n
		Selects an envelope shaping file (extension *.iq_lut or *.iq_lutpv) . \n
			:param filename: string
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:ENVelope:SHAPing:PV:FILE:SELect {param}')
