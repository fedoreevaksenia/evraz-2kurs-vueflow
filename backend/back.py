from database import Database
from bot import Bot
from flask import Flask, request
from threading import Thread
import json

app = Flask(__name__)

activeBotList = {

}


@app.route('/api/schemes/add', methods = ['POST'])
def scheme_add():
    status = 400
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        node_list = { }
        body = request.get_json()

        result_bot = client.query('SELECT bots.id, bots."botToken", sc.back_schema FROM bots LEFT JOIN schemes sc ON sc."botId" = bots.id WHERE sc.id IS NULL LIMIT 1')

        if result_bot is None:
            data = { 'message': 'get bot failed', 'status_code': 400 }
            return data, status

        if len(result_bot) == 0:
            data = { 'message': 'bots are busy', 'status_code': 400 }
            return data, status

        result = client.query('INSERT INTO schemes (name, "botId") VALUES (%s, %s) RETURNING id', [body['name'], result_bot[0]['id']])

        if (len(result) > 0):
            data = { 'message': 'success', 'data': result[0], 'status_code': 200 }
            status = 200
        else:
            data = { 'message': 'Не удалось сохранить схему', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()

    return data, status


@app.route('/api/schemes/<scheme_id>/update', methods = ['POST'])
def scheme_update(scheme_id):
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        node_list = { }
        print(request.get_json(force = True))
        body = request.get_json(force = True)
        schema = request.get_json(force = True)['scheme']
        nodes = schema['nodes']
        for node in nodes:
            if (node['type'] == 'parent'):
                continue
            node_list[node['id']] = { 'label': node['label'], 'childs': [] }
        edges = schema['edges']
        for edge in edges:
            node_list[edge['source']]['childs'].append(edge['target'])

        result = client.query('UPDATE schemes SET front_schema = %s::jsonb, back_schema = %s::jsonb, name = %s WHERE id = %s RETURNING *',
            [json.dumps(schema), json.dumps(node_list), body['name'], scheme_id]
        )

        print(result)

        if len(result) > 0:
            data = { 'message': 'success', 'status_code': 200 }
            result_bot = client.query('SELECT bots.id, bots."botToken", sc.back_schema FROM bots INNER JOIN schemes sc ON sc."botId" = bots.id WHERE sc.id = %s', [scheme_id])

            if body['activeBot'] is True:
                if result_bot[0]["id"] not in activeBotList:
                    print('starting bot', result_bot[0]["id"])
                    bot = Bot(result_bot[0]["botToken"], result_bot[0]["back_schema"])
                    t1 = Thread(target = bot.start)
                    t1.start()
                    activeBotList[result_bot[0]["id"]] = True
            elif result_bot[0]["id"] in activeBotList:
                bot = activeBotList[result_bot[0]["id"]]
                bot.change_schema(result_bot[0]["back_schema"])
        else:
            data = { 'message': 'Не удалось обновить схему', 'status_code': 409 }
    except Exception as err:
        print(err)
    finally:
        client.release()

    return data


@app.route('/api/schemes/<scheme>', methods = ['GET'])
def get_scheme(scheme):
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        result = client.query('SELECT id, name, front_schema, "botId" FROM schemes WHERE id = %s', [scheme])
        if len(result):
            data = result[0]

            if data['botId'] in activeBotList:
                data['activeBot'] = True
            else:
                data['activeBot'] = False

            data = { 'message': data, 'status_code': 200 }
        else:
            data = { 'message': 'not found', 'status_code': 400 }
    except Exception as err:
        print(err)
    finally:
        client.release()
    return data


@app.route('/api/schemes/list', methods = ['GET'])
def get_all_schemes():
    data = { 'message': 'error', 'status_code': 400 }
    client = Database()
    try:
        result = client.query('SELECT id, name FROM schemes ORDER BY name')
        data = { 'message': result, 'status_code': 200 }
    except Exception as err:
        print(err)
    finally:
        client.release()
    return data


# @app.route('/api/bot/add', methods = ['POST'])
# def bot_new():
#     data = { 'message': 'error', 'status_code': 400 }
#     object = request.get_json()
#     client = Database()
#     try:
#         result = client.query('INSERT INTO bots ("botName", "botUserName", "botLink", "botToken") VALUES (%s, %s, %s, %s) RETURNING id',
#             [object['botName'], object['botUserName'], object['botLink'], object['botToken']]
#         )
#         if len(result) > 0:
#             data = { 'message': 'success', 'status_code': 200 }
#         else:
#             data = { 'message': 'Не удалось сохранить бота', 'status_code': 409 }
#     except Exception as err:
#         print(err)
#     finally:
#         client.release()
#     return data
#
#
# @app.route('/api/bot/schema', methods = ['POST'])
# def bot_schema():
#     data = { 'message': 'error', 'status_code': 400 }
#     object = request.get_json()
#     client = Database()
#     try:
#         result = client.query('INSERT INTO connects ("botId", "schemeId") VALUES (%s, %s) RETURNING id', [object['botId'], object['schemeId']])
#         id = result[0]["id"]
#         if len(result) > 0:
#             bot_params = client.query(
#                 'SELECT b."botToken", b."botName", s.back_schema FROM connects c INNER JOIN schemes s ON s.id = c."schemeId" INNER JOIN bots b ON b.id = c."botId" WHERE c.id = %s',
#                 [id]
#             )
#             if (len(bot_params) > 0):
#                 bot = Bot(bot_params[0]["botToken"], bot_params[0]["back_schema"])
#                 t1 = Thread(target = bot.start)
#                 t1.start()
#                 activeBotList[bot_params[0]["botName"]] = bot
#                 data = { 'message': 'success', 'status_code': 200 }
#             else:
#                 data = { 'message': 'Не найдена информация о боте', 'status_code': 409 }
#         else:
#             data = { 'message': 'Не удалось сохранить связь бот/схема', 'status_code': 409 }
#     except Exception as err:
#         print(err)
#     finally:
#         client.release()
#     return data
#
#
# @app.route('/api/bot/get', methods = ['GET'])
# def get_bot_list():
#     data = { 'message': 'error', 'status_code': 400 }
#     client = Database()
#     try:
#         result = client.query('SELECT DISTINCT * FROM bots')
#         if len(result) > 0:
#             data = { 'message': result, 'status_code': 200 }
#         else:
#             data = { 'message': 'Не найдены сохранённые боты', 'status_code': 409 }
#     except Exception as err:
#         print(err)
#     finally:
#         client.release()
#     return data


def load_bots():
    client = Database()

    try:
        result = client.query('SELECT bots."botToken", bots.id as "botId", sc.back_schema FROM schemes sc INNER JOIN bots ON bots.id = sc."botId"')

        for data in result:
            print('starting bot', data["botId"], data["back_schema"])
            if data["back_schema"]:
                bot = Bot(data["botToken"], data["back_schema"])
                t1 = Thread(target = bot.start)
                t1.start()
                activeBotList[data["botId"]] = bot
    except Exception as err:
        print(err)
    finally:
        client.release()


load_bots()
app.run(debug = True)
