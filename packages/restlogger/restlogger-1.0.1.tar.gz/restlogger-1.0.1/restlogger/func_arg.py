import sys, getopt, io

def my_argument_function(argv):
    """Get the CLI argument into a python dictionary
        The dictionary that is used in My_Logger_Class is called argu
        and commes with already predefined arguments such as freq=5.

        The Try usese the getopt to get the opt/arguments from the user imput.

        In the For Loop, the apropriate user imput argument is placed in
        the right slot in the dictionary called argu.

    """

    argu = {
            'freq' : 5,
            'url' : 'http://api.openweathermap.org/data/2.5/weather?q=Zurich,CHZH&appid=3836093dde650898eb014e6f27304646',
            'xpath' : '',
            'key' : 'name', 
            'change' : 'no',
            }
    try:
        opts, args = getopt.getopt(argv,"hf:u:x:k:c:",["freq=","url=","xpath=","key=","change="])
    except getopt.GetoptError:
        print('-f <freq> -u <url> -x <xpath> -k <key> -c <y/n>')
        sys.exit()

    for opt, arg in opts:
        if opt == '-h':
            print('restlogger -f <freq> -u <url> -x <xpath> -k <key> -c <y/n>')
            sys.exit()
        elif opt in ("-f", "--freq"):
            argu['freq'] = int(arg)

        elif opt in ("-u", "--url"):
            argu['url'] = arg

        elif opt in ("-x", "--xpath"):
            argu['xpath'] = arg

        elif opt in ("-k", "--key"):
            argu['key'] = arg
        
        elif opt in ("-c", "--change"):
            argu['change'] = arg

    return argu
