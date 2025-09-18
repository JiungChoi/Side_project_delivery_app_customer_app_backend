-- Migration: Add menu information fields to cart_item table
-- Date: 2025-01-XX
-- Description: Add menu_name, menu_description, and menu_image_url columns to cart_item table

-- Add new columns to cart_item table
ALTER TABLE cart_service.cart_item 
ADD COLUMN menu_name VARCHAR(255) DEFAULT '';

ALTER TABLE cart_service.cart_item 
ADD COLUMN menu_description TEXT;

ALTER TABLE cart_service.cart_item 
ADD COLUMN menu_image_url VARCHAR(500);

-- Update existing records with empty menu_name (since it's required)
-- In production, you would populate this from the menu_service data
UPDATE cart_service.cart_item 
SET menu_name = 'Unknown Menu' 
WHERE menu_name IS NULL OR menu_name = '';

-- Make menu_name NOT NULL after updating existing records
ALTER TABLE cart_service.cart_item 
ALTER COLUMN menu_name SET NOT NULL;

-- Create index for better performance on menu_name queries
CREATE INDEX idx_cart_item_menu_name ON cart_service.cart_item(menu_name);