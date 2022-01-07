import json
import asyncio

from src.server.postListener import Listener
import threading
class User:
    def __init__(self, node, username, data):
        self.node = node
        self.username = username
        self.password = data['password']
        self.ip = data['ip']
        self.port = data['port']
        self.followers = data['followers']
        self.following = data['following']

        self.listener = Listener(self)
        threading.Thread(target=self.listener.recv_msg_loop, daemon=True).start()
        #self.timeline = Timeline(username)
    

    def add_follower(self, user_followed):
        if user_followed == self.username:
            print(f"You can't follow yourself")
            return None
        elif user_followed in self.following:
            print(f'You already follow the user {user_followed}')
            return None

        user_info = asyncio.run(self.node.get(self.username))
        user_followed_info = asyncio.run(self.node.get(user_followed))
        
        ### Update followers on user
        if user_info is not None:
            user_info = json.loads(user_info)
            user_info['followers'].append(user_followed)
        else:
            raise Exception(f"You ({self.username}) don't exist on the server")

        ### Update following list on follower
        if user_followed_info is not None:
            user_followed_info = json.loads(user_followed_info)
            user_followed_info['following'].append(self.username)
        else:
            raise Exception(f"The user {user_followed} doesn't exist on the server")

        asyncio.run(self.node.set(self.username, json.dumps(user_info)))

        print("HERE")
        print(json.dumps(user_followed_info))
        asyncio.run(self.node.set(user_followed, json.dumps(user_followed_info)))

        self.following.append(user_followed)

    def get_user(self, username):
        user_info = asyncio.run(self.node.get(username))
        user_info = json.loads(user_info)

        if user_info is None:
            raise Exception("User doesn't exist")
        user = {'username': username, 'ip': user_info['ip'], 'port' :user_info['port'] }
        return user

    def get_followers(self):
        self.following = json.loads(asyncio.run(self.node.get(self.username)))['following']

        followers_info = {}
        for username in self.following:
            followers_info[username] = self.get_user(username)

        print(followers_info)
        return followers_info

    def __str__(self) -> str:
        res = f'User {self.username}:\n'
        res += f'\tPassword: {self.password}\n'
        res += f'\tFollowers:\n'
        for username in self.followers:
            res += f'\t\t> {username}'
        res += f'\tFollowing:\n'
        for username in self.following:
            res += f'\t\t> {username}'
        return res

    # async def view_timeline(self):
    #     print(self.timeline)

    def update_timeline(self, message):
        self.timeline.add_message(message)

    # def get_suggestions(self):
    #     pass


