-- Replace non-breaking spaces (U+00A0, UTF-8: 0xC2 0xA0) with regular spaces

--[[
Given

$ cat mw_08.txt
 Window -> Behavior -> System menu appears on ALT-Space -> check

converting this from mediawiki to dokuwiki format using pandoc produces some special characters

$ pandoc -f mediawiki -t dokuwiki mw_08.txt
''%%Window┬á->┬áBehavior┬á->┬áSystem┬ámenu┬áappears┬áon┬áALT-Space┬á->┬ácheck%%''

We can check what these characters are

$ pandoc -f mediawiki -t dokuwiki mw_08.txt | xxd
00000000: 2727 2525 5769 6e64 6f77 c2a0 2d3e c2a0  ''%%Window..->..
00000010: 4265 6861 7669 6f72 c2a0 2d3e c2a0 5379  Behavior..->..Sy
00000020: 7374 656d c2a0 6d65 6e75 c2a0 6170 7065  stem..menu..appe
00000030: 6172 73c2 a06f 6ec2 a041 4c54 2d53 7061  ars..on..ALT-Spa
00000040: 6365 c2a0 2d3e c2a0 6368 6563 6b25 2527  ce..->..check%%'
00000050: 270d 0a                                  '..

So the hexadecimal representation of the bytes corresponding to these special characters are c2 and a0.
We know that \xc2\xa0 is the UTF-8 byte sequence for the non-breaking space U+00A0.
So pandoc is introducing these non-breaking space characters.

If you are calling pandoc on the command line, you can post process the ouput and filter them out using sed.

$ pandoc -f mediawiki -t dokuwiki mw_08.txt | sed 's/\xc2\xa0/ /g'
''%%Window -> Behavior -> System menu appears on ALT-Space -> check%%''

But if you are calling pandoc inside a script (ex:- mediawiki2dokuwiki.sh), it is better to filter them out at the pandoc level itself. This script helps you do exactly that.

Call this script nbsp.lua and place it in the same directory as that of the script that calls pandoc.

Then in the other script add the following to the pandoc command.

--lua-filter="$(dirname "$0")/nbsp.lua"


To test the script on the command line:

$ pandoc -f mediawiki -t dokuwiki mw_08.txt --lua-filter="$rutils/bin/nbsp.lua"
''%%Window -> Behavior -> System menu appears on ALT-Space -> check%%''
--]]

function Str(elem)
    elem.text = elem.text:gsub('\xc2\xa0', ' ')
    return elem
end

function NonBreakingSpace()
    return pandoc.Str(' ')
end

function Code(elem)
    elem.text = elem.text:gsub('\xc2\xa0', ' ')
    return elem
end

function CodeBlock(elem)
    elem.text = elem.text:gsub('\xc2\xa0', ' ')
    return elem
end
