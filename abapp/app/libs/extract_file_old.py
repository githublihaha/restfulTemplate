import os
import filetype
import bz2
import tarfile
import zipfile

import py7zr
import rarfile

class ExtractError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def extract_tar_or_gz(filelist, dest_dir):
    # filelist is a list contents files whole path,
    # dest_dir is the directory extract to
    extract_names = []
    for filepath in filelist:
        try:
            tar = tarfile.open(filepath)
            names = tar.getnames()

            print('----------------------')
            print('tar file names: ')
            print(names)
            print('----------------------')

            extract_names.extend(names)
            for name in names:
                tar.extract(name, dest_dir)
            tar.close()
        except Exception as e:
            message = 'Extract tar file failed: ' + e
            filename = os.path.basename(filepath)
            code = 400
        else:
            message = 'Extract tar file succeeded.'
            filename = '  '.join(names)
            code = 200






def extract_file(filepath, dest_dir):
    # init
    message = ''
    filename = ''
    code = 200


    kind = filetype.guess(filepath)
    if kind is None:
        # txt file
        message = 'It looks like a text file.'
        filename = os.path.basename(filepath)
        code = 200
    else:
        file_type = kind.extension()
        if file_type == 'tar' or file_type == 'gz':
            try:
                tar = tarfile.open(filepath)
                names = tar.getnames()
                for name in names:
                    tar.extract(name, dest_dir)
                tar.close()
            except Exception as e:
                message = 'Extract tar file failed: ' + e
                filename = os.path.basename(filepath)
                code = 400
            else:
                message = 'Extract tar file succeeded.'
                filename = '  '.join(names)
                code = 200
        elif file_type == 'zip':
            try:
                zip_ref = zipfile.ZipFile(filepath, 'r')
                zip_ref.extractall(dest_dir)
                names = zip_ref.namelist()
                zip_ref.close()
            except Exception as e:
                message = 'Extract zip file failed: ' + e
                filename = os.path.basename(filepath)
                code = 400
            else:
                message = 'Extract zip file succeeded.'
                filename = '  '.join(names)
                code = 200
        elif file_type == 'bz2':
            try:
                bz2file = bz2.BZ2File(filepath)
                file_base_name = os.path.basename(filepath)
                basename = file_base_name.split('.')[0]
                new_file = os.path.join(dest_dir, basename)
                un_bz2_file = open(new_file, 'wb')
                un_bz2_file.write(bz2file.read())
                bz2file.close()
                un_bz2_file.close()

                new_file_type = filetype.guess_extension(new_file)
                if new_file_type is None:
                    bz2_filename = basename
                    pass
                elif new_file_type == 'tar':
                    tar = tarfile.open(new_file)
                    names = tar.getnames()
                    for name in names:
                        tar.extract(name, dest_dir)
                    tar.close()
                    bz2_filename = '  '.join(names)
                else:
                    raise Exception
            except Exception as e:
                message = 'Extract bz2 file failed: ' + e
                filename = os.path.basename(filepath)
                code = 400
            else:
                message = 'Extract bz2 file succeeded.'
                filename = bz2_filename
                code = 200
        elif file_type == 'rar':
            try:
                rar = rarfile.RarFile(filepath)
                names = rar.namelist()
                for name in names:
                    rar.extract(name, dest_dir)
                rar.close()
            except Exception as e:
                message = 'Extract rar file failed: ' + e
                filename = os.path.basename(filepath)
                code = 400
            else:
                message = 'Extract rar file succeeded.'
                filename = '  '.join(names)
                code = 200
        elif file_type == '7z':
            try:
                archive = py7zr.SevenZipFile(filepath, mode='r')
                names = archive.getnames()
                archive.extractall(path=dest_dir)
                archive.close()
            except Exception as e:
                message = 'Extract 7z file failed: ' + e
                filename = os.path.basename(filepath)
                code = 400
            else:
                message = 'Extract 7z file succeeded.'
                filename = '  '.join(names)
                code = 200


    return message, filename, code


