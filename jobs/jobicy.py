import urllib.request
import xml.etree.ElementTree as ET

def fetch_jobicy_rss(url: str = "https://jobicy.com/jobs-rss-feed"):
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        jobs = []
        for item in root.find('channel').findall('item'):
            job = {
                "title": item.findtext("title", default=""),
                "link": item.findtext("link", default=""),
                "pubDate": item.findtext("pubDate", default=""),
                "description": item.findtext("description", default=""),
            }
        jobs.append(job)
        return jobs


    except Exception as e:
        print("Error fetching RSS:", e)
        return []


if __name__ == "__main__":
    data = fetch_jobicy_rss()
    for job in data[:5]:  # print first 5
        print(job["title"], job["link"], "\n")