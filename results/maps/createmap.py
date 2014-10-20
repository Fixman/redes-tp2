import sys

from urllib.request import urlopen

# The greatest Python script ever written.
# Gets a newline-separated list of files as input, outputs a
# png image with a path between cities.
# Execute with Python 3!

output = open(sys.argv[1], 'wb')

cities = [hop.strip().split() for hop in sys.stdin]

options = {
    'size': '1280x1280',
    'scale': '2',
    'zoom': '2',

    'style': 'feature:all|element:labels|visibility:off',

    # For the record, I know this is a horrible, horrible hack. Sorry!
    'markers': '&markers='.join('size:mid|label:{}|color:{}|{}'.format(x[0][0], 'red' if x[2] == '1' else 'blue', x[0]) for x in cities),
    'path': '&path='.join('weight:1|color:{}|{}|{}'.format('red' if cities[i][1] == '1' else 'blue', cities[i - 1][0], cities[i][0]) for i in range(1, len(cities)))
}

options_string = '&'.join('{}={}'.format(arg, options[arg]) for arg in options)
image = urlopen('http://maps.googleapis.com/maps/api/staticmap?{}'.format(options_string))

output.write(image.read())
