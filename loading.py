from pathlib import Path

import h5py
import numpy as np
import ruamel_yaml

project_path = None


def load_project(path):
    global project_path
    project_path = path


ks_sample_rate = None
ks_spike_times = None
ks_spike_templates = None
ks_channel_pos = None
ks_spike_amplitudes = None
ks_spike_clusters = None


def load_kilosort(path=None):
    global ks_sample_rate, ks_channel_pos, ks_spike_amplitudes, ks_spike_clusters, ks_spike_templates, ks_spike_times

    if path is None:
        path = project_path

    g = {}
    exec(Path(path + '/params.py').read_bytes(), g)

    ks_sample_rate = g['sample_rate']
    ks_spike_times = np.load(path + "/spike_times.npy") / ks_sample_rate
    ks_spike_amplitudes = np.load(path + "/amplitudes.npy")
    ks_spike_templates = np.load(path + "/templates.npy")
    ks_channel_pos = np.load(path + "/channel_positions.npy")
    ks_spike_clusters = np.load(path + "/spike_clusters.npy")


lfp_data_path = None
lfp_data = None
channel_number = None
sample_rate = None
total_seconds = None


def load_lfp(path):
    """

    Parameters
    ----------
    path : str

    """
    global lfp_data_path, lfp_data, channel_number, sample_rate, total_seconds

    if '/' in path:
        lfp_data_path = path
    else:
        lfp_data_path = project_path + '/' + path

    meta_path = lfp_data_path.replace('.bin', '.meta')
    with open(meta_path, 'r') as f:
        for line in f:
            if line.startswith('nSavedChans='):
                channel_number = int(line.strip()[len('nSavedChans='):])
            if line.startswith('imSampRate='):
                sample_rate = int(line.strip()[len('imSampRate='):])
            if line.startswith('fileTimeSecs='):
                total_seconds = float(line.strip()[len('fileTimeSecs='):])

    lfp_data = np.memmap(lfp_data_path, dtype=np.dtype('int16')).reshape((-1, channel_number))


evt_start_time = None


def load_event(path):
    global evt_start_time
    from fklab.io.neuralynx import NlxOpen
    evt_data = NlxOpen(path)
    evt_time = evt_data.data._memorymap['timestamp']
    evt_estr = evt_data.data._memorymap['eventstring']
    evt_start_time = evt_time[evt_estr == b'Starting Recording'] / 1e6


cluster_data = None


def load_cluster(path=None):
    """

    Parameters
    ----------
    path

    Returns
    -------

    """
    global cluster_data
    if path is None:
        path = project_path + '/cluster_info.tsv'

    dtype = np.dtype([
        ('id', np.int),
        ('Amplitude', np.float),
        ('ContamPct', np.float),
        ('KSLabel', np.dtype('U5')),
        ('amp', np.float),
        ('channel', np.int),
        ('depth', np.float),
        ('firing_rate', np.float),
        ('group', np.dtype('U5')),
        ('n_spikes', np.int),
        ('shank', np.int),
    ])

    cluster_data = np.loadtxt(path, dtype=dtype, skiprows=1, delimiter='\t',
                              converters={7: lambda fr: fr.replace(b' spk/s', b'')})


def get_cluster_ids(channel_list):
    cu = cluster_data['id']
    ch = cluster_data['channel']

    ret = []

    for channel in channel_list:
        ret.extend(cu[ch == channel])

    return ret

def get_time_slice(start, stop, time_minute=False):
    """

    Parameters
    ----------
    start : float
        second
    stop : float
        second
    time_minute

    Returns
    -------
    slice

    """
    f = sample_rate

    if time_minute:
        f *= 60

    return slice(start + f, stop * f)


position_data_path = None
head_direction = None
position = None
position_time = None
position_velocity = None


def load_position(path):
    global position_data_path, head_direction, position, position_time, position_velocity
    position_data_path = path
    position_data = h5py.File(path, 'r')

    # diodes = position_data['diodes'].value
    head_direction = np.array(position_data['head_direction'])
    position = np.array(position_data['position'])
    position_time = np.array(position_data['time'])
    position_velocity = np.array(position_data['velocity'])


position_yaml = None


def load_position_yaml(path=None):
    global position_yaml
    if path is None:
        path = str(Path(position_data_path).with_name('position.yaml'))

    with open(path) as f:
        position_yaml = ruamel_yaml.YAML().load(f)


environment_yaml = None


def load_environment_yaml(path=None):
    global environment_yaml
    if path is None:
        path = str(Path(position_data_path).with_name('environment.yaml'))

    with open(path) as f:
        environment_yaml = ruamel_yaml.YAML().load(f)


def get_spike_seq(time_range, *, cluster_list=None, channel_list=None):
    """
    Examples
    --------
    >>> mask = get_spike_seq(...)
    >>> spike_count = np.count_nonzero(mask)
    >>> spike_t = ks_spike_times[mask, 0]
    >>> spike_a = ks_spike_amplitudes[mask]

    Parameters
    ----------
    time_range
    cluster_list
    channel_list

    Returns
    -------

    """
    if cluster_list is not None and channel_list is not None:
        raise RuntimeError('either cluster_list or channel_list')

    ret = []

    for cluster in cluster_data:
        cluster_id = cluster['id']
        channel_id = cluster['channel']

        if cluster_list is not None and cluster_id not in cluster_list:
            continue

        if channel_list is not None and channel_id not in channel_list:
            continue

        spike_mask = np.logical_and.reduce((
            ks_spike_clusters == cluster_id,
            time_range[0] <= ks_spike_times[:, 0],
            ks_spike_times[:, 0] <= time_range[1]
        ))

        ret.append(spike_mask)

    return np.logical_or.reduce(tuple(ret))
