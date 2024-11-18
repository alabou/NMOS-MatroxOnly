#!/bin/sh

# Start the sitemap.xml file
echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?> <urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" > sitemap.xml

# Use `find` to locate files and handle spaces properly with a while loop
find . -type f -name "*.md" | while IFS= read -r file; do
  # Strip the leading `./` from the file path
  file_path=$(echo "$file" | sed 's|^\./||')

  # Convert spaces
  file_path=$(echo "$file_path" | sed 's/ /%20/g')

  # Construct the raw.githubusercontent.com URL
  url="https://raw.githubusercontent.com/alabou/NMOS-MatroxOnly/master/${file_path}"

  # Append the URL to the sitemap
  echo "<url><loc>${url}</loc></url>" >> sitemap.xml
done

# Close the sitemap.xml file
echo "</urlset>" >> sitemap.xml
