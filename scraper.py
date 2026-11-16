import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://realpython.github.io/fake-jobs/"

def fetch_page(url):
    """Download the page and return its HTML."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Stops with an error if the request failed
    return response.text

def parse_jobs(html):
    """Extract job info from the HTML."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.find_all("div", class_="card-content"):
        title = card.find("h2", class_="title").get_text(strip=True)
        company = card.find("h3", class_="company").get_text(strip=True)
        location = card.find("p", class_="location").get_text(strip=True)
        date = card.find("time").get_text(strip=True)
        link = card.find_all("a")[-1]["href"]

        jobs.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Date Posted": date,
            "Apply Link": link,
        })

    return jobs

def save_to_excel(jobs, filename="jobs.xlsx"):
    """Save the list of jobs to an Excel file."""
    df = pd.DataFrame(jobs)
    df.to_excel(filename, index=False)
    print(f"Saved {len(df)} jobs to {filename}")

def main():
    html = fetch_page(URL)
    jobs = parse_jobs(html)
    save_to_excel(jobs)

if __name__ == "__main__":
    main()
