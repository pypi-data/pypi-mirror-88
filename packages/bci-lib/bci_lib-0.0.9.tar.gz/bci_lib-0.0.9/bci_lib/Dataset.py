import os
import pickle
import numpy as np
from mne.io import RawArray
from mne import create_info
from scipy.io import loadmat
from mne.channels import make_standard_montage
from bci_lib import RawData
from bci_lib.DataTypes import BaseData, ID


class Dataset:
    _BASE_LOCAL_LOCATION = '/content/'
    _BASE_LOCAL_LOCATION_reset = _BASE_LOCAL_LOCATION

    @classmethod
    def change_BASE_LOCAL_LOCATION(cls, new_location):
        cls._BASE_LOCAL_LOCATION = new_location

    @classmethod
    def reset_BASE_LOCAL_LOCATION(cls):
        cls._BASE_LOCAL_LOCATION = cls._BASE_LOCAL_LOCATION_reset

    @staticmethod
    def get_file_location(file_name):
        return Dataset._BASE_LOCAL_LOCATION + file_name

    @staticmethod
    def get_current_file_location():
        return Dataset.get_file_location("current_file")

    @staticmethod
    def download(url: str, to: str):
        if url.lower().startswith(("http:", "https:")):
            import requests
            try:
                r = requests.get(url)
            except requests.ConnectionError:
                print("!!! Failed to download data !!!")
            else:
                if r.status_code != requests.codes.ok:
                    print("!!! Failed to download data !!!")
                else:
                    with open(to, "wb") as fid:
                        fid.write(r.content)
        elif url.lower().startswith("ftp:"):
            import shutil
            import urllib.request as request
            from contextlib import closing

            with closing(request.urlopen(url)) as r:
                with open(to, 'wb') as fid:
                    shutil.copyfileobj(r, fid)
        else:
            from shutil import copyfile
            copyfile(url, to)

    @staticmethod
    def delete_file(file):
        if os.path.exists(file):
            os.remove(file)
        else:
            print("The file does not exist")

    @staticmethod
    def load(data_info: dict, save_in_cache: bool = True) -> BaseData:
        # check is in local_location if true load this else call download_and_prepare function
        download_url = data_info['FUNCTION'].__func__(data_info['FILE'])
        local_file_path = Dataset.get_file_location(data_info['LOCAL'])
        prepare_func = data_info['PREPARE_FUNC'].__func__
        current_file_path = Dataset.get_current_file_location()

        if os.path.isfile(local_file_path):
            file_to_read = open(local_file_path, "rb")
            loaded_object = pickle.load(file_to_read)
            file_to_read.close()
        else:
            Dataset.download(download_url, current_file_path)
            loaded_object = prepare_func(current_file_path)
            Dataset.delete_file(current_file_path)
            if save_in_cache:
                loaded_object.save_obj(local_file_path)
        return loaded_object

    class Cho2017:
        _FOLDER_URL = "ftp://parrot.genomics.cn/gigadb/pub/10.5524/100001_101000/100295/mat_data/"
        _FOLDER_URL_reset = _FOLDER_URL

        @classmethod
        def change_FOLDER_URL(cls, new_url):
            cls._FOLDER_URL = new_url

        @classmethod
        def reset_FOLDER_URL(cls):
            cls._FOLDER_URL = cls._FOLDER_URL_reset

        @staticmethod
        def get_FILE_URL(file_name):
            return Dataset.Cho2017._FOLDER_URL + file_name

        @staticmethod
        def prepare(current_file: str, ):
            data = loadmat(current_file, squeeze_me=True, struct_as_record=False,
                           verify_compressed_data_integrity=False)['eeg']
            eeg_ch_names = ['Fp1', 'AF7', 'AF3', 'F1', 'F3', 'F5', 'F7', 'FT7',
                            'FC5', 'FC3', 'FC1', 'C1', 'C3', 'C5', 'T7', 'TP7',
                            'CP5', 'CP3', 'CP1', 'P1', 'P3', 'P5', 'P7', 'P9',
                            'PO7', 'PO3', 'O1', 'Iz', 'Oz', 'POz', 'Pz', 'CPz',
                            'Fpz', 'Fp2', 'AF8', 'AF4', 'AFz', 'Fz', 'F2', 'F4',
                            'F6', 'F8', 'FT8', 'FC6', 'FC4', 'FC2', 'FCz', 'Cz',
                            'C2', 'C4', 'C6', 'T8', 'TP8', 'CP6', 'CP4', 'CP2',
                            'P2', 'P4', 'P6', 'P8', 'P10', 'PO8', 'PO4', 'O2']
            emg_ch_names = ['EMG1', 'EMG2', 'EMG3', 'EMG4']
            ch_names = eeg_ch_names + emg_ch_names + ['Stim']
            ch_types = ['eeg'] * 64 + ['emg'] * 4 + ['stim']
            montage = make_standard_montage('standard_1005')

            imagery_left = data.imagery_left - \
                data.imagery_left.mean(axis=1, keepdims=True)
            imagery_right = data.imagery_right - \
                data.imagery_right.mean(axis=1, keepdims=True)
            eeg_data_l = np.vstack([imagery_left * 1e-6, data.imagery_event])
            eeg_data_r = np.vstack(
                [imagery_right * 1e-6, data.imagery_event * 2])
            eeg_data = np.hstack([eeg_data_l, np.zeros(
                (eeg_data_l.shape[0], 500)), eeg_data_r])

            info = create_info(ch_names=ch_names,
                               ch_types=ch_types, sfreq=data.srate)
            raw = RawArray(data=eeg_data, info=info, verbose=False)
            raw.set_montage(montage)

            raw_data = RawData(id=ID(RawData), data=raw)
            return raw_data

        s01 = {'FILE': 's01.mat', 'LOCAL': 'Cho2017_s01',
               'FUNCTION': get_FILE_URL, 'PREPARE_FUNC': prepare}
