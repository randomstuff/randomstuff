#!/usr/bin/ruby
# coding: utf-8

# The MIT License (MIT)
#
# Copyright (c) 2014 Gabriel Corona
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Remove some crap from HTML snippets. Well they need not be crap but
# there usually are.

require "nokogiri"

## Functions

def remove_attributes(doc, selector, name)
  doc.css(selector).each do |node|
    att = node.attribute(name)
    if att
      node.remove_attribute(name)
      $stderr.puts "Removed name: #{name}\n"
    end
  end
end

def unwrap node
  node.children.each do |x|
    node.before(x)
  end
  node.remove
end

def css_unwrap doc, selector
  doc.css(selector).each do |y|
    $stderr.puts "Unwrapping: #{y}\n"
    unwrap y
  end
end

# Turn <i> into <q>:
def i_to_q(doc)
  doc.css("i").each do |node|
    node.node_name = "q"
  end
end

def split_paragraphs(doc)
# Split paragraphs on <br/>:
  doc.css("p > br").each do |br|
    p = br.parent

    # Clone
    new_p = p.document.create_element("p")
    p.children.take_while{ |x| x!=br }.each do |x|
      new_p.add_child x
    end
    p.before(new_p)

    br.remove
  end
end

def strip_empty_paragraphs(doc)
  # Remove empty paragraphs:
  doc.css("p").each do |node|
    if node.element_children.empty? && /\A *\z/.match(node.inner_text)
      node.remove
    end
  end
end

def pants(doc)
  doc.traverse do |node|
    case node.node_type
    when Nokogiri::XML::Node::TEXT_NODE, Nokogiri::XML::Node::CDATA_SECTION_NODE
      content = node.content
      content.gsub!('...', '…')
      content.gsub!("''", '"')
      content.gsub!(/(\p{L})"/, '\1”')
      content.gsub!(/"(\p{L})/, '“\1')
      content.gsub!(/"(\p{Zs})/, '”\1')
      content.gsub!(/(\p{Zs})"/, '\1“')
      content.gsub!(/"(\p{P})/, '”\1')
      content.gsub!(/(\p{P})"/, '\1“')
      content.gsub!('« ', '« ')
      content.gsub!(' :', ' :')
      content.gsub!(' ;', ' ;')
      content.gsub!(' !', ' !')
      content.gsub!(' ?', ' ?')
      node.content = content
    end
  end
end

# Main script:

if (ARGV[0])
  html = File.read(ARGV[0])
else
  html = $stdin.read
end
doc = Nokogiri::HTML::DocumentFragment.parse html
# TODO, remove <font>
remove_attributes(doc, "*[align]", "align");
remove_attributes(doc, "*[dir]", "dir");
remove_attributes(doc, "*[style]", "style");
remove_attributes(doc, "*[lang]", "lang");
 remove_attributes(doc, "*[class='western']", "class");
css_unwrap(doc, "span")
css_unwrap(doc, "font")
css_unwrap(doc, "address")
for i in (0..6) do
  css_unwrap(doc, "h#{i} b")
end
i_to_q(doc)
split_paragraphs(doc)
strip_empty_paragraphs(doc)
pants(doc)
print doc.to_html
