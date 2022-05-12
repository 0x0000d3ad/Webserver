#!/usr/bin/python3

###########################################################################
#
# name          : webserver.py
#
# purpose       : webserver for serving metadata
#
# usage         : python webserver.py
#
# description   :
#
###########################################################################

import datetime
import flask
import flask_restful
import json
import os
import time

from eth_utils import keccak, to_checksum_address
from flask_restful import reqparse
from web3 import HTTPProvider, Web3
from web3.auto import w3

MAX_SUPPLY = 7777

abi = None
with open( os.path.join( "data", "abi.json" ), 'r' ) as f :
    abi = json.load( f )

config_json = None
with open( os.path.join( "data", "appconfig.json" ), 'r' ) as f :
    config_json = json.load( f )

def get_supply() :
    total_supply = None

    try :
        contract_address = to_checksum_address( config_json[ "contract_address" ] )
        w3 = Web3( HTTPProvider( config_json[ "infura_mainnet" ] ) )
        db = w3.eth.contract( address=contract_address, abi=json.dumps( abi ) )
        total_supply = db.functions.totalSupply().call()
    except Exception as e :
        err_string = "[%s] --> Error: Unable to get total supply.  Details: %s" % ( datetime.datetime.now().strftime( "%F %T" ), str( e ) )
        print( err_string )
        with open( "debug.txt", 'a' ) as f :
            f.write( err_string + "\n" )

    return total_supply

app = flask.Flask( __name__ )
api = flask_restful.Api( app )

class GetMetadata( flask_restful.Resource ) :
    def get( self ) :
        return_value = {}
        parser = reqparse.RequestParser()
        parser.add_argument( "tokenId", type=int, help="Get metadata for tokenId" )
        args = parser.parse_args()

        if args.tokenId :
            if args.tokenId >= 0 and args.tokenId <= MAX_SUPPLY :
                metadata_filename = config_json[ "unrevealed" ] 
                total_supply_returned = get_supply()

                if total_supply_returned is None :
                    return_value[ "error" ] = "Failed to get total supply"
                    return return_value

                try :
                    if args.tokenId < total_supply_returned :
                        metadata_filename = os.path.join( config_json[ "metadata_dir" ], "%u.json" % args.tokenId )
                except Exception as e :
                    err_string = "[%s] --> Error: Something bad happened with metadata.  Details: %s" % ( datetime.datetime.now().strftime( "%F %T" ), str( e ) )
                    print( err_string )
                    with open( "debug.txt", 'a' ) as f :
                        f.write( err_string + "\n" )
                with open( metadata_filename, 'r' ) as f :
                    return_value = json.load( f )
            else :
                return_value[ "error" ] = "Invalid tokenId"
        return return_value

api.add_resource( GetMetadata, "/tokenId" )

if __name__ == "__main__" :
    import waitress
    waitress.serve( app, host="0.0.0.0", port=42525 )
