class CommonFingerprint:

    def __init__(self, common=[]):
        self.common = common

    # append the list of fingerprints with matching hashes from file 1 and 2
    def append(self, file1_fps, file2_fps):
        self.common.append((file1_fps, file2_fps))

    # select to get fingerprint from file
    def get(self, hash_fp_index, file, fingerprint):
        return self.common[hash_fp_index][file][fingerprint]

    # get list of fingerprints with matching hash for file1 or file 2
    def get_fps_substring(self, hash_fp_index, file):
        sub_list = []
        for fingerprint in self.common[hash_fp_index][file]:
            if fingerprint.substring not in sub_list:
                sub_list.append(fingerprint.substring)
        return sub_list

    def clear(self):
        self.common.clear()
