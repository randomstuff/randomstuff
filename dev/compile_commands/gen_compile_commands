#!/usr/bin/ruby

# Usage: gen_compile_commands compile_commands.yaml
# With compile_commands.yaml:
#
# ---
# - pattern:
#    - "**/*.{h,hpp}"
#    - "**/*.cpp"
#   command: clang++ -x c++ -std=c++11 -c
# - pattern: "**/*.c"
#   command: clang -std=gnu11 -c
# ---

require 'yaml'
require 'json'

input = YAML.load(File.read(ARGV[0]))

output = input.map do |e|
  patterns = if e["pattern"].respond_to? "each"
               e["pattern"]
             else
               [ e["pattern"] ]
             end
  patterns.map do |pattern|
    Dir.glob(pattern).map do |file|
      res = {
        :file => file,
        :directory => Dir.pwd,
        :command => "#{e["command"]} #{file}",
      }
      res
    end
  end
end

puts JSON.pretty_generate(output.flatten)
