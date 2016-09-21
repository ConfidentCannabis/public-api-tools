"""
Generate html table from list of encoded characters to help
ensure the encoding exactly matches what it should.
"""

source = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
    '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    '{', '|', '}', '~', ' ', '\\t', '\\n', '\\r', '\\x0b', '\\x0c']

python = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29',
    '%2A', '%2B', '%2C', '-', '.', '%2F', '%3A', '%3B', '%3C', '%3D', '%3E',
    '%3F', '%40', '%5B', '%5C', '%5D', '%5E', '_', '%60', '%7B', '%7C', '%7D',
    '%7E', '+', '%09', '%0A', '%0D', '%0B', '%0C']

js = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e',
    'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '%21', '%22', '%23', '%24', '%25', '%26', '%27', '%28', '%29',
    '%2A', '%2B', '%2C', '-', '.', '%2F', '%3A', '%3B', '%3C', '%3D', '%3E',
    '%3F', '%40', '%5B', '%5C', '%5D', '%5E', '_', '%60', '%7B', '%7C', '%7D',
    '%7E', '+', '%09', '%0A', '%0D', '%0B', '%0C']


if __name__ == '__main__':
    lists = [
        ('Source', source),
        ('Python', python),
        ('JS', js)
    ]

    # markdown
    # filename = 'encoding_side_by_side.md'
    # content = '| ' + ' | '.join([l[0] for l in lists]) + ' |\n'
    # content += '|-' + '-|-'.join(['-' * len(l[0]) for l in lists]) + '-|\n'

    # output = zip(*[lang[1] for lang in lists])
    # for row in output:
    #     content += '| ' + ' | '.join( row) + ' |\n'

    # html
    filename = 'encoding_side_by_side.html'
    content = """
    <html>
      <table>
        <thead>
          <tr>"""

    for lang in lists:
        content += """
            <th>{}</th>""".format(lang[0])

    content += """
          </tr>
        </thead>
        <tbody>"""

    output = zip(*[lang[1] for lang in lists])
    for row in output:
        line = '<tr>'
        for col in row:
            line += '<td>{}</td>'.format(col)
        line += '</tr>'
        content += line

    content += """
      </table>
    </html>"""

    with open(filename, 'w') as f:
        f.write(content)
    print "Wrote {}".format(filename)
