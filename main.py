import string
import random
import json
import tls_client

session = tls_client.Session(random_tls_extension_order=True)

def get_random_string(lenght = random.randint(8, 12)) -> str:
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(lenght))

def get_image_link() -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1'
    }

    response = session.get(url, headers=headers).text
    json_data: dict = json.loads(json.loads(json.dumps(response.split('window.__APOLLO_STATE__=')[1].split('</script>')[0][:-1])))
    filtered_keys: list = [key for key in json_data.keys() if key.endswith('.previews.0')]

    downloand_list: list = []
    for key in filtered_keys:
        downloand_list.append(json_data[key]["url"].replace('{{%2F}}', '/'))

    return downloand_list

def downloand_image(links: list) -> None:
    for link in links:
        try:
            response = session.get(link)
            if response.status_code == 200:
                with open(f"image/{get_random_string()}.jpg", 'wb') as f:
                    f.write(response.content)
        except:
            pass

def start() -> None:
    links = get_image_link()
    print(f"\n[*] {len(links)} image source was taken\n[*] Images are downloading...")
    downloand_image(links)

if __name__ == '__main__':
    url = input("[*] Enter store link: ")

    start()



