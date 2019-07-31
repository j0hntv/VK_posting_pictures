# VK_posting_pictures

Script for posting images from [xkcd.com](https://xkcd.com) to the group [VK](https://vk.com).

Example: [xkcd_comics_fun](https://vk.com/xkcd_comics_fun)
### How to install

Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
Create an application on the Vkontakte developer [page.](https://vk.com/dev) The application type should be `standalone`. Get user `access key`. Then get `client_id` and `access_token`. [Read more.](https://vk.com/dev/implicit_flow_user)

Create .env file with environment variables:
```
ACCESS_TOKEN=<ACCESS_TOKEN>
GROUP_ID=<GROUP_ID>
```

### Usage
```
python main.py
```
Enjoy!
### Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org)