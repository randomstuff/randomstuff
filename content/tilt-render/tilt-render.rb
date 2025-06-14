#!/usr/bin/ruby
require 'tilt'
require 'safe_yaml/load'
require 'ostruct'
require 'optparse'

options = OpenStruct.new
options.data = nil
OptionParser.new do |opt|
  opt.banner = "Render with Tilt"
  opt.on "--data [FILE]", "Data file (YAML)" do |f|
    options.data = f
  end
end.parse!

# Register template renderers:
Tilt.register Tilt::KramdownTemplate, 'md'

def to_obj(x)
  if x.is_a?(Hash)
    res = OpenStruct.new
    x.each do |k,v|
      res[k] = to_obj(v)
    end
    res
  elsif x.is_a?(Array)
    x.map { |y| to_obj(y) }
  else
    x
  end
end

if options.data
  data = to_obj(SafeYAML.load_file(options.data))
else
  data = Object.new
end

templates = ARGV.map { |f| Tilt.new f }

def render(data, templates, i)
  if i == templates.size - 1
    templates[i].render data
  else
    templates[i].render data do
      render data, templates, i + 1
    end
  end
end

print render(data, templates, 0)
