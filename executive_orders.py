import requests
from bs4 import BeautifulSoup

def fetch_executive_orders():
    base_url = "https://www.whitehouse.gov/presidential-actions/page/{}/"
    max_pages = 20  # Number of pages to scrape
    markdown_content = "# Executive Orders\n\n"
    order_count = 0

    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        response = requests.get(base_url.format(page))
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Skipping.")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        orders = soup.find_all('h2', class_='wp-block-post-title')

        if not orders:
            print(f"No executive orders found on page {page}. Stopping.")
            break

        for order in orders:
            order_count += 1
            title = order.get_text(strip=True)
            link = order.find('a')['href']

            print(f"Fetching content for: {title}")
            # Fetch the content of each executive order
            order_response = requests.get(link)
            if order_response.status_code == 200:
                order_soup = BeautifulSoup(order_response.text, 'html.parser')
                # Adjust this selector based on the actual HTML structure
                content_section = order_soup.find('div', class_='entry-content')
                if content_section:
                    # Extract all paragraph texts within the content section
                    content = "\n\n".join(p.get_text(strip=True) for p in content_section.find_all('p'))
                else:
                    content = "Content not available."
            else:
                content = "Failed to fetch content."

            # Add to the Markdown file
            markdown_content += f"<details>\n<summary>{order_count}. {title}</summary>\n\n"
            markdown_content += f"{content}\n\n"
            markdown_content += f"[Read more]({link})\n\n</details>\n\n"

    # Save to a Markdown file
    with open("executive_orders.md", "w") as file:
        file.write(markdown_content)

    print(f"Markdown file generated as 'executive_orders.md'. Total orders fetched: {order_count}")

if __name__ == "__main__":
    fetch_executive_orders()
