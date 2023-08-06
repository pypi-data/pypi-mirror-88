"""Functions for working with reverb."""

from typing import Dict, Union

from synthizer import Context, GlobalFdnReverb

ReverbValue = Union[bool, float, str]
ReverbDict = Dict[str, ReverbValue]


def reverb_to_dict(
    reverb: GlobalFdnReverb, name: str = 'Untitled Reverb'
) -> ReverbDict:
    """Return the given reverb as a dictionary.

    This enables you to dump a reverb object as a dictionary.

    :param reverb: The Synthizer reverb object to dump.

    :param name: An optional name for easier identification of reverb presets.
    """
    return {
        'name': name,
        'gain': reverb.gain,
        'input_filter_cutoff': reverb.input_filter_cutoff,
        'input_filter_enabled': reverb.input_filter_enabled,
        'late_reflections_delay': reverb.late_reflections_delay,
        'late_reflections_diffusion': reverb.late_reflections_diffusion,
        # 'late_reflections_hf_reference':
        # reverb.late_reflections_hf_reference,
        'late_reflections_hf_rolloff': reverb.late_reflections_hf_rolloff,
        'late_reflections_lf_reference': reverb.late_reflections_lf_reference,
        'late_reflections_lf_rolloff': reverb.late_reflections_lf_rolloff,
        'late_reflections_modulation_depth':
        reverb.late_reflections_modulation_depth,
        'late_reflections_modulation_frequency':
        reverb.late_reflections_modulation_frequency,
        'mean_free_path': reverb.mean_free_path,
        't60': reverb.t60
    }


def reverb_from_dict(context: Context, data: ReverbDict) -> GlobalFdnReverb:
    """Return a reverb preset from the provided data.

    :param context: The synthizer context to bind the reverb object to.

    :param data: The data to load from.
    """
    reverb: GlobalFdnReverb = GlobalFdnReverb(context)
    name: str
    value: ReverbValue
    for name, value in data.items():
        if name != 'name':
            setattr(reverb, name, value)
    return reverb
