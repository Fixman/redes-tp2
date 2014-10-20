import sys

from urllib.request import urlopen

# The greatest Python script ever written.
# Gets a newline-separated list of files as input, outputs a
# png image with a path between cities.
# Execute with Python 3!

output = open(sys.argv[1], 'wb')

cities = [hop.strip('\n') for hop in sys.stdin]

options = {
    'size': '1280x1280',
    'zoom': '2',

    'markers': 'size:small|' + '|'.join(cities),
    'path': 'weight:1|' + '|'.join(cities),
}

options_string = '&'.join('{}={}'.format(arg, options[arg]) for arg in options)
image = urlopen('http://maps.googleapis.com/maps/api/staticmap?{}'.format(options_string))

output.write(image.read())
