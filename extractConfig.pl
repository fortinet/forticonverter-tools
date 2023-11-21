#!/usr/bin/perl -w

use strict;

my $debug = 0;

MAIN:
{
   my @objectTypes = processArgs();

   foreach my $objectType( @objectTypes ) {
      retrieveObjects( $objectType );
   }
}

sub processArgs {
   showHelp() unless @ARGV == 2;

   my $groupName  = $ARGV[0];
   my $objectType = $ARGV[1];

   lsmscmd( "gotogrp $groupName") or exit;;

   my @objectTypes;
   
   if ( $objectType =~ /^(brick|brickruleset|hostgroup|servicegroup)$/ ) { #brick adicionado
      push( @objectTypes, $objectType );
   }
   elsif( $objectType eq "all" ) {
      @objectTypes = qw( brick brickruleset hostgroup servicegroup );  #brick adicionado
   }
   else { 
      showHelp();
   }
   
   return @objectTypes;
}

sub lsmscmd
{
   my $cmd = shift;
   
   print "lsmscmd(): [$cmd]\n" if $debug;
   my $result = `lsmscmd $cmd 2>&1`;
   print "-> [$result]\n" if $debug;
   if( $result !~ /OK/s ) {
      print STDERR "lsmscmd error: $result";
      exit;
   }
   return $result;
}

sub retrieveObjects
{
   my $objectType = shift;

   my @objectList   = split(/\n+/, lsmscmd("list $objectType"));
   my $objectCount  = scalar @objectList; 
   my $progressText = sprintf("\rProcess [%15s]: %6d entries...", $objectType, $objectCount);
   
   my $count = 0;
   foreach my $objectName( @objectList ) {
      next unless $objectName;
      next if $objectName =~ /LIST.+: *OK/;
      # Only keep values between quotes
      if ($objectName =~ m/'(.+)'/) {
	      $objectName = $1;
		  print "Name: $objectName extract\n";
          lsmscmd("list $objectType $objectName");
          $count++;
          print "$progressText " . int($count*100/$objectCount)."%";
	  }

   }
   print "$progressText done\n";
}

sub showHelp
{
   print <<EOT;
Usage: $0 <groupName> <objectType> 
   groupName:   Name of the group to query
   objectType:  <all|brick|brickruleset|hostgroup|servicegroup>

Note: this sequence must be successful before starting this tool
   # bash
   # export PATH=\$PATH:/opt/isms/lmf
   # . lsmslogon <GUI_user> /tmp/<tmpdir>

EOT

   exit;
}
