import asyncio, struct, time, random
import websockets
import logging
import socket
import json

async def handle_websocket(websocket, path):
    if "editor" in path:
        await handle_editor_request(websocket)
        return
    
    msgs = []
    users = []

    def msg_ws(user, address, *args):
        msgs.append((user, address, args))

    def user_ws(users_now):
        for user in users_now:
            users.append(user)
    
    Connection.notification_callbacks.append(msg_ws)

    oscrouter = Group.index.get('oscrouter', None)
    if oscrouter:
        oscrouter.users.notification_callbacks.append(user_ws)
        oscrouter.users.notify_cbs()

    async def send_msgs():
        msgs_dict = {'messages': []}
        while len(msgs) > 0:
            user, address, args = msgs.pop(0)
            msgs_dict['messages'].append({'user': user.name, 'address': address, 'args': args})
        
        if len(msgs_dict['messages']) > 0:
            await websocket.send(json.dumps(msgs_dict))
        
        users_dict = {'users': {}}
        while len(users) > 0:
            user = users.pop(0)
            users_dict['users'][user.name] = [conn.peername for conn in user.connections]
        
        if users_dict['users'] != {}:
            await websocket.send(json.dumps(users_dict))

    try:
        while True:
            await send_msgs()
            await asyncio.sleep(0.1)
    except (websockets.exceptions.ConnectionClosedOK,
            websockets.exceptions.ConnectionClosedError):
        pass
    except Exception as e:
        logging.exception(f"Websocket {websocket} raised exception...")
    finally:
        Connection.notification_callbacks.remove(msg_ws)
        if oscrouter:
            oscrouter.users.notification_callbacks.remove(user_ws)
    logging.info(f"Websocket {websocket} connection leaving...")
