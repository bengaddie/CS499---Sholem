#!/usr/bin/perl  -T

=head1 SYNOPSYS

editSholem.cgi book page

Author: Raphael Finkel 1/2015  GPL

=cut

use strict;
use utf8;
use CGI qw/:standard -debug/;
$ENV{'PATH'} = '/bin:/usr/bin:/usr/local/bin:/usr/local/gnu/bin'; # for security

# constants
my $dataDir = "/u/al-d3/csfac/raphael/projects/ocr/SholemAleykhem"; # SVN
my $spellFile = '/homes/raphael/HTML/yiddish/wordlist.utf8.txt';
my %books = (
	202583 => 'Volume 1',
	202584 => 'Volume 2',
	202585 => 'Volume 3',
	202586 => 'Volume 4',
	202587 => 'Volume 5',
	202588 => 'Volume 6',
	202589 => 'Volume 7',
	202590 => 'Volume 8',
	202591 => 'Volume 9',
	202592 => 'Volume 10',
	202593 => 'Volume 11',
	202594 => 'Volume 12',
	202595 => 'Volume 13',
	202596 => 'Volume 14',
	202597 => 'Volume 15',
);
my $css = '
	pre, textarea {
		font-family: "Times New Roman", Times, serif;
		font-size: 100%; 
		font-weight: bold;
	}
	h1 {
		font-size: 200%;
		text-align: center;
	}
	.red {
		color: red;
	}
	.bad {background-color:#FFB0A0;}
	.orig {
		margin-top: 5px;
		background-color:#E0E0EF;
		direction: rtl;
	}
	#myDiv {
		height:650px;
	}
	#myDiv img
	{
		max-width:100%; 
		max-height:100%;
		margin:auto;
		display:block;
	}
';

# variables
my $book;
my $page;
my $user;
my $realName;
my $password;
my $new;
my $authenticate;
my $email;
my $submittedText;
my %okWords; # each ok word just maps to 1

sub init {
	my ($title);
	binmode STDOUT, ":utf8";
	binmode STDERR, ":utf8";
	binmode STDIN, ":utf8";
	$book = param('book');
	$page = param('page');
	$user = untaint(param('user'));
		$user = 'User name' unless defined($user);
	$realName = untaint(param('realName'));
		$user = 'Real name' unless defined($realName);
	$submittedText = param('text');
	$password = untaint(param('password'));
		$password = '' unless defined($password);
	$new = param('new'); $new = 0 unless defined($new);
	$authenticate = param('authenticate');
		$authenticate = 0 unless defined($authenticate);
	$email = untaint(param('email'));
	$title = "Edit $book/$page" if defined($book);
	my $analytics = `cat analytics.txt`;
	# $analytics = ''; # disabled for now
	print header(-type=>"text/html", -expires=>'-1d', -charset=>'UTF-8') ,
		start_html(-encoding=>"UTF-8",
			-title=>$title,
			-dir=>'ltr',
			-script=>"
				function showHidden(what) {
					document.getElementById(what).style.display = 'inherit';
				}
				function hideHidden(what) {
					document.getElementById(what).style.display = 'none';
				}
				" .  $analytics,
			-style=>{-code=>$css,
				-src=>'//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css',
			},
		),
		h1("Correcting OCR for $books{$book}");
	# print "Page is $page; user is $user; password is $password<br/>";
	# print "Accepting new version from $user for $book/$page<br/>" if $new;
	open OKS, $spellFile or die("Cannot read $spellFile\n");
	binmode OKS, ":utf8";
	while (my $line = <OKS>) {
		chomp $line;
		$okWords{$line} = 1;
	}
	close OKS;
} # init

sub doWork {
	my $text;
	print "<div class='container'>";
	if ($new == 1) { # show edited version
		$text = $submittedText;
	} elsif ($new == 2) { # attempt to submit an edited version
		$text = $submittedText;
		$text =~ s//'/g; # unfeather
		if (!passwordOK()) {
			print "<span class='red'>Sorry, your user name or password is wrong, so your changes
			are not accepted.</span>  You can go back or try again here.<br/><br/>\n";
			$new = 0;
		} else {
			print "Accepted (but not stored, because that's not implemented)\n";
		}
	} elsif ($authenticate) {
		print "Request for authentication in process; if approved, you will get
		email.<br/><br/>" , end_html();
		system("echo '\"$user\"' '\"$password\"' '\"$email\"' '\"$realName\"' | " . 
			"/usr/bin/mutt -s 'editSholem authentication request' " .
			" raphael\@cs.uky.edu");
		exit(0);
	} else { # not a new version; look up the current version.
		my $fileName = "$dataDir/$book/$page";
		open DATA, $fileName or die("Cannot read $fileName\n");
		binmode DATA, ":utf8";
		$/ = undef; # slurp
		$text = <DATA>;
		close DATA;
	} # not a new version
	my @lines = split /\n/, $text;
	my $lineCount = 1 + scalar @lines;
	if ($new) {
		print "Here is the updated version of the page.  You may edit it again
		if you like.<br/><br/>\n";
	} else {
		print "Here is the current version of the page.
		When you edit it, please correct
		<ul><li>
		mistaken letters
		</li><li>
		wrong hyphens (distinguish a quotation hyphen (―) from a makef (־))
		</li><li>
		indentation (lines should start at the right margin, and indented
			paragraphs should start with 4 spaces)
		</li><li>
		inter-line spacing (there should be a single blank line after the
			header, no blank line at the bottom)
		</li></ul>
		but don't standardize the spelling.
		<br/></div>
		";
	}
	print "
		<!--<a target='_blank'
			href='https://archive.org/stream/nybc$book#page/n$page/mode/1up'>
			See original scan (new tab)
			</a>
		-->
		<br/><br/>
		<div class='container'>
		<div class='row'>
		<div class='col-sm-2'>
		<button class='button btn-primary'
			id='showHints'
			onclick='
				showHidden(\"theHints\");
				hideHidden(\"showHints\");
				showHidden(\"hideHints\");
			'>
				show hints</button>
		<button class='button btn-warning'
			id='hideHints'
			style='display:none;'
			onclick='
				hideHidden(\"theHints\");
				hideHidden(\"hideHints\");
				showHidden(\"showHints\");
			'>hide hints</button>
		</div>
		<div class='col-sm-2'>
		<button class='button btn-primary'
			id='showOriginal'
			onclick='
				showHidden(\"theOriginal\");
				hideHidden(\"showOriginal\");
				showHidden(\"hideOriginal\");
			'>show original</button>
		<button class='button btn-warning'
			id='hideOriginal'
			style='display:none;'
			onclick='
				hideHidden(\"theOriginal\");
				hideHidden(\"hideOriginal\");
				showHidden(\"showOriginal\");
			'>hide original</button>
		</div></div></div>
		<form action='$0' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='book' value='$book'/>
			<input type='hidden' name='page' value='$page'/>
			<table style='table-layout:fixed;'>
			<tr><td><br/>
			<textarea name='text' dir='rtl' rows='$lineCount'
				id='theText' cols='50'>$text</textarea>
			</td>
			<td id='theHints' style='display:none;'> 
				<br/>
				<pre class='orig'>" . checkSpell($text) . "</pre>
			</td>
			<td ><br/>
				<div id='myDiv'>
				<img
				id='theOriginal' style='display:none;'
				alt='original scan'
				src='images/nybc${book}_orig_tif/nybc${book}_orig_$page.png' />
				</div>
			</td>
			</tr></table>
			<br/>
			<input type='hidden' name='new' value='1'/>
			<input type='submit' value='See new version'/>
		</form>";
	if ($new == 1) { # this is a revised version; allow it to be saved.
		my $featheredText = $text;
		$featheredText =~ s/'//g;
		print "<hr/>
			<form action='$0' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='book' value='$book'/>
			<input type='hidden' name='page' value='$page'/>
			<input type='text' name='user' value='$user'/>User name<br/>
			<input type='password' name='password'
				value='$password'/>password<br/>
			<input type='hidden' name='new' value='2'/>
			<input type='hidden' name='text' value='$featheredText'/>
			<input type='submit' value='Submit new version'/>
			</form>\n";
	}
	print "<hr/>
		<form action='$0' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='book' value='$book'/>
			<input type='text' name='user' value='$user'/>User name<br/>
			<input type='text' name='realName' value='Your full name'/>Full name<br/>
			<input type='password' name='password'
				value='$password'/>password<br/>
			<input type='hidden' name='authenticate' value='yes'/>
			<input type='text' name='email'/>Email&nbsp;
			<input type='submit' value='Request permission to be an editor'/>
		</form>
		<hr/>
		<table><tr><td>
		<form action='$0' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='book' value='$book'/>
			<input type='hidden' name='user' value='$user'/>
			<input type='hidden' name='password' value='$password'/>
			<input type='hidden' name='page' value='" .
				sprintf("%04d", $page-1) .
			"'/>
			<input type='submit'
				value='&laquo; Go to previous page in the book'/>
		</form>
		</td><td>
		<form action='$0' method='post' enctype='multipart/form-data'>
			<input type='hidden' name='book' value='$book'/>
			<input type='hidden' name='user' value='$user'/>
			<input type='hidden' name='password' value='$password'/>
			<input type='hidden' name='page' value='" .
				sprintf("%04d", $page+1) .
			"'/>
			<input type='submit' value='Go to next page in the book &raquo;'/>
		</form>
		</td></tr></table>
		";
} # doWork

sub finalize {
	# $form =~ s/entry/entry1/g;
	print br(), br(), end_html(), "\n";
} # finalize

sub untaint {
	my ($string) = @_;
	$string =~ s/'//g; # we always quote results, so this should be enough
	$string =~ /(.*)/; # remove taint
	$string = $1;
	# print STDERR "string [$string]\n";
	return ($string);
} # untaint

sub passwordOK {
	open PASS, "sholemPasswords";
	while (my $line = <PASS>) {
		my @pieces = split(/:/, $line);
		next unless $pieces[0] eq $user;
		next unless crypt($password, $pieces[1]) eq $pieces[1];
		return 1; # good
	}
	return 0; # bad
}  # passwordOK

sub checkSpell { # returns original text marked up for mis-spelling
	my ($orig) = @_;
	my @answer;
	my $remainder = ''; # first part of a hyphenated word at end of line
	for my $line (split /\n/, $orig) {
		if ($remainder ne '') {
			$line =~ s/^(\s*)/$1$remainder/;
			$remainder = '';
		}
		if ($line =~ s/(\w+)־$//) {
			$remainder = $1;
		}
		my @linePieces;
		for my $part (split(/([\p{P}\s\d]+)/, $line)) {
			if ($part =~ /\p{L}/ and !defined($okWords{$part})) {
				$part = "<span class='bad'>$part</span>";
			}
			push @linePieces, $part;
		} # each part
		push @answer, join(' ', @linePieces);
	} # one line
	return(join("\n", @answer));
} # checkSpell

init();
doWork();
finalize();

