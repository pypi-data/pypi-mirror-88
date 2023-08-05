import rlp
from hashlib import blake2b
from eth_keys import keys
from eth_utils import to_bytes
from rlp.sedes import (
    CountableList,
    big_endian_int,
    binary
)
from .keystore import sha3
from .types import (
    bytearray_to_bytestr,
    decode_hex,
    encode_hex,
    encode_number
)


def noop(value):
    return value


#
# block
#
ETH_BLOCK_KWARGS_MAP = {
    "id": "hash",
    "parentID": "parentHash",
    "signer": "miner",
    "totalScore": "totalDifficulty",
    "txsRoot": "transactionsRoot",
}


BLOCK_FORMATTERS = {
    "number": encode_number,
    "size": encode_number,
    "timestamp": encode_number,
    "gasLimit": encode_number,
    "gasUsed": encode_number,
    "totalScore": encode_number,
}


def meter_block_convert_to_eth_block(block):
    return {
        ETH_BLOCK_KWARGS_MAP.get(k, k): BLOCK_FORMATTERS.get(k, noop)(v)
        for k, v in block.items()
    }


#
# receipt
#
def meter_receipt_convert_to_eth_receipt(receipt):
    return {
        "status": encode_number(0 if receipt["reverted"] else 1),
        "transactionHash": receipt["meta"]["txID"],
        "transactionIndex": encode_number(0),
        "blockNumber": encode_number(receipt["meta"]["blockNumber"]),
        "blockHash": receipt["meta"]["blockID"],
        "cumulativeGasUsed": encode_number(receipt["gasUsed"]),
        "gasUsed": encode_number(receipt["gasUsed"]),
        "contractAddress": None if receipt["reverted"] else receipt["outputs"][0]["contractAddress"],
        "logs": None if receipt["reverted"] else [
            meter_receipt_log_convert_to_eth_log(receipt, index, log)
            for index, log in enumerate(receipt["outputs"][0]["events"])
        ],
    }


#
# log
#
def meter_receipt_log_convert_to_eth_log(receipt, index, log):
    return {
        "type": "mined",
        "logIndex": encode_number(index),
        "transactionIndex": encode_number(0),
        "transactionHash": receipt["meta"]["txID"],
        "blockHash": receipt["meta"]["blockID"],
        "blockNumber": encode_number(receipt["meta"]["blockNumber"]),
        "address": log["address"],
        "data": log["data"],
        "topics": log["topics"],
    }


def meter_log_convert_to_eth_log(address, logs):
    if logs:
        return [
            {
                "logIndex": encode_number(index),
                "blockNumber": encode_number(log["meta"]["blockNumber"]),
                "blockHash": log["meta"]["blockID"],
                "transactionHash": log["meta"]["txID"],
                "transactionIndex": encode_number(0),
                "address": address,
                "data": log["data"],
                "topics": log["topics"],
            }
            for index, log in enumerate(logs)
        ]
    return []


#
# transaction
#
def meter_tx_convert_to_eth_tx(tx):
    return {
        "hash": tx["id"],
        "nonce": tx["nonce"],
        "blockHash": tx["meta"]["blockID"],
        "blockNumber": encode_number(tx["meta"]["blockNumber"]),
        "transactionIndex": encode_number(0),
        "from": tx["origin"],
        "to": tx["clauses"][0]["to"],
        "value": tx["clauses"][0]["value"],
        "gas": encode_number(tx["gas"]),
        "gasPrice": encode_number(1),
        "input": tx["clauses"][0]["data"]
    }


#
# storage
#
def meter_storage_convert_to_eth_storage(storage):
    def _convert_hash(key): return "0x{}".format(
        encode_hex(sha3(to_bytes(hexstr=key))))
    return {
        _convert_hash(v["key"]): v
        for _, v in storage.items()
    }


class Clause(rlp.Serializable):
    fields = [
        ("To", binary),
        ("Value", big_endian_int),
        ("Data", binary),
    ]

    def __init__(self, To, Value, Data):
        super(Clause, self).__init__(To, Value, Data)


class MeterTransaction(rlp.Serializable):
    fields = [
        ("ChainTag", big_endian_int),
        ("BlockRef", big_endian_int),
        ("Expiration", big_endian_int),
        ("Clauses", CountableList(Clause)),  # []
        ("GasPriceCoef", big_endian_int),
        ("Gas", big_endian_int),
        ("DependsOn", binary),  # b""
        ("Nonce", big_endian_int),
        ("Reserved", CountableList(object)),  # []
        ("Signature", binary),  # b""
    ]

    def __init__(self, chain_tag, blk_ref, eth_tx):
        receiver = b"" if "to" not in eth_tx else decode_hex(eth_tx["to"])
        clauses = [
            Clause(
                receiver,
                eth_tx.get("value", 0),
                decode_hex(eth_tx.get("data", "")),
            )
        ]
        super(MeterTransaction, self).__init__(chain_tag, blk_ref, (2 **
                                                                    32) - 1, clauses, 0, eth_tx.get("gas", 3000000), b"", 0, [], b"")

    def sign(self, key):
        '''Sign this transaction with a private key.

        A potentially already existing signature would be overridden.
        '''
        h = blake2b(digest_size=32)
        h.update(rlp.encode(self, MeterTransaction.exclude(["Signature"])))
        rawhash = h.digest()

        if key in (0, "", b"\x00" * 32, "0" * 64):
            raise Exception("Zero privkey cannot sign")

        if len(key) == 64:
            key = to_bytes(hexstr=key)  # we need a binary key
        pk = keys.PrivateKey(key)

        self.Signature = pk.sign_msg_hash(rawhash).to_bytes()


#
# estimate eth gas
#
TX_GAS = 5000
CLAUSE_GAS = 21000 - TX_GAS
CLAUSE_GAS_CONTRACT_CREATION = 53000 - TX_GAS
TX_DATA_ZERO_GAS = 4
TX_DATA_NON_ZERO_GAS = 68


def data_gas(data):
    data = decode_hex(data)
    if len(data) == 0:
        return 0
    z = 0
    nz = 0
    for byt in data:
        if byt == 0:
            z += 1
        else:
            nz += 1
    return (TX_DATA_ZERO_GAS * z) + (TX_DATA_NON_ZERO_GAS * nz)


def intrinsic_gas(transaction):
    total = TX_GAS
    gas = data_gas(transaction["data"])
    total += gas
    cgas = CLAUSE_GAS
    if "to" not in transaction:
        cgas = CLAUSE_GAS_CONTRACT_CREATION
    total += cgas
    return total
