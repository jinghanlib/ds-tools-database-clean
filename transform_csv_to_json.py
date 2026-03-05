#!/usr/bin/env python3
"""Transform Airtable CSV to structured JSON for Eleventy site."""

import csv
import json
import re
import os

def sanitize_filename(name):
    """Create safe filename from tool name."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-').lower()

def create_slug(name):
    """Create URL-friendly slug."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-').lower()

def parse_categories(type_field):
    """Parse comma-separated categories."""
    if not type_field:
        return []
    return [cat.strip() for cat in type_field.split(',') if cat.strip()]

def get_image_filename(name):
    """Get local image filename for a tool."""
    safe_name = sanitize_filename(name)
    # Check for different extensions
    images_dir = 'images'
    for ext in ['.png', '.jpg', '.gif', '.webp', '.svg']:
        if os.path.exists(os.path.join(images_dir, f"{safe_name}{ext}")):
            return f"{safe_name}{ext}"
    return f"{safe_name}.png"  # Default

def transform_csv_to_json(csv_path, output_path):
    """Transform CSV to JSON structure."""
    tools = []
    all_categories = set()

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for i, row in enumerate(reader, 1):
            name = row.get('Name of Source', '').strip()
            if not name:
                continue

            url = row.get('URL ', '').strip()  # Note: CSV has space after URL
            categories = parse_categories(row.get('Type', ''))
            description = row.get('Details', '').strip()
            image_field = row.get('Image', '')
            updated = row.get('Updated', '').strip()

            # Add categories to set
            all_categories.update(categories)

            # Determine if tool has an image
            has_image = bool(image_field)
            image_path = f"/assets/images/{get_image_filename(name)}" if has_image else None

            tool = {
                "id": i,
                "name": name,
                "slug": create_slug(name),
                "url": url if url.startswith('http') else f"https://{url}" if url else "",
                "categories": categories,
                "description": description,
                "image": image_path,
                "updated": updated
            }
            tools.append(tool)

    # Sort categories alphabetically
    sorted_categories = sorted(all_categories)

    output = {
        "tools": tools,
        "categories": sorted_categories
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Transformed {len(tools)} tools")
    print(f"Found {len(sorted_categories)} categories: {sorted_categories}")
    print(f"Output saved to: {output_path}")

if __name__ == '__main__':
    transform_csv_to_json('Data-Grid view.csv', 'tools.json')
