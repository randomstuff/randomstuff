#!/bin/sed -f
# Transform a TSV file into an HTML table

s/&/\&amp;/g
s/</\&lt;/g

# The first line is the thead row:
1 s/^/<table><thead>\
<tr><th>/g
1 s%	%</th><th>%g
1 s%$%</th>\
</thead>\<tbody>%g

# The other lines are the tbody rows:
2~1 s/^/<tr><td>/g
2~1 s%	%</td><td>%g
2~1 s%$%</td></tr>%g

# Close the table:
$ a </tbody></table>
