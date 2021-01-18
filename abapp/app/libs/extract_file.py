import os
import filetype
import tarfile
import zipfile
import shutil

import py7zr
import rarfile

from werkzeug.utils import secure_filename


class ExtractError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def extract_tar_gz_bz2_xz(filepath, dest_dir):
    # filelist is a list contents files whole path,
    # dest_dir is the directory extract to
    print('===============tar gz bz2 xz===================')

    print('filepath  is : ')
    print(filepath)
    extract_names = []

    tar = tarfile.open(filepath)
    names = tar.getnames()

    print('----------------------')
    print('file names: ')
    print(names)
    print('----------------------')

    for name in names:
        tar.extract(name, dest_dir)
        # all_path = os.path.join(dest_dir,name)
        # if not os.path.isdir(all_path):
        extract_names.append(os.path.join(dest_dir,name))

        print('extract name is : ')
        print(extract_names)

    tar.close()


    return extract_names


def extract_zip_file(filepath, dest_dir):
    print('===============zip===================')
    print('filepath  is : ')
    print(filepath)
    extract_names = []

    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_ref.extractall(dest_dir)
    names = zip_ref.namelist()
    zip_ref.close()

    for name in names:
        extract_names.append(os.path.join(dest_dir, name))
    print('extract name is : ')
    print(extract_names)

    return extract_names




def extract_rar_file(filepath, dest_dir):
    #
    print('===============rar===================')
    print('filepath  is : ')
    print(filepath)
    extract_names = []

    rar = rarfile.RarFile(filepath)
    names = rar.namelist()
    for name in names:
        base_name = os.path.basename(name)
        secure_base_name = secure_filename(base_name)
        print('Base name is : ' + base_name)
        print('Secure base name is : ' + secure_base_name)

        if secure_base_name != '':
            new_file = os.path.join(dest_dir, secure_base_name)
            un_rar_file = open(new_file, 'wb')
            un_rar_file.write(rar.read(name))
            un_rar_file.close()
            extract_names.append(new_file)

            print('Extract file: ', end='')
            print(new_file)

    return extract_names


def extract_7z_file(filepath, dest_dir):
    print('===============7z===================')
    print('filepath  is : ')
    print(filepath)
    extract_names = []

    archive = py7zr.SevenZipFile(filepath, mode='r')
    names = archive.getnames()
    archive.extractall(path=dest_dir)
    archive.close()

    for name in names:
        extract_names.append(os.path.join(dest_dir, name))
    print('extract name is : ')
    print(extract_names)

    return extract_names

def extract_recursion(filepathlist, dest_dir, extracted_name_list, error_log):
    for filepath in filepathlist:
        print(filepath)
        if not os.path.isdir(filepath):
            kind = filetype.guess(filepath)

            if kind is None:
                if os.path.dirname(filepath) != dest_dir:
                    try:
                        new_file_path = shutil.copy(filepath, dest_dir)
                    except Exception as e:
                        message = 'Move file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extracted_name_list.append(new_file_path)

                extracted_name_list.append(filepath)

            else:
                print(kind)
                file_type = kind.extension
                if file_type == 'tar':
                    try:
                        extracted_filepathlist = extract_tar_gz_bz2_xz(filepath, dest_dir)
                    except Exception as e:
                        message = 'Extract tar file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == 'gz':
                    try:
                        extracted_filepathlist = extract_tar_gz_bz2_xz(filepath, dest_dir)
                    except Exception as e:
                        message = 'Extract gz file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == 'bz2':
                    try:
                        extracted_filepathlist = extract_tar_gz_bz2_xz(filepath, dest_dir)
                    except Exception as e:
                        message = 'Extract bz2 file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == 'xz':
                    try:
                        extracted_filepathlist = extract_tar_gz_bz2_xz(filepath, dest_dir)
                    except Exception as e:
                        message = 'Extract xz file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == 'zip':
                    try:
                        extracted_filepathlist = extract_zip_file(filepath, dest_dir)
                    except ExtractError as e:
                        message = 'Extract zip file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == 'rar':
                    try:
                        extracted_filepathlist = extract_rar_file(filepath, dest_dir)
                    except ExtractError as e:
                        message = 'Extract rar file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                elif file_type == '7z':
                    try:
                        extracted_filepathlist = extract_7z_file(filepath, dest_dir)
                    except ExtractError as e:
                        message = 'Extract 7z file: ' + filepath + 'failed: ' + str(e)
                        error_log.append(message)
                        print(message)
                    else:
                        extract_recursion(extracted_filepathlist, dest_dir, extracted_name_list, error_log)
                else:
                    message = 'Extract Error: ' + file_type + ' is not supported.'
                    error_log.append(message)
        else:
            # is a folder
            new_root_folder = filepath
            list_dir = os.listdir(filepath)
            # print('new floder: ', end='')
            # print(new_root_folder)

            all_path_list = [os.path.join(new_root_folder, name) for name in list_dir]
            # print('***************************************')
            # print(list_dir)
            # print('***************************************')

            for item in all_path_list:
                extract_recursion([item], dest_dir, extracted_name_list, error_log)





if __name__ == "__main__":
    extracted_name_list = []
    error_log = []

    try:
        extract_recursion(['/home/thetai/tmp/tmp/eee.7z'], '/home/thetai/tmp/tmp/dest', extracted_name_list, error_log)
    except Exception as e:
        print(e)
    else:
        print('ok')

    print('-------------------all over---------------------')
    print('extracted_name_list +++++++++++++++++++++')
    print(extracted_name_list)
    print('error_log +++++++++++++++++++++')
    print(error_log)
