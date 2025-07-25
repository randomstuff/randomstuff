#!/usr/bin/ruby
# Grep with xpath.
# ex: grexpath //a/@href https://highlightjs.org/

# TODO, handle XML as well as HTML
# TODO, namespace support (custom prefix)

require "net/http"
require "uri"
require "nokogiri"

uri = ARGV[1]
xpath = ARGV[0]

# Fetch
uri = URI.parse(uri);
response = Net::HTTP.get_response(uri);
html = Nokogiri::HTML::parse(response.body);

ns = {
  'html'   => "http://www.w3.org/1999/xhtml",
  'mathml' => "http://www.w3.org/1998/Math/MathML",
  'svg'    => "http://www.w3.org/2000/svg"
}

html.xpath(xpath, ns).each do |x|
  STDOUT.write(x)
  STDOUT.write "\n"
end

