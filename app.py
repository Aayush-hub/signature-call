from cashfree_sdk.payouts import Payouts
from cashfree_sdk.payouts import payouts_config_var
import time
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from flask import Flask, jsonify, render_template
import time
import base64
from cashfree_sdk.exceptions.exceptions import *

Payouts.init("CF156514C693AFFBVPR34I1OCVPG", "f9894c80185ef723a761e9e0567befdb3f8e194b", "PROD", public_key='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy1tQMmHsdFysWCymxntfdc4qhFhL5Jlv/94YPuNgIpbmEySPMsZ1xg04emJE1VtMNVaKpyuz4IFQvwESQC87DqKRmXQd3/eVF1Sdd0IDfKquJb/QXEbUA+xDewTgsjALoex+8IKPUaNeXRYkH+gM21igV4ELtriF+JciMzRdz7QpYo31fqeX9S2poqBV0Uq5pgtJedwuY/cQa8EpT1kSalBFu0f6x5uuDuS7J2kjFyYjm8ahBUyV9tVB+Ye0b5iXM3LsLiKwygeA6JSF7f+PnWVaCnEetIkG8bMG9/1JHJdYsDQLJ8+INX+ucjjswH+GjLZI2CH5s2H06csIc3xFUwIDAQAB')

keyDER = base64.b64decode('MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy1tQMmHsdFysWCymxntfdc4qhFhL5Jlv/94YPuNgIpbmEySPMsZ1xg04emJE1VtMNVaKpyuz4IFQvwESQC87DqKRmXQd3/eVF1Sdd0IDfKquJb/QXEbUA+xDewTgsjALoex+8IKPUaNeXRYkH+gM21igV4ELtriF+JciMzRdz7QpYo31fqeX9S2poqBV0Uq5pgtJedwuY/cQa8EpT1kSalBFu0f6x5uuDuS7J2kjFyYjm8ahBUyV9tVB+Ye0b5iXM3LsLiKwygeA6JSF7f+PnWVaCnEetIkG8bMG9/1JHJdYsDQLJ8+INX+ucjjswH+GjLZI2CH5s2H06csIc3xFUwIDAQAB')
keyPub = RSA.importKey(keyDER)
app = Flask(__name__)


# @app.route('/')
# def initial_route():
#     return render_template('index.html')


@app.route('/', methods=['GET'])

def generate_signature():
    if payouts_config_var.signature != "" and payouts_config_var.signature_expiry != 0 and (payouts_config_var.signature_expiry - time.time()) > 0:
        return
    cur_time = round(time.time())
    cur_time_str = str(cur_time)
    encode_data = payouts_config_var.payout_creds.client_id + "." + cur_time_str
    encrypter = PKCS1_OAEP.new(keyPub)
    signature = encrypter.encrypt(encode_data.encode())
    signature_str = base64.b64encode(signature).decode("utf-8")
    payouts_config_var.signature = signature_str
    payouts_config_var.signature_expiry = cur_time+100000

    return jsonify(signature_str=signature_str)

if __name__ == "__main__":
    app.run(debug=True)


"""
server
client -> POST request HIT-> server ->  prediction back to client 

Steps
---------------
# Get audio file and save it 
# Invoke the service (ASR)
# make a prediction 
# remove the audio file  from the current dir
# send back the predicted keywors or string to client in json format

"""
