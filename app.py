from flask import Flask, render_template, request
from flask import url_for, json, jsonify
import  requests
from datetime import datetime


#===================================== CONFIGURATION ===================================================================

#Start back-end server
app = Flask(__name__, static_url_path='/static')

#Initialize dummy database, note the property 'available' so we can keep track of spending
dummy_db = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z","available": 1000 }
,{ "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z","available": 200 }
, { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z","available": -200 }
, { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z","available": 10000 }
, { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z","available": 300 }]


#add transaction
@app.route('/addtx', methods=['POST'])
def add_tx():
    try:
        content = request.get_json()
        data = {"timestamp": content['timestamp'], "payer":content['payer'], "points": content['points'], "available": content['points']}
        dummy_db.append(data)
        return('success!')

    except Exception as err:
        print(f'Other error occurred: {err}')

#spend points
@app.route('/spend', methods=['POST'])
def spend_tx():
    try:
        content = request.get_json()
        payment = content['points'] #points to spend
        dummy_db.sort(key=lambda x:datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ')) #sort by oldest to newest so we can iterate
        sum_total = 0
        if payment <= 0:
            return('payment amout not valid!')
        for i in dummy_db:
            sum_total += i['available']
        if sum_total >= payment:
            pre_output= {} #convenient pre output that will be parsed later

            for tx in dummy_db: #Cheking for negative inputs so we can deduct it from the oldest available Tx
                if (tx['available'] < 0):
                    negative = tx['available'] * -1
                    tx.update({"available":0}) #updating the tx so it doesn't have negative points
                    for tx_2 in dummy_db: #This is where we deduct the poins into the oldest available Tx
                        if (tx_2['payer'] == tx['payer']) and (negative <= tx_2['available']):
                            tx_2.update({"available": tx_2['available'] - negative})

            for tx in dummy_db:   #In this iteration we check and deduct points on availble Txs in chronological order
                if (tx['available'] < payment) and (tx['available'] != 0) :
                    payment -= tx['available']
                    if tx['payer'] not in pre_output:
                        pre_output.update({tx['payer']:tx['available']})
                        tx.update({"available":0})
                    else:
                        sum_1 = pre_output[tx['payer']]
                        sum_2 = tx['points']
                        suma = sum_1 + sum_2
                        pre_output.update({tx['payer']:suma})
                        tx.update({"available":0})
                elif (tx['available'] != 0):  #If ponts to spend are mayor to points available in Tx we go this way
                    points  =  payment
                    if tx['payer'] not in pre_output:
                        pre_output.update({tx['payer']:points})
                        tx.update({"available":tx['available'] - points})
                    else:
                        sum_1 = pre_output[tx['payer']]
                        sum_2 = points
                        suma = sum_1 + sum_2
                        pre_output.update({q['payer']:suma})
                        tx.update({"available":tx['available'] - points})
                    break #at this point we can safely assume that payment equals cero so we break this iteration
            result_list = []
            for payer in pre_output: #we'll iterate on the pre_outputs so we can add our new spent points to either response and database
                if pre_output[payer]!= 0:
                    result_list.append({'payer':payer, 'points':pre_output[payer]*-1})
                    dummy_db.append({'payer':payer, 'points':pre_output[payer]*-1, 'timestamp':datetime.strftime(datetime.now(),'%Y-%m-%dT%H:%M:%SZ'), 'available': 0})
            #print(dummy_db)
            return jsonify(result_list)
        else:
            return('Not enough balance!')



    except Exception as err:
        print(f'Other error occurred: {err}')

@app.route('/balance', methods=['GET'])
def balance():
    try:
        dummy_db.sort(key=lambda x:datetime.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ'))
        pre_output={}
        for q in dummy_db:
            if q['payer'] not in pre_output:
                pre_output.update({q['payer']:q['available']})
            else:
                sum_1 = pre_output[q['payer']]
                sum_2 = q['available']
                suma = sum_1 + sum_2
                pre_output.update({q['payer']:suma})

        return jsonify(pre_output)


    except Exception as err:
        print(f'Other error occurred: {err}')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
