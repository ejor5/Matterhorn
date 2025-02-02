import requests
from bs4 import BeautifulSoup

def get_wait_time(ride_href):
    try:
        response = requests.get("https://queue-times.com/en-US/parks/16/queue_times")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        ride = soup.find('a', href=ride_href)
        if not ride:
            return "Offline"
        
        wait_span = ride.find('span', class_='has-text-weight-bold', 
                            style=lambda x: x and 'white-space: nowrap' in x)
        if not wait_span:
            return "Closed"
            
        return wait_span.get_text().strip()
    except Exception as e:
        return "Error"

if __name__ == "__main__":
    rides = {
        'Haunted Mansion': '/en-US/parks/16/rides/13958',
        'Space Mountain': '/en-US/parks/16/rides/284'
    }
    
    for ride_name, href in rides.items():
        print(f"{ride_name}: {get_wait_time(href)}")