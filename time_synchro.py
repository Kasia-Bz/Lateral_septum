import numpy as np
import os.path
from pathlib import Path
from fklab.io.neuralynx import NlxOpen


def drop_falling_edge(a):
    m = a[:, 1] > 0
    return a[m, :]


def drop_rising_edge(a):
    m = a[:, 1] == 0
    return a[m, :]


def time_sync_align(seq_1, seq_2, threshold=0.001, min_length=3, order=1):
    from scipy.sparse import csr_matrix

    ga = np.gradient(seq_1[:, 0], edge_order=1)[:, None]
    gb = np.gradient(seq_2[:, 0], edge_order=1)[None, :]
    x = np.abs(ga - gb)

    x = x < threshold
    nx, ny = x.shape
    xi, yi = np.nonzero(x)
    x = csr_matrix(x)

    result = []

    for kx, ky in zip(xi, yi):
        if x[kx, ky]:
            n = 1

            # find beginning
            start_x, start_y = kx, ky
            while start_x > 0 and start_y > 0 and x[start_x - 1, start_y - 1]:
                start_x -= 1
                start_y -= 1
                n += 1
                x[start_x, start_y] = False

            # find end
            end_x, end_y = kx, ky
            while end_x < nx - 1 and end_y < ny - 1 and x[end_x + 1, end_y + 1]:
                end_x += 1
                end_y += 1
                n += 1
                x[end_x, end_y] = False

            if n >= min_length:
                result.append(((start_x, end_x), (start_y, end_y)))

            x[kx, ky] = False

    return result


# ==== average time shift value ====

def average_time_align_frame(seq_1, seq_2, time_align_frame):
    result = []

    for ((e1, e2), (d1, d2)) in time_align_frame:
        t1 = seq_1[e1:e2, 0]
        t2 = seq_2[d1:d2, 0]
        result.extend(list(t2 - t1))

    result = np.array(result)
    print('mean', np.mean(result))
    print('std', np.std(result))

    return np.mean(result)


def synchro(evt_file, dat_file,
            use_cache=True,
            save_cache=True):
    """

    Parameters
    ----------
    evt_file :str
    dat_file :str

    Returns
    -------
    avg_time_shift : float

    """
    # path to Events.nev
    evt_file = Path(evt_file)

    # path to bin file
    dat_file = Path(dat_file)

    meta_path = dat_file.with_suffix('.meta')
    with open(meta_path, 'r') as f:
        for line in f:
            if line.startswith('nSavedChans='):
                channel_number = int(line.strip()[len('nSavedChans='):])
            if line.startswith('imSampRate='):
                sample_rate = int(line.strip()[len('imSampRate='):])

    sync_evt_file = evt_file.with_name('sync_evt.npy')
    sync_dat_file = dat_file.with_name('sync_dat.npy')

    # ==== event =====

    if sync_evt_file.exists() and use_cache:
        sync_evt = np.load(sync_evt_file)
    else:
        evt_data = NlxOpen(str(evt_file))
        evt_time = evt_data.data._memorymap['timestamp']
        evt_estr = evt_data.data._memorymap['eventstring']

        def raising_edge(axes, _):
            return np.array([it.startswith(b'TTL') and b'(0x0001)' in it for it in axes])

        def falling_edge(axes, _):
            return np.array([it.startswith(b'TTL') and b'(0x0000)' in it for it in axes])

        raising = np.apply_over_axes(raising_edge, evt_estr, axes=0)
        falling = np.apply_over_axes(falling_edge, evt_estr, axes=0)
        mask = np.logical_or(raising, falling)

        start_time = evt_time[evt_estr == b'Starting Recording']

        evt_edge = np.zeros_like(evt_time)
        evt_time = (evt_time[mask] - start_time) / 1e6
        evt_edge[raising] = 1
        evt_edge = evt_edge[mask]

        sync_evt = np.stack([evt_time, evt_edge]).T

        if save_cache:
            np.save(sync_evt_file, sync_evt)

    # ==== raw data =====
    if sync_dat_file.exists() and use_cache:
        sync_dat = np.load(sync_dat_file)
    else:
        dat_data = np.memmap(dat_file, dtype=np.dtype('int16'), mode='r').reshape(-1, channel_number)
        dat_row, dat_col = dat_data.shape
        dat_time = np.arange(dat_row) / sample_rate
        dat_sync = dat_data[:, channel_number - 1]
        dat_edge = np.diff(dat_sync, prepend=dat_sync[0]) != 0
        dat_time = dat_time[dat_edge]
        dat_sync = dat_sync[dat_edge]

        sync_dat = np.stack([dat_time, dat_sync]).T

        if save_cache:
            np.save(sync_dat_file, sync_dat)

    # ==== time sync signal align ====
    sync_evt = drop_rising_edge(sync_evt)
    sync_dat = drop_rising_edge(sync_dat)
    time_align_frame = time_sync_align(sync_evt, sync_dat)
    # ==== average time shift value ====
    return average_time_align_frame(sync_evt, sync_dat, time_align_frame)
