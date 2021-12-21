ALLOWED_HOSTS = ["*"]

# Modules in use, commented modules that you won't use
MODULES = [
    'authentication',
    'base',
    'booth',
    'census',
    'mixnet',
    'postproc',
    'store',
    'visualizer',
    'voting',
]



APIS = {
    'authentication': 'https://equipo1decide.herokuapp.com/',
    'base': 'https://equipo1decide.herokuapp.com/',
    'booth': 'https://equipo1decide.herokuapp.com/',
    'census': 'https://equipo1decide.herokuapp.com/',
    'mixnet': 'https://equipo1decide.herokuapp.com/',
    'postproc': 'https://equipo1decide.herokuapp.com/',
    'store': 'https://equipo1decide.herokuapp.com/',
    'visualizer': 'https://equipo1decide.herokuapp.com/',
    'voting': 'https://equipo1decide.herokuapp.com/',
}

BASEURL = 'https://equipo1decide.herokuapp.com/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decidedb',
        'USER': 'decide',
        'HOST': 'localhost',
        'PASSWORD': 'complexpassword',
        'PORT': '5432',
    }
}

# number of bits for the key, all auths should use the same number of bits
KEYBITS = 256