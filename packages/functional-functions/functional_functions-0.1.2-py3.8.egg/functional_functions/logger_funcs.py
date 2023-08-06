def get_logger(filename):
    '''
    The purpose of this function is to create a somewhat standard logger for when you need to add logging to your script.
    The function will check your provided filepath for an existing logs folder, and will create one if it does not exist.
    
    sample syntax on your files:
    
    dir_path = os.path.dirname(os.path.realpath(__file__))

    logging = get_logger(dir_path)
    logger = logging.getLogger(__name__)

    '''

    full_path = filename + '/logs'
    if path.exists(full_path):
        print('found')
    else:
        os.mkdir(filename + '/logs')
        print('made')
    
    logging.basicConfig(filename=full_path + '/logger_' + str(dt.now()) + '.log',
                            format='%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s',
                            filemode='a',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

    return logging