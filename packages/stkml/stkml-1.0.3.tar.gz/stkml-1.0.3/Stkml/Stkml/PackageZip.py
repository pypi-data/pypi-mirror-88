import os
from zipfile import ZipFile, ZipInfo

class PackageZip(ZipFile):

    def extract_all(self, path=None, members=None, pwd=None):
        if members is None:
            members = self.namelist()

        if path is None:
            path = os.getcwd()
        else:
            path = os.fspath(path)

        for member in members:
            zinfo = self.getinfo(member)
            ret_val = self._extract_member(zinfo, path, pwd)
            attr = zinfo.external_attr >> 16
            os.chmod(ret_val, attr)

    def zip(self, path: str) -> None:
        ziph = self
        for root, _, files in os.walk(path):
            for file in files:
                file_name = os.path.join(root, file)
                with open(file_name, 'rb') as file_pointer:
                    info = ZipInfo(file_name.replace(f'{path}/', ""))
                    info.external_attr = 0o500 << 16
                    ziph.writestr(info, file_pointer.read())
        ziph.close()
