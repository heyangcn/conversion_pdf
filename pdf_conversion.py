import os
import sys
import logging
import colorlog
import time
from logging.handlers import RotatingFileHandler
import tempfile
from pdf2image import convert_from_path


class logger:
    def __init__(self):
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
        self.log_format = colorlog.ColoredFormatter(
            # '%(log_color)s%(asctime)s %(filename)s%(levelname)s: %(message)s',
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config)
        if not os.path.exists("./log/"):
            os.makedirs("./log/")
        self.log_filename = "./log/error_log.txt"
        self.write_log_file()
        # self.write_log_Onefilename()

    def write_log_file(self):

        logging.getLogger().setLevel(logging.DEBUG)
        # 打印到控制台
        console = logging.StreamHandler()
        # 设置控制台日志输出的级别。如果设置为logging.INFO，就不会输出DEBUG日志信息
        console.setLevel(logging.DEBUG)
        # console.setFormatter(logging.Formatter(self.log_format))
        console.setFormatter(self.log_format)
        logging.getLogger().addHandler(console)
        # logging.getLogger().removeHandler(console)

        # 自动换文件
        handler = logging.handlers.RotatingFileHandler(
            filename=self.log_filename)
        handler.setLevel(logging.DEBUG)
        # handler.setFormatter(logging.Formatter(self.log_format))
        handler.setFormatter(self.log_format)
        logging.getLogger().addHandler(handler)

        # logging.getLogger().removeHandler(handler)

    def write_log_Onefilename(self):
        # 只写在一个文件
        filename = self.log_filename.format(
            time.strftime("%Y-%m-%d", time.localtime(time.time())))
        logging.basicConfig(filename=filename, format=self.log_format,
                            datefmt='%Y-%m-%d %H:%M:%S:%S %p', filemode='a+', level=logging.INFO)


def conver_pdf(destinate_dir, store_dir, folder, filename):
    """TODO: Docstring for conver_pdf.
    :returns: TODO

    """
    filename = destinate_dir+folder+filename
    logging.info("begin to convert file: " + filename)
    try:
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                filename, output_folder=path, first_page=0, dpi=500)
        base_filename = os.path.splitext(os.path.basename(filename))[0]
        if len(images_from_path) == 1:
            save_dir = store_dir+folder
            for page in images_from_path:
                page.save(os.path.join(save_dir, base_filename+'.jpg'), 'JPEG')
        else:
            save_dir = store_dir+folder+base_filename
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            i = 0
            for page in images_from_path:
                i += 1
                page.save(os.path.join(save_dir, str(i)+'.jpg'), 'JPEG')
    except Exception as e:
        # raise e
        logging.error(filename + " convert failed ")

    logging.info("finish convert file: " + filename)


# conver_pdf(filename)

def get_conversion_list(folder_dir):
    """TODO: Docstring for get_conversion_list.
    :returns: TODO

    """
    return [name+'/' for name in os.listdir(
        folder_dir) if os.path.isdir(os.path.join(folder_dir, name))]
    # print(list_dir)


def convert_folderpdf(destinate_dir, store_dir, folder):
    """TODO: Docstring for convert_folderpdf.
    :returns: TODO

    """
    file_list = [file for file in os.listdir(destinate_dir+folder)]
    pdf_list = []
    for file in file_list:
        if file.lower().endswith('.pdf'):
            pdf_list.append(file)
        else:
            logging.warning(destinate_dir+folder+file + " is not a pdf file")

    if len(pdf_list) > 0:
        # create store folder
        if not os.path.exists(store_dir+folder):
            os.makedirs(store_dir+folder)

        for filename in pdf_list:
            conver_pdf(destinate_dir, store_dir, folder, filename)


def main():
    """TODO: Docstring for main.

    :arg1: TODO
    :returns: TODO

    """
    # logger()
    # logging.debug('this is a debug level message')
    # logging.info("this is a info level message")
    # logging.warning("this is a warning level message")
    # logging.error("this is a error level message")
    # logging.critical("this is a critical level message")
    # return
    if len(sys.argv) != 3:
        print("arguments error!")
        return
    folder_dir = sys.argv[1]
    store_dir = sys.argv[2]

    if not os.path.exists(folder_dir):
        print("conversion folder not exists!")
        return
    if not folder_dir.endswith('/'):
        folder_dir += '/'
    if not store_dir.endswith('/'):
        store_dir += '/'

    if folder_dir == store_dir:
        print('destinate dir and store dir can not be same dir!')
        return
    if not os.path.exists(store_dir):
        os.makedirs(store_dir)

    # set log format
    logger()

    folder_list = get_conversion_list(folder_dir)
    if len(folder_list) == 0:
        print('no folder in your dir!')
        return
    for folder in folder_list:
        logging.debug('begin convert '+folder)
        convert_folderpdf(folder_dir, store_dir, folder)
        logging.debug('convert '+folder + ' end')


if __name__ == "__main__":
    main()
