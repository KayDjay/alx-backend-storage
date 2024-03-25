-- Script to create an index on the first letter of name in the table names

CREATE INDEX idx_name_first ON names (LEFT(name, 1));