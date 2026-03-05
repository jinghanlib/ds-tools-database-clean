#!/usr/bin/env python3
"""Download images from Airtable CSV before URLs expire."""

import csv
import os
import re
import time
import urllib.request
import urllib.error
import ssl

def extract_image_url(image_field):
    """Extract URL from Airtable image field format: filename.png (https://...)"""
    match = re.search(r'\((https?://[^)]+)\)', image_field)
    return match.group(1) if match else None

def sanitize_filename(name):
    """Create safe filename from tool name."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-').lower()

def download_images(csv_path, output_dir):
    """Download all images from CSV to output directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Create SSL context that doesn't verify (Airtable CDN sometimes has issues)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    downloaded = 0
    failed = 0
    skipped = 0

    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        total = len(rows)

        for i, row in enumerate(rows):
            name = row.get('Name of Source', '')
            image_field = row.get('Image', '')

            if not name:
                continue

            if not image_field:
                print(f"[{i+1}/{total}] No image: {name}")
                skipped += 1
                continue

            url = extract_image_url(image_field)
            if not url:
                print(f"[{i+1}/{total}] Invalid image field: {name}")
                skipped += 1
                continue

            safe_name = sanitize_filename(name)

            # Determine extension from URL or default to png
            if '.jpg' in url.lower() or '.jpeg' in url.lower():
                ext = '.jpg'
            elif '.gif' in url.lower():
                ext = '.gif'
            elif '.webp' in url.lower():
                ext = '.webp'
            elif '.svg' in url.lower():
                ext = '.svg'
            else:
                ext = '.png'

            filename = f"{safe_name}{ext}"
            filepath = os.path.join(output_dir, filename)

            # Skip if already downloaded
            if os.path.exists(filepath):
                print(f"[{i+1}/{total}] Already exists: {filename}")
                downloaded += 1
                continue

            try:
                request = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
                )
                with urllib.request.urlopen(request, timeout=30, context=ctx) as response:
                    with open(filepath, 'wb') as img:
                        img.write(response.read())
                print(f"[{i+1}/{total}] Downloaded: {filename}")
                downloaded += 1
                time.sleep(0.3)  # Be nice to the server
            except Exception as e:
                print(f"[{i+1}/{total}] Failed: {name} - {e}")
                failed += 1

    print(f"\n--- Summary ---")
    print(f"Downloaded: {downloaded}")
    print(f"Failed: {failed}")
    print(f"Skipped (no image): {skipped}")
    print(f"Total: {total}")

if __name__ == '__main__':
    csv_path = 'Data-Grid view.csv'
    output_dir = 'images'

    print(f"Downloading images from: {csv_path}")
    print(f"Saving to: {output_dir}")
    print()

    download_images(csv_path, output_dir)
