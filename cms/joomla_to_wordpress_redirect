#!/usr/bin/ruby
# -*- coding: utf-8 -*-

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

# Generate redirections for a Joomla to WordPress migration.
# Needs to be customised based on the WordPress URI layout.

require "mysql2"

database = ARGV[0]
prefix = ARGV[1]

class Category
  attr_accessor :id, :parent_id, :path, :title, :alias, :parent, :menu
  def initialize(row)
    @id = row[:id]
    @parent_id = row[:parent_id]
    @path = row[:path]
    @title = row[:title]
    @alias = row[:alias]
  end
end

client = Mysql2::Client.new(:host => "127.0.0.1", :port => 3307,
                            :username => "root", :password => "potato",
                            :database => database,
                            :symbolize_keys => true)

# Find the mapping category_id => menu_path
menus={}
re = /index.php\?option=com_content&view=category&layout=.*&id=([0-9]*)/
client.query("select * from #{prefix}menu").each do |row|
  link = row[:link]
  res = re.match(row[:link])
  if(res)
    menus[res[1].to_i] = row[:path]
  end
end

categories={}
client.query("select * from #{prefix}categories").each do |row|
  category = Category.new row
  categories[category.id] = category
end
# Find the parent of each category:
categories.each do |id,category|
  if category.parent_id != 0
    category.parent = categories[category.parent_id]
  end
end

# Find the suitable menu for each category:
categories.each do |id,category|
  menu_category = category
  while menu_category and not menus[menu_category.id] do
    menu_category = menu_category.parent
  end
  if menu_category
    category.menu = menus[menu_category.id]
  end
end

# Query content:
client.query("select a.id as id, a.alias as alias, a.created as pub,
                     a.catid as catid
              from #{prefix}content a").each do |row|
  slug = "/" + row[:id].to_s + "-" + row[:alias]
  category = categories[row[:catid]]
  menu_path = category.menu
  if not menu_path
    menu_path = ""
  end
  joomla_uri = "/" + menu_path + slug
  wordpress_uri = row[:pub].strftime("/%Y/%m/%d/") + row[:alias] + "/"
  puts ("RedirectPermanent "+joomla_uri + " " + wordpress_uri)
end
