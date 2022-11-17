#!/bin/sh

# turn on Bluray Disc Player
if [ $1 = "bd" ]; then
   echo "tx 4F:82:21:00" | cec-client -s
fi

# turn on TV
if [ $1 = "tv" ]; then
   echo "tx 4F:82:30:00" | cec-client -s
fi

# turn on Amp
if [ $1 = "ampon" ]; then
   echo "on 5" | cec-client -s
fi

# turn off Amp
if [ $1 = "ampoff" ]; then
   echo "standby 5" | cec-client -s
fi

exit 0