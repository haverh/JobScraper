from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

# Extract th
def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def extract_linkedin_job_id(url):
  match = re.search(r'/jobs/view/(\d+)/?', url)
  if match:
    return match.group(1)
  return None

# def extract_indeed_job_id()

app = Flask(__name__)

# Define a route to scrape job postings
@app.route('/scrape-job', methods=['POST'])
def scrape_job():
  # Extract the URL from the request
  job_url = request.json.get('url')
  print("LINE 27:", job_url)

  linkedin_posting = 'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/'

  posting_domain = extract_domain(job_url)

  if (posting_domain == 'www.linkedin.com'):
    job_id = extract_linkedin_job_id(job_url)
    
    response = requests.get(linkedin_posting + job_id)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    company = soup.find('a', class_='topcard__org-name-link').text.strip()
    role = soup.find('h2', class_='top-card-layout__title').text.strip() 

    # Return the extracted data as a JSON response
    return jsonify(
      {
        'status': 'success',
        'data':{'role': role, 'company': company, 'source': 'www.linkedin.com'}
      }
    )
  else:
    # Return the extracted data as a JSON response
    return jsonify(
      {
        'status': 'failure',
        'message': 'There has been an issue extracting job information. Please enter it manually.'
      }
    )

if __name__ == '__main__':
  app.run(debug=True)
