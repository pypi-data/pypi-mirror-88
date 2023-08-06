from ..Internal import Core
from typing import List, Tuple
import math
import datetime
from struct import pack


class ArbFiles:
	"""Class containing utilities to operate the arbitrary file - creation and transfer to the instrument"""

	def __init__(self, core: Core):
		self._core = core

	def send_waveform_file_to_instrument(self, wv_file_path, instr_file_path):
		"""Same as send_file_from_pc_to_instrument()"""
		cmd = f"MMEM:DATA '{instr_file_path}',"
		self._core.io.write_bin_block_from_file(cmd, wv_file_path)

	@staticmethod
	def create_waveform_file_from_samples(i_samples: List[float], q_samples: List[float], out_wv_file_path: str, clock_freq: float, auto_scale: bool = True, comment: str = '', additional_tags: List[str] = None) -> Tuple[int, float, float]:
		"""Creates a R&S waveform file based on provided I and Q samples.
		:param i_samples: List of I input samples
		:param q_samples: List of Q input samples
		:param out_wv_file_path: Path where to save the created file
		:param clock_freq: Default clock frequency of the file
		:param auto_scale: If True (default), the samples are scaled to the max value. If false, make sure they are properly scaled
		:param comment: Comment for the waveform file
		:param additional_tags: add list of additional tags, for example markers
		:return Returns tuple: (samples count, peak offset to full scale in dB, RMS offset to full scale in dB)"""

		# Determine overall number of samples
		samples = len(i_samples)
		if len(i_samples) != len(q_samples):
			raise Exception(f"I and Q sample Lists are not of the same length. I length: '{len(i_samples)}', Q length: '{len(q_samples)}'")

		# Calculate the (squared) IQ vectors
		iq_vectors_sqr = ArbFiles._get_square_iq_vectors(i_samples, q_samples)
		iq_vector_max_offset = ArbFiles._get_iq_vector_max_offset(iq_vectors_sqr)

		# Check if autoscaling to full scale is required
		if auto_scale and iq_vector_max_offset != 1.0:
			scale_factor = math.sqrt(iq_vector_max_offset)
			for x in range(samples):
				i_samples[x] *= scale_factor
				q_samples[x] *= scale_factor

			# Re-calculate the (squared) IQ vectors
			iq_vectors_sqr = ArbFiles._get_square_iq_vectors(i_samples, q_samples)
			iq_vector_max_offset = ArbFiles._get_iq_vector_max_offset(iq_vectors_sqr)

		else:
			i_data_max = max(i_samples)
			i_data_min = min(i_samples)
			q_data_max = max(q_samples)
			q_data_min = min(q_samples)
			# Checking I and Q components if autoscaling is disabled
			if i_data_min < -1 or i_data_max > 1:
				raise OverflowError(f'I component must be in the range between -1 to +1 if auto scaling is disabled.\nCurrent I range is {i_data_min} .. {i_data_max}')
			if q_data_min < -1 or q_data_max > 1:
				raise OverflowError(f'Q component must be in the range between -1 to +1 if auto scaling is disabled.\nCurrent Q range is {q_data_min} .. {q_data_max}')
			for x in range(samples):
				size = math.sqrt(iq_vectors_sqr[x])
				if size > 1:
					raise OverflowError(f'I/Q vector size is > 1: sample {x}, vector size {size}')

		# Check if any IQ vector > zero
		if max(iq_vectors_sqr) > 0:
			# Calculate the (squared) RMS IQ vector offset to full scale (1)
			iq_vector_rms_offset = samples / math.fsum(iq_vectors_sqr)
		else:
			iq_vector_rms_offset = 1

		# Calculate the logarithmic (squared) RMS and MAX IQ vector offset to full scale (1)
		iq_vector_max_offset_log = round(10 * math.log10(iq_vector_max_offset), 5)
		iq_vector_rms_offset_log = round(10 * math.log10(iq_vector_rms_offset), 5)

		# Open new waveform file for writing as text
		with open(out_wv_file_path, 'w') as file:
			# Write waveform file header
			# The tags TYPE, CLOCK, LEVEL OFFS and WAVEFORM are mandatory for each
			# waveform. All other tags are optional and can be inserted after the TYPE tag in
			# arbitrary order. The waveform data tag must be the final one.
			file.write(ArbFiles._get_wv_file_tag(f'TYPE: SMU-WV,0'))
			file.write(ArbFiles._get_wv_file_tag(f'COMMENT: {comment}'))
			file.write(ArbFiles._get_wv_file_tag(f'COPYRIGHT: Rohde&Schwarz'))
			file.write(ArbFiles._get_wv_file_tag(f'DATE: {datetime.datetime.now().strftime("%Y-%m-%d;%H:%M:%S")}'))
			file.write(ArbFiles._get_wv_file_tag(f'CONTROL LENGTH: {samples}'))
			file.write(ArbFiles._get_wv_file_tag(f'SAMPLES: {samples}'))
			file.write(ArbFiles._get_wv_file_tag(f'CLOCK: {clock_freq}'))
			file.write(ArbFiles._get_wv_file_tag(f'LEVEL OFFS: {iq_vector_rms_offset_log},{iq_vector_max_offset_log}'))

			# Check if additional tags are present
			if additional_tags:
				for tag in additional_tags:
					file.write(ArbFiles._get_wv_file_tag(tag))

			# Waveform tag is the last string tag in the file
			file.write('{WAVEFORM-' + f'{4 * samples + 1}: #')

		# Open waveform file again to append as binary and write samples
		with open(out_wv_file_path, 'ab') as file:
			# Write waveform IQ data
			# Note: 16-bit signed integer in 2's complement notation containing
			#      the I and Q component alternately and starting with the I component.
			#      Each component consists of two bytes in Little endian format
			#      representation, i.e least significant byte (LSB) first.
			#      The values of the two bytes in an I component and a Q component
			#      are in the range 0x8001 to 0x7FFF (-32767 to +32767).
			#      Please look into the SMW user manual for the conversion table.
			#      Note: +0.5 to overcome round down effect of "floor"
			for x in range(samples):
				# Write I sample
				int_i = int(math.floor(i_samples[x] * 32767 + 0.5))
				file.write(pack('h', int_i))

				# Write Q sample
				int_q = int(math.floor(q_samples[x] * 32767 + 0.5))
				file.write(pack('h', int_q))

			# Tag curly bracket at the end
			file.write(b'}')

		# Return the samples count, peak offset to full scale in dB, RMS offset to full scale in dB
		return samples, iq_vector_max_offset_log, iq_vector_rms_offset_log

	@staticmethod
	def _get_square_iq_vectors(i_data: List[float], q_data: List[float]) -> List[float]:
		"""Returns List of squared sum of the i and q values: x = pow(i,2) + pow(q,2)"""
		iq_vector_list = []
		for x in range(len(i_data)):
			iq_vector_list.append(pow(i_data[x], 2) + pow(q_data[x], 2))
		return iq_vector_list

	@staticmethod
	def _get_iq_vector_max_offset(iq_vector_list: List[float]) -> float:
		# Check if any IQ vector > zero
		maximum = max(iq_vector_list)
		# Calculate the (squared) MAX IQ vector offset to full scale (1)
		result = 1.0 if maximum <= 0 else 1.0 / maximum
		return result

	@staticmethod
	def _get_wv_file_tag(content: str) -> str:
		"""Returns the tag surrounded by exactly one pair of curly brackets"""
		content = content.lstrip('{').rstrip('}')
		content = '{' + content + '}'
		return content

	@staticmethod
	def create_waveform_file_from_samples_file(iq_samples_file_path: str, wv_file_path: str, clock_freq: float, auto_scale: bool = True, comment: str = '', additional_tags: List[str] = None) -> Tuple[int, float, float]:
		"""Creates a R&S waveform file based on provided IQ data file.
		The I and Q values in the in_iq_samples_file_path can be either given in a single
		complex number in each row or I & Q values separated by a comma in each row.
		:param iq_samples_file_path: Input file with IQ samples
		:param wv_file_path: Path where to save the created file
		:param clock_freq: Default clock frequency of the file
		:param auto_scale: If True (default), the samples are scaled to the max value. If false, make sure they are properly scaled
		:param comment: Comment for the waveform file
		:param additional_tags: add list of additional tags, for example markers
		:return Returns tuple: (samples count, peak offset to full scale in dB, RMS offset to full scale in dB)"""

		# Read the IQ data file
		with open(iq_samples_file_path, 'r') as file:
			# Read IQ data from IQ data file
			i_samples: List[float] = []
			q_samples: List[float] = []
			for line in file:
				line = line.strip()
				if line == '':
					continue

				# IQ as complex number
				if 'j' in line:
					i = float(complex(line).real)
					q = float(complex(line).imag)
				# I and Q separated with a comma (,)
				elif ',' in line:
					values = line.split(',')
					if len(values) != 2:
						raise Exception(f"IQ file '{iq_samples_file_path}' line '{line}' has unsupported format - you need exactly 2 comma-separated values pro line")
					i = float(values[0])
					q = float(values[1])
				else:
					raise Exception(f"IQ file '{iq_samples_file_path}' line '{line}' has unsupported format")
				i_samples.append(i)
				q_samples.append(q)

		return ArbFiles.create_waveform_file_from_samples(i_samples, q_samples, wv_file_path, clock_freq, auto_scale, comment, additional_tags)
