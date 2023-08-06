import getpass
import webbrowser

from imgflip.api import get_memes, caption_image


memes = get_memes()
for i, meme in enumerate(memes):
    print(i, meme['name'], meme['id'])

index = int(input('Select id: '))
template_id = memes[index]['id']
username = input('Username: ')
password = getpass.getpass()
text0 = input('Text 0: ')
text1 = input('Text 1: ')
image = caption_image(template_id, username, password, text0, text1)
print(image)

webbrowser.open(image['data']['url'], new=2)
